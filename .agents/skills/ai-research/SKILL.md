---
name: ai-research
description: Research, search, fact-check, compare, score, and reach evidence-backed decisions about AI-related GitHub repositories, products, papers, claims, and trends. Use when the user wants to understand whether something is useful, trustworthy, worth trying, worth watching, or durable enough for the AI wiki.
---

# AI Research Desk

Create a public-sanitized evidence ledger before proposing durable wiki knowledge. Keep research, operational adoption, and wiki promotion as separate decisions.

## Start

1. Read repository `references/research-config.md` completely.
2. Read [references/research-pack-schema.md](references/research-pack-schema.md). For a GitHub project, also read [references/github-audit.md](references/github-audit.md).
3. Classify the request as `github`, `paper`, `product`, `verify`, `compare`, or `discover`.
4. Restate the research question, decision goal, scope, and semantic completion criteria. Ask only if a missing choice would materially change the research.
5. Initialize a pack from the repository root:

```powershell
python .agents/skills/ai-research/scripts/init_research_pack.py --topic "<topic>" --task-type <type> --question "<question>" --decision-goal "<goal>"
```

Never overwrite an existing pack.

## Research

1. Build a query plan that covers identity, primary facts, practical use, counter-evidence, current state, risk, and alternatives.
2. Prefer AnySearch when available. Use official or source-native evidence for decisive claims. If a source or tool fails, record its true outcome and disclose the coverage gap before fallback.
3. Add every material source attempt to `sources.jsonl`. Add bounded claims to `claims.jsonl`, including evidence against and uncertainty.
4. For GitHub work, inspect the repository beyond the README and apply the nine-dimension rubric. Do not convert popularity into quality.
5. For comparisons, apply every shared dimension to every candidate. For fact-checks, classify claims only and do not invent a total project score.
6. Seek disconfirming evidence before concluding. Mark unresolved risks as blockers.

## Decide

1. Fill the scorecard according to the task type. Recalculate weighted scores from the recorded dimensions.
2. Write `decision.md` so the evidence summary, counter-evidence, open questions, recheck conditions, and recommendation can be audited without the chat transcript.
3. Separate repository/project claims from live verification. `Adopt` requires a relevant end-to-end live check; installation or a successful command alone is insufficient.
4. Set matching lifecycle status in `brief.md` and `decision.md`; normally use `decided` when the question is answered with current evidence.
5. Update that pack's row in `_research/index.md` to match the final status and outcome.

## Validate and accept

Run the structural validator:

```powershell
python .agents/skills/ai-research/scripts/validate_research_pack.py _research/<pack-id>
```

Then perform semantic acceptance: read the final decision, sample high-importance claims against their sources, verify that counter-evidence affected the conclusion, and confirm that coverage limitations are explicit. Report mechanical validation and semantic acceptance separately.

## Promotion boundary

Stop after the research decision unless the user explicitly approves wiki promotion. Do not write `_staging/` or durable wiki pages automatically. If promotion is approved, record `promotion_status`, `approved_by`, and `approved_at` in `decision.md`, validate again, and hand off to a separate wiki workflow.
