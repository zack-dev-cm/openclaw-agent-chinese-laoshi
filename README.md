# OpenClaw Chinese Laoshi

Public OpenClaw plugin and skill bundle for a pilot-first Chinese lesson
normalization and tutor workflow.

[ClawHub](https://clawhub.ai/zack-dev-cm/openclaw-agent-chinese-laoshi) publishes
the installable skill. GitHub keeps the public source bundle and release tags.

## Included Surfaces

- Codex plugin: `plugins/openclaw-chinese-laoshi`
- OpenClaw skill: `skills/openclaw-chinese-laoshi-ops`
- Publication gate: `scripts/check_publication_bundle.py`

## What It Does

- normalizes transcript/subtitle inputs into grounded raw transcripts
- builds lesson JSON and learner-facing Markdown
- builds local export bundles without assuming cloud credentials
- enforces pilot-first review before scaling
- blocks publication when the bundle contains slop, local-path bleed, or
  secret-shaped text

## Safe Publishing Rule

Do not publish directly from an internal working repo. Build this sanitized
bundle first, then run the gate from a clean public checkout:

```bash
python3 scripts/check_publication_bundle.py
```

## Push Target

The public repository is:

```text
https://github.com/zack-dev-cm/openclaw-agent-chinese-laoshi
```

## ClawHub

After the gate passes and the repository is pushed publicly, publish the skill
with:

```bash
clawhub publish ./skills/openclaw-chinese-laoshi-ops --slug openclaw-agent-chinese-laoshi --name "OpenClaw Chinese Laoshi Ops" --version <semver> --changelog "<text>" --tags latest,chinese,language-learning,drive
```

Published page: https://clawhub.ai/zack-dev-cm/openclaw-agent-chinese-laoshi

Current clean release: `v1.0.9` / `1.0.9`

Reference:

- https://docs.openclaw.ai/tools/clawhub
