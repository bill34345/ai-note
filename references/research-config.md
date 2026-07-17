# AI Research Desk configuration

This file is the repository source of truth for `$ai-research`. Research packs are public-sanitized evidence ledgers; they are not automatically wiki pages.

## Task routing

| Task type | Use for | Score model | Normal output |
| --- | --- | --- | --- |
| `github` | One GitHub repository or code project | GitHub 9-dimension rubric | `Adopt`, `Trial`, `Watch`, `Reference`, `Reject`, or `Unknown` |
| `paper` | A paper, benchmark, or technical report | General evidence rubric | Evidence-backed conclusion with limits |
| `product` | A product, service, model, or tool | General evidence rubric | Evidence-backed conclusion with limits |
| `verify` | A factual claim or contested statement | Claims only; no project total | `Confirmed`, `Supported`, `Contested`, `Unverified`, `Refuted`, or `Unknown` |
| `compare` | Two or more candidates | One shared general rubric for every candidate | Comparable candidate scores plus trade-offs |
| `discover` | Landscape scan or candidate search | General evidence rubric | Shortlist and next research questions |

## Evidence policy

1. Define the question, decision goal, scope, and completion criteria before searching.
2. Prefer primary sources: official docs, repository files, releases, source code, papers, standards, and first-party statements.
3. Seek at least one independent source for high-importance claims when one reasonably exists.
4. Keep source retrieval outcome as `success`, `no_result`, `failed`, or `blocked`. Only `success` can support or oppose a claim; `no_result` is not proof of absence.
5. Separate observations from inferences. Every claim links to evidence for and against it and ends as `confirmed`, `supported`, `contested`, `unverified`, or `refuted`.
6. Search specifically for counter-evidence, unresolved issues, abandoned maintenance, security/privacy risk, hidden cost, and compatibility limits.
7. Record retrieval dates and recheck conditions for facts likely to change.

AnySearch is the preferred general search backend when installed. Use source-native or official tools when they provide better evidence. Disclose tool/source coverage failures before falling back.

## GitHub project rubric

Score each dimension from 0 to 5 and cite source IDs in the rationale.

| Dimension | Weight | Question |
| --- | ---: | --- |
| Relevance | 15 | Does it solve the user's real problem? |
| Usability | 15 | Can the intended user install, understand, and operate it? |
| Maturity | 10 | Is the implementation coherent beyond a demo or claim? |
| Maintenance | 10 | Are releases, commits, issues, and ownership healthy enough? |
| Evidence | 15 | Are important claims supported by primary and independent evidence? |
| Security and privacy | 15 | Are permissions, data handling, dependencies, and attack surface acceptable? |
| Cost and dependencies | 5 | Are monetary, compute, account, and ecosystem costs explicit and acceptable? |
| Reversibility | 5 | Can it be trialed and removed without costly lock-in or damage? |
| Knowledge durability | 10 | Will the result remain useful enough to justify durable wiki knowledge? |

Weighted score is `sum(score × weight) / 100`. It is decision support, not an automatic verdict.

- `Adopt`: score at least 4.0, live verification passed, and no blocker remains.
- `Trial`: score at least 3.2 and no high/critical blocker remains.
- `Watch`: promising but immature, low-frequency, or not currently needed.
- `Reference`: useful as a pattern or reference, but not something to operate now.
- `Reject`: current evidence shows a poor fit or unacceptable risk.
- `Unknown`: evidence or coverage is insufficient.

An unresolved blocker overrides the numeric score. A one-time or rarely reused utility can be worth researching without being worth promoting to the wiki.

## General evidence rubric

Score relevance 20, authority 20, directness 20, independent support 15, freshness 10, and reproducibility 15. Comparisons must use exactly this same set and weights for every candidate. Fact-checks do not use this total.

## Public research pack contract

Each `_research/<YYYY-MM-DD>-<slug>/` contains exactly:

- `brief.md`: question, scope, task type, status, and completion criteria;
- `sources.jsonl`: source inventory and retrieval outcomes;
- `claims.jsonl`: auditable claim/evidence graph;
- `scorecard.json`: task-appropriate scoring or claims-only marker;
- `decision.md`: conclusion, counter-evidence, mechanical checks, semantic acceptance, recheck conditions, and promotion record.

Allowed lifecycle statuses are `collecting`, `auditing`, `decided`, and `closed`. Files must remain UTF-8 and public-sanitized. Raw pages, downloads, caches, and temporary files belong only in ignored local directories and never justify a conclusion unless their sanitized evidence is recorded.

## Promotion gate

Finishing research does not authorize wiki writes. Promotion requires all of the following:

1. the user explicitly approves promotion;
2. `decision.md` records `promotion_status: approved` or `promoted`, plus `approved_by` and `approved_at`;
3. the pack is `decided` or `closed` and passes structural validation;
4. semantic review confirms that the proposed wiki knowledge is durable, source-traceable, and not merely transient news or a one-use utility.

Only after those conditions may a separate wiki workflow create `_staging/` pages. Human review remains required before final promotion.
