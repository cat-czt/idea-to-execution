#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:-cat-czt/idea-to-execution}"
REF="${REF:-main}"
SKILL_NAME="idea-to-execution"
TARGET="generic"
INSTALL_PARENT=""
FORCE="0"

usage() {
  cat <<'USAGE'
Install idea-to-execution skill from GitHub.

Usage:
  curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash
  curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash -s -- --target claude
  curl -fsSL https://raw.githubusercontent.com/cat-czt/idea-to-execution/main/scripts/install-skill.sh | bash -s -- --dir "$HOME/.agent/skills"

Options:
  --target generic|claude|codex|opencode  Choose a default install parent.
  --dir PATH                            Install under PATH/idea-to-execution.
  --ref REF                             Git ref to install from. Default: main.
  --force                               Replace existing installation.
  -h, --help                            Show this help.

Environment:
  SKILLS_DIR    Overrides install parent directory.
  REPO          Overrides GitHub repo, default cat-czt/idea-to-execution.
  REF           Overrides Git ref, default main.
USAGE
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --dir)
      INSTALL_PARENT="${2:-}"
      shift 2
      ;;
    --ref)
      REF="${2:-}"
      shift 2
      ;;
    --force)
      FORCE="1"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[error] unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v curl >/dev/null 2>&1; then
  echo "[error] curl is required" >&2
  exit 1
fi
if ! command -v tar >/dev/null 2>&1; then
  echo "[error] tar is required" >&2
  exit 1
fi

if [ -n "${SKILLS_DIR:-}" ]; then
  INSTALL_PARENT="$SKILLS_DIR"
elif [ -z "$INSTALL_PARENT" ]; then
  case "$TARGET" in
    generic)
      INSTALL_PARENT="$HOME/.agent/skills"
      ;;
    claude)
      INSTALL_PARENT="$HOME/.claude/skills"
      ;;
    codex|opencode)
      INSTALL_PARENT="$HOME/.agent/skills"
      ;;
    *)
      echo "[error] unsupported target: $TARGET" >&2
      echo "[hint] use --target generic, claude, codex, opencode, or --dir PATH" >&2
      exit 2
      ;;
  esac
fi

DEST="$INSTALL_PARENT/$SKILL_NAME"
TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

mkdir -p "$TMP_DIR/src" "$INSTALL_PARENT"
ARCHIVE_URL="https://github.com/${REPO}/archive/refs/heads/${REF}.tar.gz"

printf '[info] installing %s from %s@%s\n' "$SKILL_NAME" "$REPO" "$REF"
printf '[info] destination: %s\n' "$DEST"

if [ -e "$DEST" ] && [ "$FORCE" != "1" ]; then
  echo "[error] destination already exists: $DEST" >&2
  echo "[hint] rerun with --force to replace it" >&2
  exit 1
fi

curl -fsSL "$ARCHIVE_URL" -o "$TMP_DIR/repo.tar.gz"
tar -xzf "$TMP_DIR/repo.tar.gz" --strip-components=1 -C "$TMP_DIR/src"

if [ ! -f "$TMP_DIR/src/SKILL.md" ]; then
  echo "[error] downloaded repository does not contain SKILL.md at root" >&2
  exit 1
fi

if [ "$FORCE" = "1" ]; then
  rm -rf "$DEST"
fi
mkdir -p "$DEST"
cp -R "$TMP_DIR/src/." "$DEST/"

if [ -f "$DEST/scripts/kanban_dispatch.py" ]; then
  chmod +x "$DEST/scripts/kanban_dispatch.py" || true
fi

cat <<EOF
[ok] installed $SKILL_NAME

Location:
  $DEST

Next steps:
  1. Point your agent or project instructions to this skill directory.
  2. For Claude Code-style use, copy or reference the rules in:
     $DEST/SKILL.md
  3. For Codex/OpenCode-style use, add a short AGENTS.md instruction:
     Use the idea-to-execution protocol from $DEST.

Test:
  test -f "$DEST/SKILL.md" && echo "skill installed"
EOF
