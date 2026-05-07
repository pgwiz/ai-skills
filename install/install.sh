#!/usr/bin/env sh
# install.sh — Agent Memory Skill installer
# Source: https://github.com/pgwiz/ai-skills
# Works on: macOS, Linux, WSL

set -eu

AGENT_USER="$(whoami)"
AGENT_HOME="${HOME}"
AGENT_SYSTEM_PATH="${HOME}/agent-system"

if [ -d "${HOME}/.copilot" ]; then
    SKILL_PATH="${HOME}/.copilot/skills/agent-memory"
elif [ -d "${HOME}/.agents" ]; then
    SKILL_PATH="${HOME}/.agents/skills/agent-memory"
else
    mkdir -p "${HOME}/.copilot/skills"
    SKILL_PATH="${HOME}/.copilot/skills/agent-memory"
fi

echo ""
echo "=== Agent Memory Skill Installer ==="
echo "User      : ${AGENT_USER}"
echo "Home      : ${AGENT_HOME}"
echo "System    : ${AGENT_SYSTEM_PATH}"
echo "Skill dir : ${SKILL_PATH}"
echo ""
printf "Proceed? (y/n): "
read -r confirm
[ "${confirm}" != "y" ] && echo "Aborted." && exit 0

TMP_ROOT=""
cleanup() {
    if [ -n "${TMP_ROOT}" ] && [ -d "${TMP_ROOT}" ]; then
        rm -rf "${TMP_ROOT}"
    fi
}
trap cleanup EXIT INT TERM

if [ -f "./agent-memory/SKILL.md" ]; then
    SOURCE_ROOT="."
else
    TMP_BASE="${TMPDIR:-/tmp}"
    if command -v mktemp >/dev/null 2>&1; then
        TMP_ROOT="$(mktemp -d "${TMP_BASE}/ai-skills.XXXXXX")"
    else
        TMP_ROOT="${TMP_BASE}/ai-skills.$$"
        mkdir -p "${TMP_ROOT}"
    fi

    echo "Fetching skill source from GitHub..."
    if command -v git >/dev/null 2>&1; then
        git clone --depth=1 https://github.com/pgwiz/ai-skills.git "${TMP_ROOT}/repo" >/dev/null 2>&1
        SOURCE_ROOT="${TMP_ROOT}/repo"
    elif command -v curl >/dev/null 2>&1 && command -v tar >/dev/null 2>&1; then
        curl -fsSL https://github.com/pgwiz/ai-skills/archive/refs/heads/main.tar.gz -o "${TMP_ROOT}/repo.tar.gz"
        mkdir -p "${TMP_ROOT}/extract"
        tar -xzf "${TMP_ROOT}/repo.tar.gz" -C "${TMP_ROOT}/extract"
        SOURCE_ROOT="${TMP_ROOT}/extract/ai-skills-main"
    else
        echo "Error: no local source found and cannot fetch from GitHub (need git or curl+tar)." >&2
        exit 1
    fi
fi

if [ ! -f "${SOURCE_ROOT}/agent-memory/SKILL.md" ]; then
    echo "Error: source files not found at ${SOURCE_ROOT}" >&2
    exit 1
fi

patch_file() {
    file="$1"
    tmp_file="${file}.tmp"
    sed \
        -e "s|{AGENT_SYSTEM_PATH}|${AGENT_SYSTEM_PATH}|g" \
        -e "s|{AGENT_USER}|${AGENT_USER}|g" \
        -e "s|{AGENT_HOME}|${AGENT_HOME}|g" \
        "$file" > "$tmp_file"
    mv "$tmp_file" "$file"
}

echo "Installing global memory files..."
mkdir -p "${AGENT_SYSTEM_PATH}"

for f in GLOBAL_PROTOCOL.md GLOBAL_WARNINGS.md CONVENTIONS.md AGENT_BOOTSTRAP.md SESSION_START.md README.md; do
    src="${SOURCE_ROOT}/agent-memory/references/${f}"
    dest="${AGENT_SYSTEM_PATH}/${f}"
    if [ -f "$src" ]; then
        cp "$src" "$dest"
        patch_file "$dest"
        echo "  ✓ ${f}"
    fi
done

echo "Installing skill..."
mkdir -p "${SKILL_PATH}/references"

cp "${SOURCE_ROOT}/agent-memory/SKILL.md" "${SKILL_PATH}/SKILL.md"
patch_file "${SKILL_PATH}/SKILL.md"

for f in "${SOURCE_ROOT}"/agent-memory/references/*.md; do
    cp "$f" "${SKILL_PATH}/references/"
    patch_file "${SKILL_PATH}/references/$(basename "$f")"
done

INSTALLED_ON="$(date '+%Y-%m-%d %H:%M')"
PLATFORM="$(uname -s)"
CONFIG_CONTENT="AGENT_SYSTEM_PATH=${AGENT_SYSTEM_PATH}
AGENT_USER=${AGENT_USER}
AGENT_HOME=${AGENT_HOME}
INSTALLED_ON=${INSTALLED_ON}
PLATFORM=${PLATFORM}"

printf "%s\n" "$CONFIG_CONTENT" > "${AGENT_SYSTEM_PATH}/.agent-config"
printf "%s\n" "$CONFIG_CONTENT" > "${SKILL_PATH}/.agent-config"

echo ""
echo "✓ Install complete!"
echo ""
echo "Global files : ${AGENT_SYSTEM_PATH}/"
echo "Skill        : ${SKILL_PATH}/"
echo ""
echo "NEXT STEPS:"
echo "  1. Open any project root"
echo "  2. Tell the agent: Bootstrap .agent/ for this project"
echo "  3. From now on, just type your task"
echo ""
