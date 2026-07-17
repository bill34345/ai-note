#!/usr/bin/env python3
"""Create a public-sanitized AI research pack without overwriting existing work."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path


TASK_TYPES = {"github", "paper", "product", "verify", "compare", "discover"}
GITHUB_DIMENSIONS = {
    "relevance": 15,
    "usability": 15,
    "maturity": 10,
    "maintenance": 10,
    "evidence": 15,
    "security_privacy": 15,
    "cost_dependencies": 5,
    "reversibility": 5,
    "knowledge_durability": 10,
}
GENERAL_DIMENSIONS = {
    "relevance": 20,
    "authority": 20,
    "directness": 20,
    "independent_support": 15,
    "freshness": 10,
    "reproducibility": 15,
}
ASSETS = Path(__file__).resolve().parents[1] / "assets"


def slugify(topic: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    if slug:
        return slug[:72].rstrip("-")
    digest = hashlib.sha256(topic.encode("utf-8")).hexdigest()[:8]
    return f"research-{digest}"


def scorecard(task_type: str, topic: str) -> dict[str, object]:
    if task_type == "verify":
        return {
            "schema_version": 1,
            "rubric": "claims-only",
            "subject": topic,
            "dimensions": {},
            "blockers": [],
            "weighted_score": None,
        }
    if task_type == "compare":
        return {
            "schema_version": 1,
            "rubric": "comparison",
            "subject": topic,
            "candidate_dimensions": GENERAL_DIMENSIONS,
            "candidates": [],
            "blockers": [],
            "weighted_score": None,
        }
    rubric = "github" if task_type == "github" else "general"
    weights = GITHUB_DIMENSIONS if rubric == "github" else GENERAL_DIMENSIONS
    dimensions = {
        name: {
            "score": 0,
            "weight": weight,
            "rationale": "Not researched yet.",
            "evidence_ids": [],
        }
        for name, weight in weights.items()
    }
    return {
        "schema_version": 1,
        "rubric": rubric,
        "subject": topic,
        "dimensions": dimensions,
        "blockers": [],
        "weighted_score": 0.0,
    }


def iso_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD")
    return value


def single_line(value: str) -> str:
    if "\n" in value or "\r" in value:
        raise argparse.ArgumentTypeError("value must be a single line")
    return value


def update_index(root: Path, pack_id: str, topic: str, task_type: str) -> None:
    index_path = root / "_research" / "index.md"
    if not index_path.exists():
        index_path.write_text(
            "# Research index\n\n"
            "Public-sanitized research packs. A decision is not wiki promotion approval.\n\n"
            "| ID | Topic | Type | Status | Decision |\n"
            "| --- | --- | --- | --- | --- |\n",
            encoding="utf-8",
        )
    safe_topic = topic.replace("|", "\\|").replace("\n", " ")
    with index_path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(
            f"| [{pack_id}](./{pack_id}/decision.md) | {safe_topic} | "
            f"{task_type} | collecting | Unknown |\n"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--topic", required=True, type=single_line)
    parser.add_argument("--task-type", required=True, choices=sorted(TASK_TYPES))
    parser.add_argument("--question", required=True)
    parser.add_argument("--decision-goal", required=True)
    parser.add_argument("--date", type=iso_date, default=date.today().isoformat())
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pack_id = f"{args.date}-{slugify(args.topic)}"
    pack = args.root.resolve() / "_research" / pack_id
    if pack.exists():
        print(f"Research pack already exists: {pack}", file=sys.stderr)
        return 2

    pack.mkdir(parents=True)
    brief_template = (ASSETS / "brief.md.tmpl").read_text(encoding="utf-8")
    (pack / "brief.md").write_text(
        brief_template.format(
            pack_id=pack_id,
            topic=args.topic,
            task_type=args.task_type,
            created=args.date,
            question=args.question,
            decision_goal=args.decision_goal,
        ),
        encoding="utf-8",
    )
    (pack / "sources.jsonl").write_text("", encoding="utf-8")
    (pack / "claims.jsonl").write_text("", encoding="utf-8")
    (pack / "scorecard.json").write_text(
        json.dumps(scorecard(args.task_type, args.topic), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (pack / "decision.md").write_text(
        (ASSETS / "decision.md.tmpl").read_text(encoding="utf-8"), encoding="utf-8"
    )
    update_index(args.root.resolve(), pack_id, args.topic, args.task_type)
    print(pack)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
