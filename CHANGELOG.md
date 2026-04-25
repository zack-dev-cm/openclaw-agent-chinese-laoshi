# Changelog

## v1.0.12 - 2026-04-25

- Added ChatGPT connector guidance so GitHub-connected sessions pin the correct
  Chinese Laoshi repo before searching broadly.
- Documented how to answer repo "system prompt" requests using visible prompt
  artifacts without exposing hidden platform instructions.
- Added roleplay-start checks that force ChatGPT sessions to read bundled
  `references/course-data` before starting Chinese lesson practice.
- Extended the publication gate to keep the standalone skill and plugin skill
  connector guidance mirrored.

## v1.0.11 - 2026-04-25

- Bundled sanitized public lesson data directly inside the published skill under
  `references/course-data`, including the lesson bundle, lesson plans, HSK
  practice payloads, roleplay scenarios, and training manifests.
- Added publication gates that fail when the public skill or plugin skill is
  missing course data, has incomplete lesson counts, leaks internal JSON keys,
  or drifts between the two published skill copies.
- Kept raw media, raw transcripts, Drive IDs, local paths, source indexes,
  review-control metadata, and credential lanes out of the public artifact.

## v1.0.9 - 2026-04-23

- Published the clean public GitHub bundle and canonical ClawHub package at
  `openclaw-agent-chinese-laoshi`.
- Kept the published skill instruction-only: no installs, no declared runtime
  bins, no credential requests, and explicit command confirmation before any
  repository command.
- Enforced public release gates for placeholder text, local-path bleed,
  loopback/debug endpoints, secret-shaped text, known Drive IDs, stale ClawHub
  slugs, and drift between the public skill and plugin copy.
