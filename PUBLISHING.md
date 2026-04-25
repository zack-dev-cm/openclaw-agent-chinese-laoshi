# Publishing

This bundle is the public release surface. It intentionally excludes internal
lesson manifests, local Drive mount traces, and operator-only working docs.
It must include sanitized public course data under
`skills/openclaw-chinese-laoshi-ops/references/course-data` so the published
ClawHub skill can answer lesson-study requests without private repo access.

## Build

From the internal working repo:

```bash
python3 scripts/build_public_release_bundle.py
```

Or build, verify, and initialize a git repo inside the public bundle:

```bash
bash scripts/init_public_release_git.sh https://github.com/zack-dev-cm/openclaw-agent-chinese-laoshi.git
```

## Verify

```bash
python3 scripts/check_publication_bundle.py
```

## Publish

1. Push the contents of `release/public-repo` to a public GitHub repository:

```bash
git -C release/public-repo status --short
git -C release/public-repo add -A
git -C release/public-repo commit -m "Add ChatGPT connector guidance"
git -C release/public-repo push origin main
```

2. Tag the exact commit that passed the publication gate:

```bash
git -C release/public-repo tag -a v1.0.12 -m "OpenClaw Chinese Laoshi v1.0.12"
git -C release/public-repo push origin main --tags
```

3. Set the GitHub repository homepage to the ClawHub skill page so catalog
   tooling can link the GitHub and ClawHub surfaces:

```bash
gh repo edit zack-dev-cm/openclaw-agent-chinese-laoshi --homepage https://clawhub.ai/zack-dev-cm/openclaw-agent-chinese-laoshi
```

4. Add repository topics that match the published skill tags:

```bash
gh repo edit zack-dev-cm/openclaw-agent-chinese-laoshi --add-topic openclaw --add-topic chinese --add-topic language-learning --add-topic drive --add-topic skill
```

5. Publish the skill from that repo or directly from the local bundle:

```bash
clawhub publish ./skills/openclaw-chinese-laoshi-ops --slug openclaw-agent-chinese-laoshi --name "OpenClaw Chinese Laoshi Ops" --version <semver> --changelog "<text>" --tags latest,chinese,language-learning,drive
```

For the current release:

```bash
clawhub publish ./skills/openclaw-chinese-laoshi-ops --slug openclaw-agent-chinese-laoshi --name "OpenClaw Chinese Laoshi Ops" --version 1.0.12 --changelog "Add ChatGPT connector guidance for prompt lookup and lesson roleplay routing." --tags latest,chinese,language-learning,drive
```

## Published Locations

- GitHub:

```text
https://github.com/zack-dev-cm/openclaw-agent-chinese-laoshi
```

- ClawHub slug: `openclaw-agent-chinese-laoshi`
- ClawHub page: `https://clawhub.ai/zack-dev-cm/openclaw-agent-chinese-laoshi`
- Initial ClawHub version: `1.0.0`

## Fail Conditions

Publication must stop if the gate detects:

- placeholder scaffolding
- local absolute paths
- loopback or debugging endpoints
- secret-shaped strings
- known Drive file IDs
- drift between the bundled plugin skill and the public skill copy
- missing or incomplete public `references/course-data`
- missing ChatGPT connector guidance or drift between skill copies
- vague fallback authority when audited repository commands are missing
- public-skill Drive, transcription, or vision lanes that ask for secrets,
  browser sessions, or cloud auth
- missing public metadata, release notes, local publication gate, or publish docs
