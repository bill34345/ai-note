# Research pack schema and editing guide

Read the repository's `references/research-config.md` first. This reference gives the exact record shapes used by the validator.

## Source record

One compact JSON object per line in `sources.jsonl`:

```json
{"source_id":"s1","url":"https://example.com/primary","title":"Primary source","source_type":"official_docs","retrieved_at":"2026-07-17T12:00:00+08:00","primary":true,"outcome":"success","evidence_note":"What this source can and cannot establish."}
```

Keep unsuccessful attempts too. Use `no_result`, `failed`, or `blocked`; do not cite them as supporting evidence.

## Claim record

One compact JSON object per line in `claims.jsonl`:

```json
{"claim_id":"c1","text":"A bounded, testable claim.","importance":"high","evidence_for":["s1"],"evidence_against":[],"status":"supported","confidence":"medium","rationale":"Why the cited evidence warrants this status and what remains unknown."}
```

Allowed claim statuses: `confirmed`, `supported`, `contested`, `unverified`, `refuted`. Allowed confidence: `low`, `medium`, `high`.

## Scorecards

- `github`: edit each existing dimension's `score`, `rationale`, and `evidence_ids`, then recompute `weighted_score`.
- `general`: use the same procedure with the six evidence dimensions.
- `claims-only`: leave `dimensions` empty and `weighted_score` null. The conclusion comes from claim statuses.
- `comparison`: keep `candidate_dimensions` unchanged. Add at least two candidate objects; each uses every shared dimension and its own `weighted_score`. Candidate dimensions contain `score`, `rationale`, and `evidence_ids`; weights stay at the shared top level.

A blocker has `id`, `severity` (`low`, `medium`, `high`, or `critical`), `summary`, and `evidence_ids`.

## Finalization

Set both `brief.md` and `decision.md` to the same lifecycle status. A `decided` or `closed` pack needs at least one source and one claim; a decided comparison needs at least two candidates. Update the matching row in `_research/index.md` after changing status or outcome.

Run:

```powershell
python .agents/skills/ai-research/scripts/validate_research_pack.py _research/<pack-id>
```

Then read `decision.md` and sample the cited evidence. Passing the script is mechanical validation only.
