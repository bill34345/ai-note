# GitHub evidence checklist

Use only the parts relevant to the decision, but do not infer them from stars or the README alone.

- Identity: canonical repository, owner, license, archived/fork status, intended audience.
- Fit: concrete user problem, supported platforms, expected frequency of use, better existing alternatives.
- Installation: documented steps, dependency manifests, account/API requirements, platform assumptions, uninstall path.
- Capability: trace key claims into source code, tests, examples, releases, or a live trial.
- Maintenance: recent commits and releases in context, issue/PR handling, bus factor, breaking changes.
- Security/privacy: permissions, shell execution, network calls, credential handling, telemetry, downloaded code, dependency risk.
- Cost: paid APIs, model/token cost, compute/storage, rate limits, lock-in.
- Reversibility: isolated trial, backup needs, files/configuration changed, clean removal.
- Evidence quality: primary evidence, independent user reports, known failures, and explicit coverage gaps.
- Durability: whether the result deserves a long-lived wiki page or should remain a dated research decision.

For live verification, record the actual environment, exact behavior tested, and observed outcome. Installation success alone is not capability proof.
