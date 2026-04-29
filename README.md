# OpenClaw Chinese Laoshi

Public OpenClaw plugin and skill bundle for a pilot-first Chinese lesson
normalization and tutor workflow.

[ClawHub](https://clawhub.ai/zack-dev-cm/openclaw-agent-chinese-laoshi) publishes
the installable skill. GitHub keeps the public source bundle and release tags.

## Included Surfaces

- Codex plugin: `plugins/openclaw-chinese-laoshi`
- OpenClaw skill: `skills/openclaw-chinese-laoshi-ops`
- Bundled public course data: `skills/openclaw-chinese-laoshi-ops/references/course-data`
- Public system prompts: `prompts/system`
- Published skill prompt mirror: `skills/openclaw-chinese-laoshi-ops/references/system-prompts`
- ChatGPT connector guidance: `skills/openclaw-chinese-laoshi-ops/references/chatgpt-connector-guidance.md`
- Publication gate: `scripts/check_publication_bundle.py`

## What It Does

- normalizes transcript/subtitle inputs into grounded raw transcripts
- builds lesson JSON and learner-facing Markdown
- ships sanitized lesson, lesson-plan, HSK practice, and roleplay data for the
  installable skill
- publishes tutor prompt packs with a shared correction, pacing, pinyin, and
  instruction-bleed contract
- guides ChatGPT/GitHub connector sessions to use the bundled lesson data
  instead of unrelated repository search hits
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

Current clean release: `v1.0.13` / `1.0.13`

Reference:

- https://docs.openclaw.ai/tools/clawhub
