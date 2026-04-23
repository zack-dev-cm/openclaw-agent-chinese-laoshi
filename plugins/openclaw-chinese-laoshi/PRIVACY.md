# Privacy

OpenClaw Chinese Laoshi is a workflow plugin. It does not ship telemetry or
its own remote storage.

## Data handling

- Raw lesson videos are expected to stay in Google Drive or another operator
  controlled source.
- Durable text assets such as lesson JSON, Markdown lesson docs, and manifests
  are stored where the operator keeps the project repository.
- The publication gate is designed to block local filesystem paths, secret-like
  strings, and known Drive file IDs from shipping in the public bundle.

## Operator responsibility

- Review source permissions before exporting lesson assets.
- Keep API keys in environment variables, not in tracked files.
- Do not publish content that still contains customer names, account IDs, or
  local browser/session details.
