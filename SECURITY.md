# Security

This repository publishes a sanitized OpenClaw skill and plugin bundle. It should
not contain secrets, local workstation paths, raw lesson media, Drive file IDs,
or private account identifiers.

## Reporting

Report a security issue privately through the GitHub repository owner profile:

https://github.com/zack-dev-cm

Avoid opening public issues that include credentials, private file IDs, or other
sensitive data.

## Supported Surface

The supported public surface is the latest tagged release and the `latest`
ClawHub skill tag.

## Gate

Every public release must pass:

```bash
python3 scripts/check_publication_bundle.py
```
