# Evals

`evals.json` is the maintained eval set for this skill; its `version` tracks `SKILL.md`. There is no automated runner: each eval is a prompt plus an assertion checklist, verified manually or by an agent, assertion by assertion.

Historical upstream snapshots are project records under `management/upstream/evals/`; they are intentionally excluded from the runtime skill and install package. To rerun an eval round, use `evals.json` with a fresh session and store dated evidence in the project management area rather than this runtime directory.
