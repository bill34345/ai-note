# AI-wiki repository instructions

## Research Desk

- For requests to research, search, compare, score, verify, or recommend AI-related projects, products, papers, claims, or trends, use the repository skill `$ai-research`.
- Read `references/research-config.md` before beginning research. It is the repository source of truth for task routing, evidence quality, scoring, decisions, public-safety rules, and promotion gates.
- Store reusable research evidence under `_research/<YYYY-MM-DD>-<slug>/`. Keep the five sanitized artifacts (`brief.md`, `sources.jsonl`, `claims.jsonl`, `scorecard.json`, and `decision.md`) reviewable and tracked.
- Prefer AnySearch when it is installed and supports the source. If it is unavailable or inadequate, state the reason before using a fallback. Use official documentation, repositories, releases, source code, or papers for decisive factual claims.
- Record failed, blocked, and zero-result source attempts. A failed source is missing coverage, not negative evidence.
- Treat README statements, popularity, stars, downloads, and social engagement as signals, not proof of quality or live compatibility.

## Wiki promotion gate

- Research and wiki ingestion are separate phases. Never create or modify `_staging/`, `concepts/`, `entities/`, `skills/`, `references/`, or `synthesis/` pages merely because research finished.
- Promotion requires an explicit user decision plus `promotion_status: approved` or `promoted`, a non-empty `approved_by`, and `approved_at` in the research pack's `decision.md`.
- Before promotion, explain why the result is durable enough for the wiki. One-time utilities, transient news, and weakly evidenced projects normally remain in `_research/` with a `Watch`, `Reference`, `Reject`, or `Unknown` result.

## Acceptance and public safety

- Distinguish mechanical validation from semantic acceptance. A passing validator proves structure and consistency; it does not prove that the evidence supports the conclusion.
- Read the final decision and sample its linked sources before calling research complete. State remaining coverage gaps, conflicts, and unverified environment claims.
- This is a public repository. Do not store credentials, cookies, private URLs, personal data, machine-specific user paths, copyrighted bulk content, or raw downloads in tracked research artifacts.
- Do not overwrite an existing research pack. Start a new dated pack when the question or evidence materially changes.
