#!/usr/bin/env python3
"""Validate structure, evidence links, scoring, decisions, and public safety."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


EXPECTED_FILES = {
    "brief.md",
    "sources.jsonl",
    "claims.jsonl",
    "scorecard.json",
    "decision.md",
}
FORBIDDEN_DIRS = {"raw", "downloads", "cache"}
SOURCE_OUTCOMES = {"success", "no_result", "failed", "blocked"}
CLAIM_STATUSES = {"confirmed", "supported", "contested", "unverified", "refuted"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
DECISION_STATUSES = {"collecting", "auditing", "decided", "closed"}
PROJECT_OUTCOMES = {"Adopt", "Trial", "Watch", "Reference", "Reject", "Unknown"}
CLAIM_DECISION_OUTCOMES = {
    "Confirmed",
    "Supported",
    "Contested",
    "Unverified",
    "Refuted",
    "Unknown",
}
PROMOTION_STATUSES = {"not_requested", "candidate", "approved", "promoted", "rejected"}
SECRET_PATTERNS = {
    "OpenAI-like API key": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub token": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    "GitHub fine-grained token": re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    "assigned API secret": re.compile(
        r"(?im)^\s*(?:ANYSEARCH_API_KEY|OPENAI_API_KEY|GITHUB_TOKEN)\s*[:=]\s*(?!<|\$\{|REDACTED)[^\s]+"
    ),
    "private Windows user path": re.compile(r"(?i)\b[A-Z]:\\Users\\(?!<)[^\\\s]+"),
}


class ValidationError(Exception):
    pass


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValidationError(f"{path.name}: missing frontmatter")
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line == "---":
            return result
        if ":" not in line:
            raise ValidationError(f"{path.name}: invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    raise ValidationError(f"{path.name}: unterminated frontmatter")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{path.name}:{line_number}: invalid JSON: {exc.msg}") from exc
        if not isinstance(value, dict):
            raise ValidationError(f"{path.name}:{line_number}: record must be an object")
        records.append(value)
    return records


def require_fields(record: dict[str, Any], fields: set[str], context: str) -> None:
    missing = sorted(field for field in fields if field not in record)
    if missing:
        raise ValidationError(f"{context}: missing fields: {', '.join(missing)}")


def validate_sources(records: list[dict[str, Any]]) -> tuple[set[str], set[str]]:
    required = {
        "source_id",
        "url",
        "title",
        "source_type",
        "retrieved_at",
        "primary",
        "outcome",
        "evidence_note",
    }
    source_ids: set[str] = set()
    successful_source_ids: set[str] = set()
    for index, source in enumerate(records, start=1):
        context = f"sources.jsonl:{index}"
        require_fields(source, required, context)
        source_id = source["source_id"]
        if not isinstance(source_id, str) or not source_id:
            raise ValidationError(f"{context}: source_id must be a non-empty string")
        if source_id in source_ids:
            raise ValidationError(f"{context}: duplicate source_id {source_id}")
        if source["outcome"] not in SOURCE_OUTCOMES:
            raise ValidationError(f"{context}: invalid outcome {source['outcome']}")
        if not isinstance(source["primary"], bool):
            raise ValidationError(f"{context}: primary must be boolean")
        source_ids.add(source_id)
        if source["outcome"] == "success":
            successful_source_ids.add(source_id)
    return source_ids, successful_source_ids


def validate_evidence_ids(
    ids: Any,
    source_ids: set[str],
    context: str,
    successful_source_ids: set[str] | None = None,
) -> None:
    if not isinstance(ids, list) or not all(isinstance(item, str) for item in ids):
        raise ValidationError(f"{context}: evidence IDs must be a string array")
    unknown = sorted(set(ids) - source_ids)
    if unknown:
        raise ValidationError(f"{context}: unknown source_id: {', '.join(unknown)}")
    if successful_source_ids is not None:
        unusable = sorted(set(ids) - successful_source_ids)
        if unusable:
            raise ValidationError(
                f"{context}: non-successful source cannot be used as evidence: {', '.join(unusable)}"
            )


def validate_claims(
    records: list[dict[str, Any]],
    source_ids: set[str],
    successful_source_ids: set[str],
) -> None:
    required = {
        "claim_id",
        "text",
        "importance",
        "evidence_for",
        "evidence_against",
        "status",
        "confidence",
        "rationale",
    }
    claim_ids: set[str] = set()
    for index, claim in enumerate(records, start=1):
        context = f"claims.jsonl:{index}"
        require_fields(claim, required, context)
        claim_id = claim["claim_id"]
        if not isinstance(claim_id, str) or not claim_id:
            raise ValidationError(f"{context}: claim_id must be a non-empty string")
        if claim_id in claim_ids:
            raise ValidationError(f"{context}: duplicate claim_id {claim_id}")
        if claim["status"] not in CLAIM_STATUSES:
            raise ValidationError(f"{context}: invalid status {claim['status']}")
        if claim["confidence"] not in CONFIDENCE_LEVELS:
            raise ValidationError(f"{context}: invalid confidence {claim['confidence']}")
        validate_evidence_ids(
            claim["evidence_for"],
            source_ids,
            f"{context}.evidence_for",
            successful_source_ids,
        )
        validate_evidence_ids(
            claim["evidence_against"],
            source_ids,
            f"{context}.evidence_against",
            successful_source_ids,
        )
        if claim["status"] in {"confirmed", "supported"} and not claim["evidence_for"]:
            raise ValidationError(f"{context}: {claim['status']} claim requires evidence_for")
        if claim["status"] == "refuted" and not claim["evidence_against"]:
            raise ValidationError(f"{context}: refuted claim requires evidence_against")
        claim_ids.add(claim_id)


def validate_blockers(
    blockers: Any, source_ids: set[str], successful_source_ids: set[str]
) -> list[dict[str, Any]]:
    if not isinstance(blockers, list):
        raise ValidationError("scorecard.json: blockers must be an array")
    for index, blocker in enumerate(blockers, start=1):
        context = f"scorecard.json.blockers:{index}"
        if not isinstance(blocker, dict):
            raise ValidationError(f"{context}: blocker must be an object")
        require_fields(blocker, {"id", "severity", "summary", "evidence_ids"}, context)
        if blocker["severity"] not in {"low", "medium", "high", "critical"}:
            raise ValidationError(f"{context}: invalid severity {blocker['severity']}")
        validate_evidence_ids(
            blocker["evidence_ids"],
            source_ids,
            f"{context}.evidence_ids",
            successful_source_ids,
        )
    return blockers


def validate_dimensions(
    dimensions: Any,
    source_ids: set[str],
    successful_source_ids: set[str],
    *,
    context_prefix: str,
    expected_weights: dict[str, float] | None = None,
) -> float:
    if not isinstance(dimensions, dict) or not dimensions:
        raise ValidationError(f"{context_prefix}: dimensions must be a non-empty object")
    if expected_weights is not None and set(dimensions) != set(expected_weights):
        raise ValidationError(f"{context_prefix}: candidate dimensions must match shared rubric")
    total_weight = 0.0
    weighted_total = 0.0
    for name, dimension in dimensions.items():
        context = f"{context_prefix}.{name}"
        if not isinstance(dimension, dict):
            raise ValidationError(f"{context}: dimension must be an object")
        required = {"score", "rationale", "evidence_ids"}
        if expected_weights is None:
            required.add("weight")
        require_fields(dimension, required, context)
        score = dimension["score"]
        weight = expected_weights[name] if expected_weights is not None else dimension["weight"]
        if not isinstance(score, (int, float)) or isinstance(score, bool) or not 0 <= score <= 5:
            raise ValidationError(f"{context}: score must be between 0 and 5")
        if not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0:
            raise ValidationError(f"{context}: weight must be positive")
        validate_evidence_ids(
            dimension["evidence_ids"],
            source_ids,
            f"{context}.evidence_ids",
            successful_source_ids,
        )
        total_weight += float(weight)
        weighted_total += float(score) * float(weight)
    if not math.isclose(total_weight, 100.0, abs_tol=0.001):
        raise ValidationError(f"{context_prefix}: dimension weights sum to {total_weight}, expected 100")
    return round(weighted_total / 100.0, 2)


def validate_scorecard(
    path: Path,
    source_ids: set[str],
    successful_source_ids: set[str],
    task_type: str,
) -> tuple[float | None, list[dict[str, Any]], int]:
    try:
        scorecard = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"scorecard.json: invalid JSON: {exc.msg}") from exc
    if not isinstance(scorecard, dict):
        raise ValidationError("scorecard.json: root must be an object")
    require_fields(scorecard, {"schema_version", "rubric", "subject", "blockers", "weighted_score"}, "scorecard.json")
    if scorecard["schema_version"] != 1:
        raise ValidationError("scorecard.json: schema_version must be 1")
    expected_rubric = {
        "github": "github",
        "verify": "claims-only",
        "compare": "comparison",
    }.get(task_type, "general")
    if scorecard["rubric"] != expected_rubric:
        raise ValidationError(
            f"scorecard.json: task_type {task_type} requires rubric {expected_rubric}"
        )
    blockers = validate_blockers(scorecard["blockers"], source_ids, successful_source_ids)
    if expected_rubric == "claims-only":
        require_fields(scorecard, {"dimensions"}, "scorecard.json")
        if scorecard["dimensions"] != {} or scorecard["weighted_score"] is not None:
            raise ValidationError("scorecard.json: claims-only research must not have a project score")
        return None, blockers, 0
    if expected_rubric == "comparison":
        require_fields(scorecard, {"candidate_dimensions", "candidates"}, "scorecard.json")
        weights = scorecard["candidate_dimensions"]
        if not isinstance(weights, dict) or not weights:
            raise ValidationError("scorecard.json: candidate_dimensions must be a non-empty object")
        if any(
            not isinstance(weight, (int, float)) or isinstance(weight, bool) or weight <= 0
            for weight in weights.values()
        ):
            raise ValidationError("scorecard.json: candidate dimension weights must be positive")
        if not math.isclose(sum(float(weight) for weight in weights.values()), 100.0, abs_tol=0.001):
            raise ValidationError("scorecard.json: candidate dimension weights must sum to 100")
        if scorecard["weighted_score"] is not None:
            raise ValidationError("scorecard.json: comparison must not have one project score")
        candidates = scorecard["candidates"]
        if not isinstance(candidates, list):
            raise ValidationError("scorecard.json: candidates must be an array")
        names: set[str] = set()
        for index, candidate in enumerate(candidates, start=1):
            context = f"scorecard.json.candidates:{index}"
            if not isinstance(candidate, dict):
                raise ValidationError(f"{context}: candidate must be an object")
            require_fields(candidate, {"name", "dimensions", "weighted_score"}, context)
            if not isinstance(candidate["name"], str) or not candidate["name"].strip():
                raise ValidationError(f"{context}: name must be a non-empty string")
            if candidate["name"] in names:
                raise ValidationError(f"{context}: duplicate candidate name {candidate['name']}")
            calculated = validate_dimensions(
                candidate["dimensions"],
                source_ids,
                successful_source_ids,
                context_prefix=f"{context}.dimensions",
                expected_weights=weights,
            )
            recorded = candidate["weighted_score"]
            if not isinstance(recorded, (int, float)) or isinstance(recorded, bool):
                raise ValidationError(f"{context}: weighted_score must be numeric")
            if not math.isclose(float(recorded), calculated, abs_tol=0.001):
                raise ValidationError(
                    f"{context}: weighted_score is {recorded}, calculated value is {calculated}"
                )
            names.add(candidate["name"])
        return None, blockers, len(candidates)
    require_fields(scorecard, {"dimensions"}, "scorecard.json")
    calculated = validate_dimensions(
        scorecard["dimensions"],
        source_ids,
        successful_source_ids,
        context_prefix="scorecard.json.dimensions",
    )
    recorded = scorecard["weighted_score"]
    if not isinstance(recorded, (int, float)) or isinstance(recorded, bool):
        raise ValidationError("scorecard.json: weighted_score must be numeric")
    if not math.isclose(float(recorded), calculated, abs_tol=0.001):
        raise ValidationError(
            f"scorecard.json: weighted_score is {recorded}, calculated value is {calculated}"
        )
    return calculated, blockers, 0


def as_bool(value: str, context: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise ValidationError(f"{context}: expected true or false")


def validate_decision(
    path: Path,
    score: float | None,
    blockers: list[dict[str, Any]],
    brief_status: str,
    source_count: int,
    claim_count: int,
    task_type: str,
    candidate_count: int,
) -> None:
    decision = parse_frontmatter(path)
    require_fields(
        decision,
        {
            "status",
            "outcome",
            "live_verified",
            "promotion_status",
            "approved_by",
            "approved_at",
        },
        "decision.md",
    )
    if decision["status"] not in DECISION_STATUSES:
        raise ValidationError(f"decision.md: invalid status {decision['status']}")
    if decision["status"] != brief_status:
        raise ValidationError("decision.md: status must match brief.md status")
    allowed_outcomes = CLAIM_DECISION_OUTCOMES if task_type == "verify" else PROJECT_OUTCOMES
    if decision["outcome"] not in allowed_outcomes:
        raise ValidationError(f"decision.md: invalid outcome {decision['outcome']}")
    live_verified = as_bool(decision["live_verified"], "decision.md.live_verified")
    if decision["promotion_status"] not in PROMOTION_STATUSES:
        raise ValidationError(
            f"decision.md: invalid promotion_status {decision['promotion_status']}"
        )
    if task_type == "github" and decision["outcome"] == "Adopt":
        assert score is not None
        if score < 4.0:
            raise ValidationError("decision.md: Adopt requires weighted_score >= 4.0")
        if not live_verified:
            raise ValidationError("decision.md: Adopt requires live_verified: true")
        if blockers:
            raise ValidationError("decision.md: Adopt is not allowed while blockers remain")
    if task_type == "github" and decision["outcome"] == "Trial" and score is not None and score < 3.2:
        raise ValidationError("decision.md: Trial requires weighted_score >= 3.2")
    if task_type == "github" and decision["outcome"] == "Trial" and any(
        blocker["severity"] in {"high", "critical"} for blocker in blockers
    ):
        raise ValidationError("decision.md: Trial is not allowed with a high or critical blocker")
    if decision["status"] in {"decided", "closed"}:
        if source_count == 0:
            raise ValidationError("decision.md: decided research requires at least one source")
        if claim_count == 0:
            raise ValidationError("decision.md: decided research requires at least one claim")
        if task_type == "compare" and candidate_count < 2:
            raise ValidationError("decision.md: decided comparison requires at least two candidates")
    if decision["promotion_status"] in {"approved", "promoted"}:
        if not decision["approved_by"]:
            raise ValidationError("decision.md: approved_by is required for approved promotion")
        if not decision["approved_at"]:
            raise ValidationError("decision.md: approved_at is required for approved promotion")
        if decision["status"] not in {"decided", "closed"}:
            raise ValidationError("decision.md: promotion requires a decided or closed research pack")


def scan_public_safety(pack: Path) -> None:
    forbidden = [
        path
        for path in pack.rglob("*")
        if path.is_dir() and path.name.lower() in FORBIDDEN_DIRS
    ]
    if forbidden:
        raise ValidationError(f"forbidden directory in public research pack: {forbidden[0].name}")
    for path in pack.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError(f"{path.name}: research pack files must be UTF-8 text") from exc
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                raise ValidationError(f"{path.name}: secret-like content detected ({label})")


def validate_pack(pack: Path) -> None:
    if not pack.is_dir():
        raise ValidationError(f"research pack directory not found: {pack}")
    files = {path.name for path in pack.iterdir() if path.is_file()}
    missing = sorted(EXPECTED_FILES - files)
    unexpected = sorted(files - EXPECTED_FILES)
    if missing:
        raise ValidationError(f"research pack missing files: {', '.join(missing)}")
    if unexpected:
        raise ValidationError(f"research pack has unexpected files: {', '.join(unexpected)}")
    brief = parse_frontmatter(pack / "brief.md")
    require_fields(
        brief,
        {"id", "topic", "task_type", "status", "visibility", "created"},
        "brief.md",
    )
    if brief["task_type"] not in {"github", "paper", "product", "verify", "compare", "discover"}:
        raise ValidationError(f"brief.md: invalid task_type {brief['task_type']}")
    if brief["visibility"] != "public-sanitized":
        raise ValidationError("brief.md: visibility must be public-sanitized")
    if brief["status"] not in DECISION_STATUSES:
        raise ValidationError(f"brief.md: invalid status {brief['status']}")
    scan_public_safety(pack)
    directories = sorted(path.name for path in pack.iterdir() if path.is_dir())
    if directories:
        raise ValidationError(
            f"research pack has unexpected directory: {', '.join(directories)}"
        )
    sources = load_jsonl(pack / "sources.jsonl")
    source_ids, successful_source_ids = validate_sources(sources)
    claims = load_jsonl(pack / "claims.jsonl")
    validate_claims(claims, source_ids, successful_source_ids)
    score, blockers, candidate_count = validate_scorecard(
        pack / "scorecard.json",
        source_ids,
        successful_source_ids,
        brief["task_type"],
    )
    validate_decision(
        pack / "decision.md",
        score,
        blockers,
        brief["status"],
        len(sources),
        len(claims),
        brief["task_type"],
        candidate_count,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        validate_pack(args.pack.resolve())
    except ValidationError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(f"VALID: {args.pack}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
