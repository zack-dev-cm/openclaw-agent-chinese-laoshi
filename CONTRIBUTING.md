# Contributing

This public bundle is a distribution surface for the OpenClaw Chinese Laoshi
skill and plugin.

## Scope

Good contributions improve:

- skill instructions and release-gate clarity
- plugin metadata, privacy, or terms text
- publication checks that prevent leaked private paths, Drive IDs, secrets, or
  placeholder text

The internal lesson extraction workspace, raw media, private Drive manifests, and
operator-only notes are intentionally outside this public bundle.

## Local Check

Run the publication gate before opening a change:

```bash
python3 scripts/check_publication_bundle.py
```

Do not add raw lesson media, private Drive links, local filesystem paths, API
tokens, or personal account identifiers.
