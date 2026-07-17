import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / ".agents" / "skills" / "ai-research" / "scripts"
INIT_SCRIPT = SCRIPTS / "init_research_pack.py"
VALIDATE_SCRIPT = SCRIPTS / "validate_research_pack.py"


class InitResearchPackTests(unittest.TestCase):
    def run_init(
        self,
        root: Path,
        *,
        task_type: str = "github",
        topic: str = "Codex Dream Skin",
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(INIT_SCRIPT),
                "--root",
                str(root),
                "--topic",
                topic,
                "--task-type",
                task_type,
                "--question",
                "Is it worth trying on this Windows machine?",
                "--decision-goal",
                "Decide whether to trial or watch the repository.",
                "--date",
                "2026-07-17",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_creates_a_public_sanitized_research_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            result = self.run_init(root)

            self.assertEqual(result.returncode, 0, result.stderr)
            pack = root / "_research" / "2026-07-17-codex-dream-skin"
            self.assertEqual(
                {path.name for path in pack.iterdir()},
                {
                    "brief.md",
                    "sources.jsonl",
                    "claims.jsonl",
                    "scorecard.json",
                    "decision.md",
                },
            )
            scorecard = json.loads((pack / "scorecard.json").read_text(encoding="utf-8"))
            self.assertEqual(scorecard["rubric"], "github")
            self.assertEqual(scorecard["weighted_score"], 0.0)
            self.assertIn("visibility: public-sanitized", (pack / "brief.md").read_text(encoding="utf-8"))

            index_text = (root / "_research" / "index.md").read_text(encoding="utf-8")
            self.assertIn("2026-07-17-codex-dream-skin", index_text)
            self.assertIn("collecting", index_text)

    def test_refuses_to_overwrite_an_existing_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            first = self.run_init(root)
            self.assertEqual(first.returncode, 0, first.stderr)

            second = self.run_init(root)

            self.assertNotEqual(second.returncode, 0)
            self.assertIn("already exists", second.stderr)

            index_text = (root / "_research" / "index.md").read_text(encoding="utf-8")
            self.assertEqual(index_text.count("| [2026-07-17-codex-dream-skin]"), 1)

    def test_fact_check_uses_claim_statuses_without_a_project_score(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            result = self.run_init(root, task_type="verify", topic="A disputed AI claim")

            self.assertEqual(result.returncode, 0, result.stderr)
            pack = root / "_research" / "2026-07-17-a-disputed-ai-claim"
            scorecard = json.loads((pack / "scorecard.json").read_text(encoding="utf-8"))
            self.assertEqual(scorecard["rubric"], "claims-only")
            self.assertEqual(scorecard["dimensions"], {})
            self.assertIsNone(scorecard["weighted_score"])

    def test_comparison_pack_starts_with_a_shared_candidate_rubric(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            result = self.run_init(root, task_type="compare", topic="AI coding tools")

            self.assertEqual(result.returncode, 0, result.stderr)
            pack = root / "_research" / "2026-07-17-ai-coding-tools"
            scorecard = json.loads((pack / "scorecard.json").read_text(encoding="utf-8"))
            self.assertEqual(scorecard["rubric"], "comparison")
            self.assertEqual(sum(scorecard["candidate_dimensions"].values()), 100)
            self.assertEqual(scorecard["candidates"], [])
            self.assertIsNone(scorecard["weighted_score"])

    def test_rejects_a_non_iso_date_before_creating_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            result = subprocess.run(
                [
                    sys.executable,
                    str(INIT_SCRIPT),
                    "--root",
                    str(root),
                    "--topic",
                    "Unsafe topic",
                    "--task-type",
                    "github",
                    "--question",
                    "Question",
                    "--decision-goal",
                    "Goal",
                    "--date",
                    "../../escape",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "_research").exists())

    def test_rejects_multiline_frontmatter_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            result = self.run_init(root, topic="Unsafe\nstatus: decided")

            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "_research").exists())


class ValidateResearchPackTests(unittest.TestCase):
    def create_pack(
        self,
        root: Path,
        *,
        task_type: str = "github",
        topic: str = "Codex Dream Skin",
    ) -> Path:
        result = subprocess.run(
            [
                sys.executable,
                str(INIT_SCRIPT),
                "--root",
                str(root),
                "--topic",
                topic,
                "--task-type",
                task_type,
                "--question",
                "Is it worth trying?",
                "--decision-goal",
                "Choose Trial or Watch.",
                "--date",
                "2026-07-17",
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        slug = topic.lower().replace(" ", "-")
        return root / "_research" / f"2026-07-17-{slug}"

    def validate(self, pack: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATE_SCRIPT), str(pack)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_accepts_a_structurally_complete_collecting_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))

            result = self.validate(pack)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("valid", result.stdout.lower())

    def test_accepts_collecting_fact_check_without_a_project_score(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(
                Path(temp_dir), task_type="verify", topic="A disputed AI claim"
            )

            result = self.validate(pack)

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_collecting_comparison_with_no_candidates_yet(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(
                Path(temp_dir), task_type="compare", topic="AI coding tools"
            )

            result = self.validate(pack)

            self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_a_claim_with_an_unknown_source_id(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            claim = {
                "claim_id": "c1",
                "text": "The project is safe.",
                "importance": "high",
                "evidence_for": ["missing-source"],
                "evidence_against": [],
                "status": "supported",
                "confidence": "medium",
                "rationale": "README claim only.",
            }
            (pack / "claims.jsonl").write_text(json.dumps(claim) + "\n", encoding="utf-8")

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown source_id", result.stderr)

    def test_rejects_non_successful_sources_as_claim_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            source = {
                "source_id": "s1",
                "url": "https://example.com/blocked",
                "title": "Blocked source",
                "source_type": "web",
                "retrieved_at": "2026-07-17T12:00:00+08:00",
                "primary": False,
                "outcome": "blocked",
                "evidence_note": "The source could not be read.",
            }
            claim = {
                "claim_id": "c1",
                "text": "The blocked page proves the project is safe.",
                "importance": "high",
                "evidence_for": ["s1"],
                "evidence_against": [],
                "status": "supported",
                "confidence": "medium",
                "rationale": "Incorrectly treats missing coverage as evidence.",
            }
            (pack / "sources.jsonl").write_text(json.dumps(source) + "\n", encoding="utf-8")
            (pack / "claims.jsonl").write_text(json.dumps(claim) + "\n", encoding="utf-8")

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-successful source", result.stderr)

    def test_rejects_supported_claim_without_supporting_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            claim = {
                "claim_id": "c1",
                "text": "An unsupported conclusion.",
                "importance": "high",
                "evidence_for": [],
                "evidence_against": [],
                "status": "supported",
                "confidence": "medium",
                "rationale": "No source supplied.",
            }
            (pack / "claims.jsonl").write_text(json.dumps(claim) + "\n", encoding="utf-8")

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires evidence_for", result.stderr)

    def test_rejects_an_incorrect_weighted_score(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            scorecard_path = pack / "scorecard.json"
            scorecard = json.loads(scorecard_path.read_text(encoding="utf-8"))
            scorecard["weighted_score"] = 4.5
            scorecard_path.write_text(json.dumps(scorecard), encoding="utf-8")

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("weighted_score", result.stderr)

    def test_rejects_adopt_without_live_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            scorecard_path = pack / "scorecard.json"
            scorecard = json.loads(scorecard_path.read_text(encoding="utf-8"))
            for dimension in scorecard["dimensions"].values():
                dimension["score"] = 4
            scorecard["weighted_score"] = 4.0
            scorecard_path.write_text(json.dumps(scorecard), encoding="utf-8")
            brief_path = pack / "brief.md"
            brief_path.write_text(
                brief_path.read_text(encoding="utf-8").replace(
                    "status: collecting", "status: decided"
                ),
                encoding="utf-8",
            )
            decision_path = pack / "decision.md"
            decision_path.write_text(
                decision_path.read_text(encoding="utf-8")
                .replace("status: collecting", "status: decided")
                .replace("outcome: Unknown", "outcome: Adopt"),
                encoding="utf-8",
            )

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("live_verified", result.stderr)

    def test_rejects_approved_promotion_without_human_approval_record(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            decision_path = pack / "decision.md"
            decision_path.write_text(
                decision_path.read_text(encoding="utf-8").replace(
                    "promotion_status: not_requested", "promotion_status: approved"
                ),
                encoding="utf-8",
            )

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("approved_by", result.stderr)

    def test_rejects_secret_like_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            (pack / "decision.md").write_text(
                (pack / "decision.md").read_text(encoding="utf-8")
                + "\nLeaked token: ghp_abcdefghijklmnopqrstuvwxyz1234567890\n",
                encoding="utf-8",
            )

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("secret-like", result.stderr)

    def test_rejects_forbidden_raw_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            (pack / "raw").mkdir()

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("forbidden directory", result.stderr)

    def test_rejects_unexpected_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            (pack / "extra").mkdir()

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unexpected directory", result.stderr)

    def test_rejects_a_decided_pack_without_sources_or_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            brief_path = pack / "brief.md"
            brief_path.write_text(
                brief_path.read_text(encoding="utf-8").replace(
                    "status: collecting", "status: decided"
                ),
                encoding="utf-8",
            )
            decision_path = pack / "decision.md"
            decision_path.write_text(
                decision_path.read_text(encoding="utf-8")
                .replace("status: collecting", "status: decided")
                .replace("outcome: Unknown", "outcome: Watch"),
                encoding="utf-8",
            )

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("at least one source", result.stderr)

    def test_rejects_trial_with_a_high_severity_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(Path(temp_dir))
            source = {
                "source_id": "s1",
                "url": "https://example.com/source",
                "title": "Primary source",
                "source_type": "official_docs",
                "retrieved_at": "2026-07-17T12:00:00+08:00",
                "primary": True,
                "outcome": "success",
                "evidence_note": "Supports the project description.",
            }
            claim = {
                "claim_id": "c1",
                "text": "The project may be suitable for a trial.",
                "importance": "high",
                "evidence_for": ["s1"],
                "evidence_against": [],
                "status": "supported",
                "confidence": "medium",
                "rationale": "One primary source supports the claim.",
            }
            (pack / "sources.jsonl").write_text(json.dumps(source) + "\n", encoding="utf-8")
            (pack / "claims.jsonl").write_text(json.dumps(claim) + "\n", encoding="utf-8")
            scorecard_path = pack / "scorecard.json"
            scorecard = json.loads(scorecard_path.read_text(encoding="utf-8"))
            for dimension in scorecard["dimensions"].values():
                dimension["score"] = 4
                dimension["evidence_ids"] = ["s1"]
            scorecard["weighted_score"] = 4.0
            scorecard["blockers"] = [
                {
                    "id": "b1",
                    "severity": "high",
                    "summary": "Unresolved security risk.",
                    "evidence_ids": ["s1"],
                }
            ]
            scorecard_path.write_text(json.dumps(scorecard), encoding="utf-8")
            brief_path = pack / "brief.md"
            brief_path.write_text(
                brief_path.read_text(encoding="utf-8").replace(
                    "status: collecting", "status: decided"
                ),
                encoding="utf-8",
            )
            decision_path = pack / "decision.md"
            decision_path.write_text(
                decision_path.read_text(encoding="utf-8")
                .replace("status: collecting", "status: decided")
                .replace("outcome: Unknown", "outcome: Trial"),
                encoding="utf-8",
            )

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("high or critical blocker", result.stderr)

    def test_rejects_decided_comparison_with_fewer_than_two_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            pack = self.create_pack(
                Path(temp_dir), task_type="compare", topic="AI coding tools"
            )
            source = {
                "source_id": "s1",
                "url": "https://example.com/source",
                "title": "Primary source",
                "source_type": "official_docs",
                "retrieved_at": "2026-07-17T12:00:00+08:00",
                "primary": True,
                "outcome": "success",
                "evidence_note": "Describes one candidate.",
            }
            claim = {
                "claim_id": "c1",
                "text": "The comparison currently covers only one candidate.",
                "importance": "high",
                "evidence_for": ["s1"],
                "evidence_against": [],
                "status": "supported",
                "confidence": "high",
                "rationale": "The evidence set has only one candidate.",
            }
            (pack / "sources.jsonl").write_text(json.dumps(source) + "\n", encoding="utf-8")
            (pack / "claims.jsonl").write_text(json.dumps(claim) + "\n", encoding="utf-8")
            brief_path = pack / "brief.md"
            brief_path.write_text(
                brief_path.read_text(encoding="utf-8").replace(
                    "status: collecting", "status: decided"
                ),
                encoding="utf-8",
            )
            decision_path = pack / "decision.md"
            decision_path.write_text(
                decision_path.read_text(encoding="utf-8")
                .replace("status: collecting", "status: decided")
                .replace("outcome: Unknown", "outcome: Reference"),
                encoding="utf-8",
            )

            result = self.validate(pack)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("at least two candidates", result.stderr)


if __name__ == "__main__":
    unittest.main()
