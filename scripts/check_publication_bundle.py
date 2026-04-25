#!/usr/bin/env python3
"""
Fail closed on placeholder text, leak-prone strings, and drift inside the
sanitized public release bundle before GitHub or ClawHub publication.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()

if (ROOT / "release" / "public-repo").exists():
    BUNDLE_ROOT = ROOT / "release" / "public-repo"
    MANIFEST_SOURCE_PATH = ROOT / "data" / "manifests" / "drive-files.json"
else:
    BUNDLE_ROOT = ROOT
    MANIFEST_SOURCE_PATH = ROOT / "data" / "manifests" / "drive-files.json"

PLUGIN_ROOT = BUNDLE_ROOT / "plugins" / "openclaw-chinese-laoshi"
PUBLIC_SKILL_ROOT = BUNDLE_ROOT / "skills" / "openclaw-chinese-laoshi-ops"
PLUGIN_SKILL_ROOT = PLUGIN_ROOT / "skills" / "openclaw-chinese-laoshi-ops"
MARKETPLACE_PATH = BUNDLE_ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
README_PATH = BUNDLE_ROOT / "README.md"
PUBLISHING_PATH = BUNDLE_ROOT / "PUBLISHING.md"
CHANGELOG_PATH = BUNDLE_ROOT / "CHANGELOG.md"
CITATION_PATH = BUNDLE_ROOT / "CITATION.cff"
LICENSE_PATH = BUNDLE_ROOT / "LICENSE"
REQUIRED_BUNDLE_FILES = [
    "README.md",
    "PUBLISHING.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "LICENSE",
]
ROOT_TEXT_FILES = [
    "README.md",
    "PUBLISHING.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CHANGELOG.md",
    "CITATION.cff",
    ".agents/plugins/marketplace.json",
]
TEXT_EXTENSIONS = {".cff", ".json", ".md", ".yaml", ".yml", ".svg", ".txt"}

PLACEHOLDER_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\[TODO:",
        r"lorem ipsum",
        r"docs\.example\.com",
        r"author@example\.com",
        r"keyword1",
        r"keyword2",
        r"Marketplace Display Name",
        r"marketplace-name",
        r"keep the same stages anyway",
    )
]

LEAK_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        re.escape(str(HOME)),
        r"https?://localhost(?::\d+)?",
        r"https?://127\.0\.0\.1(?::\d+)?",
        r"\bws://[A-Za-z0-9][^\s)]*",
        r"\bwss://[A-Za-z0-9][^\s)]*",
        r"devtools/browser/[A-Za-z0-9._-]+",
        r"drive\.google\.com/file/d/[A-Za-z0-9_-]+",
        r"drive\.google\.com/drive/folders/[A-Za-z0-9_-]+",
        r'"drive_file_id"\s*:',
        r'"drive_url"\s*:',
        r'"parent_folder_id"\s*:',
        r"browser_cookie3",
        r"kaisenaiko@gmail\.com",
    )
]

SECRET_PATTERNS = [
    re.compile(pattern)
    for pattern in (
        r"ghp_[A-Za-z0-9]{20,}",
        r"github_pat_[A-Za-z0-9_]{20,}",
        r"sk-[A-Za-z0-9]{20,}",
        r"AIza[0-9A-Za-z\-_]{20,}",
        r"xox[baprs]-[A-Za-z0-9-]{10,}",
        r"(?:API[_-]?KEY|TOKEN|SECRET|PASSWORD)\s*[:=]\s*['\"]?[A-Za-z0-9/_+=.\-]{12,}",
    )
]

MIRRORED_FILES = [
    ("SKILL.md", "SKILL.md"),
    ("agents/openai.yaml", "agents/openai.yaml"),
    ("references/chatgpt-connector-guidance.md", "references/chatgpt-connector-guidance.md"),
    ("references/pipeline.md", "references/pipeline.md"),
    ("references/release-gates.md", "references/release-gates.md"),
]

COURSE_DATA_ROOT_RELATIVE = Path("references/course-data")
REQUIRED_COURSE_DATA_FILES = [
    "README.md",
    "course-index.md",
    "lessons-bundle.json",
    "lessons-bundle.md",
    "hsk-training.json",
    "roleplay-training.json",
    "lesson-plans/README.md",
    "hsk/README.md",
    "roleplays/README.md",
]

BANNED_COURSE_DATA_JSON_KEYS = {
    "drive_file_id",
    "drive_title",
    "drive_url",
    "parent_folder_id",
    "verified_via",
    "source",
    "source_name",
    "source_url",
    "source_title_ru",
    "source_segment_indexes",
    "official_title_ru",
    "official_description_ru",
    "editorial_expansion_note",
    "confidence_notes",
    "lesson_summary",
    "focus_tags",
    "editorial_status",
    "transcript_status",
    "translation_status",
    "pinyin_status",
    "review_status",
    "review_snapshot",
    "evidence_level",
    "editorial_note",
    "start_ms",
    "end_ms",
    "speaker_role",
    "source_ru",
    "uncertainty_notes",
    "duration_seconds",
    "metadata",
}

REQUIRED_SKILL_SAFETY_SNIPPETS = [
    "model-invocable: false",
    "disable-model-invocation: true",
    "No Google Drive cloud upload or direct Drive API access is declared or assumed by this published skill.",
    "This published ClawHub skill can use bundled public course data or transcript/subtitle inputs only.",
    "It does not request API keys, cloud transcription credentials, browser sessions, or Drive auth.",
    "This skill has no standalone runtime requirement and does not install code.",
    "Before executing any repository command, present the exact command and wait for explicit user confirmation",
    "If a matching audited command is absent, stop",
    "`--drive-root`",
    "Never search for credentials",
]

FORBIDDEN_PUBLIC_SKILL_SNIPPETS = [
    "OPENAI_API_KEY",
    "--api-key-env",
    "transcribe_lesson_with_whisper.py",
]


def load_drive_ids(manifest_path: Path = MANIFEST_SOURCE_PATH) -> set[str]:
    if not manifest_path.exists():
        return set()
    payload = json.loads(manifest_path.read_text("utf8"))
    drive_ids: set[str] = set()
    source_folder_id = (payload.get("source_folder") or {}).get("folder_id")
    if isinstance(source_folder_id, str) and source_folder_id:
        drive_ids.add(source_folder_id)
    for key in ("core_lessons", "lessons", "enrichment_assets", "assets"):
        for item in payload.get(key, []):
            value = item.get("file_id") or item.get("drive_file_id")
            if isinstance(value, str) and value:
                drive_ids.add(value)
    return drive_ids


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
            files.append(path)
    return sorted(files)


def collect_text_issues(path: Path, text: str, drive_ids: set[str]) -> list[str]:
    issues: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        if pattern.search(text):
            issues.append(f"{display_path(path)}: placeholder match `{pattern.pattern}`")
    for pattern in LEAK_PATTERNS:
        if pattern.search(text):
            issues.append(f"{display_path(path)}: leak-prone match `{pattern.pattern}`")
    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append(f"{display_path(path)}: secret-shaped match `{pattern.pattern}`")
    for drive_id in sorted(drive_ids):
        if drive_id in text:
            issues.append(f"{display_path(path)}: known Drive file id leaked: {drive_id}")
    return issues


def collect_json_key_issues(path: Path, value, parents: tuple[str, ...] = ()) -> list[str]:
    issues: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = parents + (str(key),)
            if key in BANNED_COURSE_DATA_JSON_KEYS:
                issues.append(f"{display_path(path)}: internal JSON key `{'.'.join(child_path)}`")
            issues.extend(collect_json_key_issues(path, child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            issues.extend(collect_json_key_issues(path, child, parents + (str(index),)))
    return issues


def validate_plugin_manifest() -> list[str]:
    issues: list[str] = []
    payload = json.loads(PLUGIN_MANIFEST_PATH.read_text("utf8"))
    for key in ("name", "version", "description", "homepage", "repository", "license", "skills"):
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            issues.append(f"{PLUGIN_MANIFEST_PATH.relative_to(ROOT)}: missing `{key}`")
    interface = payload.get("interface") or {}
    for key in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "websiteURL",
        "privacyPolicyURL",
        "termsOfServiceURL",
        "brandColor",
        "composerIcon",
        "logo",
    ):
        value = interface.get(key)
        if not isinstance(value, str) or not value.strip():
            issues.append(f"{PLUGIN_MANIFEST_PATH.relative_to(ROOT)}: missing interface field `{key}`")
    default_prompt = interface.get("defaultPrompt")
    if not isinstance(default_prompt, list) or not default_prompt:
        issues.append(f"{PLUGIN_MANIFEST_PATH.relative_to(ROOT)}: `interface.defaultPrompt` must be a non-empty list")
    return issues


def validate_marketplace_manifest() -> list[str]:
    issues: list[str] = []
    payload = json.loads(MARKETPLACE_PATH.read_text("utf8"))
    if not isinstance(payload.get("name"), str) or not payload["name"].strip():
        issues.append(f"{MARKETPLACE_PATH.relative_to(ROOT)}: missing marketplace name")
    interface = payload.get("interface") or {}
    if not isinstance(interface.get("displayName"), str) or not interface["displayName"].strip():
        issues.append(f"{MARKETPLACE_PATH.relative_to(ROOT)}: missing marketplace displayName")
    plugins = payload.get("plugins") or []
    target = next((item for item in plugins if item.get("name") == "openclaw-chinese-laoshi"), None)
    if target is None:
        issues.append(f"{MARKETPLACE_PATH.relative_to(ROOT)}: missing openclaw-chinese-laoshi entry")
        return issues
    if target.get("source", {}).get("path") != "./plugins/openclaw-chinese-laoshi":
        issues.append(f"{MARKETPLACE_PATH.relative_to(ROOT)}: unexpected source path")
    return issues


def validate_public_metadata() -> list[str]:
    issues: list[str] = []
    readme = README_PATH.read_text("utf8") if README_PATH.exists() else ""
    publishing = PUBLISHING_PATH.read_text("utf8") if PUBLISHING_PATH.exists() else ""
    changelog = CHANGELOG_PATH.read_text("utf8") if CHANGELOG_PATH.exists() else ""
    if "https://clawhub.ai/zack-dev-cm/openclaw-agent-chinese-laoshi" not in readme:
        issues.append(f"{README_PATH.relative_to(ROOT)}: missing ClawHub public page link")
    if "Initial GitHub and ClawHub version" in readme:
        issues.append(f"{README_PATH.relative_to(ROOT)}: stale pre-cleanup version wording must not be published")
    if "https://clawhub.ai/zack-dev-cm/openclaw-chinese-laoshi" in readme:
        issues.append(f"{README_PATH.relative_to(ROOT)}: retired ClawHub slug must not be the public page link")
    if "https://clawhub.ai/zack-dev-cm/openclaw-chinese-laoshi-ops" in readme:
        issues.append(f"{README_PATH.relative_to(ROOT)}: retired ClawHub slug must not be the public page link")
    if "openclaw-chinese-laoshi --name" in publishing:
        issues.append(f"{PUBLISHING_PATH.relative_to(ROOT)}: retired ClawHub slug must not be the publish target")
    if "openclaw-chinese-laoshi-ops --name" in publishing:
        issues.append(f"{PUBLISHING_PATH.relative_to(ROOT)}: retired ClawHub slug must not be the publish target")
    if "--slug openclaw-agent-chinese-laoshi" not in publishing:
        issues.append(f"{PUBLISHING_PATH.relative_to(ROOT)}: missing canonical ClawHub publish target")
    if "--tags latest,chinese,language-learning,drive" not in publishing:
        issues.append(f"{PUBLISHING_PATH.relative_to(ROOT)}: missing required ClawHub publish tags")
    if "gh repo edit zack-dev-cm/openclaw-agent-chinese-laoshi --homepage https://clawhub.ai/zack-dev-cm/openclaw-agent-chinese-laoshi" not in publishing:
        issues.append(f"{PUBLISHING_PATH.relative_to(ROOT)}: missing GitHub homepage linkage step")
    if re.search(r"^## v1\.0\.[0-8]\b", changelog, re.MULTILINE):
        issues.append(f"{CHANGELOG_PATH.relative_to(ROOT)}: public changelog must not expose pre-cleanup release history")
    if "openclaw-chinese-laoshi" in changelog:
        issues.append(f"{CHANGELOG_PATH.relative_to(ROOT)}: public changelog must not expose retired ClawHub slugs")

    return issues


def parse_skill_metadata(skill_path: Path) -> dict:
    text = skill_path.read_text("utf8")
    for line in text.splitlines():
        if line.startswith("metadata: "):
            return json.loads(line[len("metadata: "):].strip())
    return {}


def parse_frontmatter_value(path: Path, key: str) -> str:
    if not path.exists():
        return ""
    text = path.read_text("utf8")
    match = re.search(rf"^{re.escape(key)}:\s*([^\n]+)", text, re.MULTILINE)
    if not match:
        return ""
    return match.group(1).strip().strip('"').strip("'")


def load_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text("utf8"))


def validate_version_consistency() -> list[str]:
    issues: list[str] = []
    public_version = parse_frontmatter_value(PUBLIC_SKILL_ROOT / "SKILL.md", "version")
    plugin_skill_version = parse_frontmatter_value(PLUGIN_SKILL_ROOT / "SKILL.md", "version")
    plugin_manifest_version = load_json_file(PLUGIN_MANIFEST_PATH).get("version", "")
    readme = README_PATH.read_text("utf8") if README_PATH.exists() else ""
    publishing = PUBLISHING_PATH.read_text("utf8") if PUBLISHING_PATH.exists() else ""
    changelog = CHANGELOG_PATH.read_text("utf8") if CHANGELOG_PATH.exists() else ""
    citation = CITATION_PATH.read_text("utf8") if CITATION_PATH.exists() else ""

    if not re.match(r"^\d+\.\d+\.\d+$", public_version or ""):
        issues.append(f"{PUBLIC_SKILL_ROOT.relative_to(ROOT)}/SKILL.md: missing valid semver version")
        return issues

    for label, value in [
        ("plugin skill", plugin_skill_version),
        ("plugin manifest", plugin_manifest_version),
    ]:
        if value != public_version:
            issues.append(f"{label} version `{value}` does not match public skill version `{public_version}`")

    if f"Current clean release: `v{public_version}` / `{public_version}`" not in readme:
        issues.append(f"{README_PATH.relative_to(ROOT)}: missing current clean release marker for {public_version}")
    if not re.search(rf"^## v{re.escape(public_version)}\b", changelog, re.MULTILINE):
        issues.append(f"{CHANGELOG_PATH.relative_to(ROOT)}: missing changelog heading for v{public_version}")
    if f'version: "{public_version}"' not in citation:
        issues.append(f"{CITATION_PATH.relative_to(ROOT)}: citation version does not match {public_version}")
    if f"--version {public_version}" not in publishing:
        issues.append(f"{PUBLISHING_PATH.relative_to(ROOT)}: missing exact ClawHub publish version {public_version}")
    if f"git -C release/public-repo tag -a v{public_version}" not in publishing:
        issues.append(f"{PUBLISHING_PATH.relative_to(ROOT)}: missing bundle-root tag command for v{public_version}")

    return issues


def validate_skill_release_safety() -> list[str]:
    issues: list[str] = []
    skill_path = PUBLIC_SKILL_ROOT / "SKILL.md"
    if not skill_path.exists():
        return [f"missing public skill file: {skill_path.relative_to(ROOT)}"]

    text = skill_path.read_text("utf8")
    flattened = " ".join(line.strip() for line in text.splitlines())
    for snippet in REQUIRED_SKILL_SAFETY_SNIPPETS:
        if snippet not in flattened:
            issues.append(f"{skill_path.relative_to(ROOT)}: missing release safety wording `{snippet}`")
    for snippet in FORBIDDEN_PUBLIC_SKILL_SNIPPETS:
        if snippet in text:
            issues.append(f"{skill_path.relative_to(ROOT)}: public skill must not mention `{snippet}`")

    metadata = parse_skill_metadata(skill_path)
    requirements = ((metadata.get("openclaw") or {}).get("requires") or {})
    bins = set(requirements.get("bins") or [])
    if bins:
        issues.append(f"{skill_path.relative_to(ROOT)}: published skill must not declare runtime bins")

    return issues


def validate_mirrors() -> list[str]:
    issues: list[str] = []
    for public_relative, plugin_relative in MIRRORED_FILES:
        public_path = PUBLIC_SKILL_ROOT / public_relative
        plugin_path = PLUGIN_SKILL_ROOT / plugin_relative
        if not public_path.exists():
            issues.append(f"missing public skill file: {public_path.relative_to(ROOT)}")
            continue
        if not plugin_path.exists():
            issues.append(f"missing plugin skill file: {plugin_path.relative_to(ROOT)}")
            continue
        if public_path.read_text("utf8") != plugin_path.read_text("utf8"):
            issues.append(
                f"mirror drift: {public_path.relative_to(ROOT)} != {plugin_path.relative_to(ROOT)}"
            )
    return issues


def relative_file_set(root: Path) -> set[str]:
    if not root.exists():
        return set()
    return {
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.is_file()
    }


def expected_course_data_files() -> set[str]:
    expected = set(REQUIRED_COURSE_DATA_FILES)
    expected.update(f"lesson-plans/lesson-{number:02d}.md" for number in range(1, 17))
    expected.update(f"hsk/lesson-{number:02d}.json" for number in range(1, 17))
    expected.update(f"roleplays/lesson-{number:02d}.json" for number in range(1, 17))
    return expected


def validate_course_data_root(root: Path, drive_ids: set[str]) -> list[str]:
    issues: list[str] = []
    if not root.exists():
        return [f"missing bundled course data: {display_path(root)}"]

    expected_files = expected_course_data_files()
    actual_files = relative_file_set(root)
    missing_files = sorted(expected_files - actual_files)
    unexpected_files = sorted(actual_files - expected_files)
    for relative in missing_files:
        issues.append(f"missing bundled course data file: {display_path(root / relative)}")
    for relative in unexpected_files:
        issues.append(f"unexpected bundled course data file: {display_path(root / relative)}")

    for relative in sorted(actual_files):
        path = root / relative
        if path.suffix.lower() not in {".json", ".md"}:
            issues.append(f"{display_path(path)}: unsupported course-data file type")
        if path.stat().st_size > 2_000_000:
            issues.append(f"{display_path(path)}: course-data file is unexpectedly large")

    expected_counts = [
        ("lesson-plans/lesson-*.md", 16),
        ("hsk/lesson-*.json", 16),
        ("roleplays/lesson-*.json", 16),
    ]
    for pattern, expected in expected_counts:
        count = len(list(root.glob(pattern)))
        if count != expected:
            issues.append(f"{display_path(root)} expected {expected} files for {pattern}, found {count}")

    lesson_bundle_path = root / "lessons-bundle.json"
    if lesson_bundle_path.exists():
        try:
            payload = json.loads(lesson_bundle_path.read_text("utf8"))
        except json.JSONDecodeError as error:
            issues.append(f"{display_path(lesson_bundle_path)}: invalid JSON: {error}")
        else:
            lessons = payload.get("lessons")
            if not isinstance(lessons, list) or len(lessons) != 16:
                issues.append(f"{display_path(lesson_bundle_path)}: expected 16 public lessons")

    for path in iter_text_files(root):
        text = path.read_text("utf8")
        issues.extend(collect_text_issues(path, text, drive_ids))
        if path.suffix.lower() == ".json":
            try:
                issues.extend(collect_json_key_issues(path, json.loads(text)))
            except json.JSONDecodeError as error:
                issues.append(f"{display_path(path)}: invalid JSON: {error}")

    return issues


def validate_course_data_bundle(drive_ids: set[str]) -> list[str]:
    issues: list[str] = []
    public_root = PUBLIC_SKILL_ROOT / COURSE_DATA_ROOT_RELATIVE
    plugin_root = PLUGIN_SKILL_ROOT / COURSE_DATA_ROOT_RELATIVE

    issues.extend(validate_course_data_root(public_root, drive_ids))
    issues.extend(validate_course_data_root(plugin_root, drive_ids))

    public_files = relative_file_set(public_root)
    plugin_files = relative_file_set(plugin_root)
    if public_files != plugin_files:
        issues.append("public and plugin course-data file lists drift")
    for relative in sorted(public_files & plugin_files):
        public_path = public_root / relative
        plugin_path = plugin_root / relative
        if public_path.read_bytes() != plugin_path.read_bytes():
            issues.append(f"course-data mirror drift: {public_path.relative_to(ROOT)} != {plugin_path.relative_to(ROOT)}")

    return issues


def main() -> int:
    issues: list[str] = []
    drive_ids = load_drive_ids()

    if not BUNDLE_ROOT.exists():
        print("publication bundle check failed:")
        print(f"- missing bundle root: {BUNDLE_ROOT.relative_to(ROOT)}")
        print("- run `python3 scripts/build_public_release_bundle.py` first")
        return 1

    for relative in REQUIRED_BUNDLE_FILES:
        path = BUNDLE_ROOT / relative
        if not path.exists():
            issues.append(f"missing bundle file: {path.relative_to(ROOT)}")

    for root in (PLUGIN_ROOT, PUBLIC_SKILL_ROOT):
        if not root.exists():
            issues.append(f"missing publication root: {root.relative_to(ROOT)}")
            continue
        for path in iter_text_files(root):
            issues.extend(collect_text_issues(path, path.read_text("utf8"), drive_ids))

    for relative in ROOT_TEXT_FILES:
        path = BUNDLE_ROOT / relative
        if path.exists():
            issues.extend(collect_text_issues(path, path.read_text("utf8"), drive_ids))

    if not PLUGIN_MANIFEST_PATH.exists():
        issues.append(f"missing plugin manifest: {PLUGIN_MANIFEST_PATH.relative_to(ROOT)}")
    else:
        issues.extend(validate_plugin_manifest())

    if not MARKETPLACE_PATH.exists():
        issues.append(f"missing marketplace manifest: {MARKETPLACE_PATH.relative_to(ROOT)}")
    else:
        marketplace_text = MARKETPLACE_PATH.read_text("utf8")
        issues.extend(collect_text_issues(MARKETPLACE_PATH, marketplace_text, drive_ids))
        issues.extend(validate_marketplace_manifest())

    issues.extend(validate_public_metadata())
    issues.extend(validate_version_consistency())
    issues.extend(validate_mirrors())
    issues.extend(validate_course_data_bundle(drive_ids))
    issues.extend(validate_skill_release_safety())

    if issues:
        print("publication bundle check failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("publication bundle check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
