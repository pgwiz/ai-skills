#!/usr/bin/env sh
# install.sh - Universal AI Skills installer (macOS, Linux, WSL)
# Source: https://github.com/pgwiz/ai-skills

set -eu

AGENT_USER="$(whoami)"
AGENT_HOME="${HOME}"
AGENT_SYSTEM_PATH="${HOME}/agent-system"

TARGET="auto"
SKILL="all"
SKILL_FOLDER_OVERRIDE=""
ASSUME_YES=0

while [ $# -gt 0 ]; do
  case "$1" in
    --target|-t)
      TARGET="$2"
      shift 2
      ;;
    --skill|-s)
      SKILL="$2"
      shift 2
      ;;
    --override|-o)
      SKILL_FOLDER_OVERRIDE="$2"
      shift 2
      ;;
    -y|--yes)
      ASSUME_YES=1
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

TARGET_DIRS=""

if [ -n "${SKILL_FOLDER_OVERRIDE}" ]; then
  TARGET_DIRS="custom:${SKILL_FOLDER_OVERRIDE}"
else
  case "${TARGET}" in
    antigravity)
      TARGET_DIRS="antigravity:${HOME}/.gemini/config/skills"
      ;;
    copilot)
      TARGET_DIRS="copilot:${HOME}/.copilot/skills"
      ;;
    agents)
      TARGET_DIRS="agents:${HOME}/.agents/skills"
      ;;
    all)
      TARGET_DIRS="antigravity:${HOME}/.gemini/config/skills copilot:${HOME}/.copilot/skills agents:${HOME}/.agents/skills"
      ;;
    auto)
      FOUND_DIRS=""
      if [ -d "${HOME}/.gemini/config/skills" ]; then
        FOUND_DIRS="${FOUND_DIRS} antigravity:${HOME}/.gemini/config/skills"
      fi
      if [ -d "${HOME}/.copilot" ]; then
        FOUND_DIRS="${FOUND_DIRS} copilot:${HOME}/.copilot/skills"
      fi
      if [ -d "${HOME}/.agents" ]; then
        FOUND_DIRS="${FOUND_DIRS} agents:${HOME}/.agents/skills"
      fi
      if [ -z "${FOUND_DIRS}" ]; then
        if [ -d "${HOME}/.gemini" ]; then
          FOUND_DIRS="antigravity:${HOME}/.gemini/config/skills"
        else
          FOUND_DIRS="copilot:${HOME}/.copilot/skills"
        fi
      fi
      # Trim leading space
      TARGET_DIRS="$(echo "${FOUND_DIRS}" | sed 's/^[ ]*//')"
      ;;
    *)
      echo "Error: Unknown target '${TARGET}'. Supported: auto, antigravity, copilot, agents, all" >&2
      exit 1
      ;;
  esac
fi

echo ""
echo "=== AI Skills Universal Installer (POSIX) ==="
echo "User        : ${AGENT_USER}"
echo "Home        : ${AGENT_HOME}"
echo "System Path : ${AGENT_SYSTEM_PATH}"
echo "Skills      : ${SKILL}"
echo "Targets     : ${TARGET_DIRS}"
echo ""

if [ "${ASSUME_YES}" -ne 1 ]; then
  printf "Proceed? (y/n): "
  read -r confirm
  [ "${confirm}" != "y" ] && echo "Aborted." && exit 0
fi

TMP_ROOT=""
cleanup() {
  if [ -n "${TMP_ROOT}" ] && [ -d "${TMP_ROOT}" ]; then
    rm -rf "${TMP_ROOT}"
  fi
}
trap cleanup EXIT INT TERM

if [ -f "./agent-memory/SKILL.md" ] || [ -f "./dev-md-compactor/SKILL.md" ]; then
  SOURCE_ROOT="."
elif [ -f "../agent-memory/SKILL.md" ] || [ -f "../dev-md-compactor/SKILL.md" ]; then
  SOURCE_ROOT=".."
else
  TMP_BASE="${TMPDIR:-/tmp}"
  if command -v mktemp >/dev/null 2>&1; then
    TMP_ROOT="$(mktemp -d "${TMP_BASE}/ai-skills.XXXXXX")"
  else
    TMP_ROOT="${TMP_BASE}/ai-skills.$$"
    mkdir -p "${TMP_ROOT}"
  fi

  echo "Fetching skills source from GitHub..."
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

INSTALLED_LOCATIONS=""

# 1. Install agent-memory
if [ "${SKILL}" = "all" ] || [ "${SKILL}" = "agent-memory" ]; then
  if [ ! -f "${SOURCE_ROOT}/agent-memory/SKILL.md" ]; then
    echo "Error: source for agent-memory not found at ${SOURCE_ROOT}/agent-memory" >&2
    exit 1
  fi

  echo "Installing global memory files for agent-memory..."
  mkdir -p "${AGENT_SYSTEM_PATH}"

  for f in GLOBAL_PROTOCOL.md GLOBAL_WARNINGS.md CONVENTIONS.md AGENT_BOOTSTRAP.md SESSION_START.md README.md; do
    src="${SOURCE_ROOT}/agent-memory/references/${f}"
    dest="${AGENT_SYSTEM_PATH}/${f}"
    if [ -f "$src" ]; then
      cp "$src" "$dest"
      patch_file "$dest"
      echo "  + ${f}"
    fi
  done

  INSTALLED_ON="$(date '+%Y-%m-%d %H:%M')"
  PLATFORM="$(uname -s)"
  CONFIG_CONTENT="AGENT_SYSTEM_PATH=${AGENT_SYSTEM_PATH}
AGENT_USER=${AGENT_USER}
AGENT_HOME=${AGENT_HOME}
INSTALLED_ON=${INSTALLED_ON}
PLATFORM=${PLATFORM}"

  printf "%s\n" "$CONFIG_CONTENT" > "${AGENT_SYSTEM_PATH}/.agent-config"

  for item in ${TARGET_DIRS}; do
    target_name="$(echo "${item}" | cut -d':' -f1)"
    base_dir="$(echo "${item}" | cut -d':' -f2)"

    if [ "${target_name}" = "custom" ] && echo "${base_dir}" | grep -q "agent-memory$"; then
      skill_dir="${base_dir}"
    else
      skill_dir="${base_dir}/agent-memory"
    fi

    echo "Installing agent-memory to ${target_name} [${skill_dir}]..."
    mkdir -p "${skill_dir}/references"
    cp "${SOURCE_ROOT}/agent-memory/SKILL.md" "${skill_dir}/SKILL.md"
    patch_file "${skill_dir}/SKILL.md"

    for f in "${SOURCE_ROOT}"/agent-memory/references/*.md; do
      [ -f "$f" ] || continue
      cp "$f" "${skill_dir}/references/"
      patch_file "${skill_dir}/references/$(basename "$f")"
    done

    printf "%s\n" "$CONFIG_CONTENT" > "${skill_dir}/.agent-config"
    INSTALLED_LOCATIONS="${INSTALLED_LOCATIONS}
  + ${skill_dir}"
  done
fi

# 2. Install dev-md-compactor
if [ "${SKILL}" = "all" ] || [ "${SKILL}" = "dev-md-compactor" ]; then
  if [ ! -f "${SOURCE_ROOT}/dev-md-compactor/SKILL.md" ]; then
    echo "Error: source for dev-md-compactor not found at ${SOURCE_ROOT}/dev-md-compactor" >&2
    exit 1
  fi

  for item in ${TARGET_DIRS}; do
    target_name="$(echo "${item}" | cut -d':' -f1)"
    base_dir="$(echo "${item}" | cut -d':' -f2)"

    if [ "${target_name}" = "custom" ] && echo "${base_dir}" | grep -q "dev-md-compactor$"; then
      skill_dir="${base_dir}"
    else
      skill_dir="${base_dir}/dev-md-compactor"
    fi

    echo "Installing dev-md-compactor to ${target_name} [${skill_dir}]..."
    mkdir -p "${skill_dir}/references" "${skill_dir}/scripts" "${skill_dir}/templates"
    cp "${SOURCE_ROOT}/dev-md-compactor/SKILL.md" "${skill_dir}/SKILL.md"

    for f in "${SOURCE_ROOT}"/dev-md-compactor/references/*.md; do
      [ -f "$f" ] && cp "$f" "${skill_dir}/references/"
    done

    for f in "${SOURCE_ROOT}"/dev-md-compactor/scripts/*; do
      [ -f "$f" ] && cp "$f" "${skill_dir}/scripts/"
    done

    for f in "${SOURCE_ROOT}"/dev-md-compactor/templates/*; do
      [ -f "$f" ] && cp "$f" "${skill_dir}/templates/"
    done

    INSTALLED_LOCATIONS="${INSTALLED_LOCATIONS}
  + ${skill_dir}"
  done
fi

echo ""
echo "+ Install complete!"
if [ "${SKILL}" = "all" ] || [ "${SKILL}" = "agent-memory" ]; then
  echo "Global memory files : ${AGENT_SYSTEM_PATH}/"
fi
echo "Installed skill locations:${INSTALLED_LOCATIONS}"
echo ""
echo "NEXT STEPS:"
echo "  - Google Antigravity : Skills are active globally in ~/.gemini/config/skills/"
echo "  - dev-md-compactor   : Run /compact-docs or python dev-md-compactor/scripts/run_compactor.py"
echo "  - agent-memory       : Tell the agent 'Bootstrap .agent/ for this project'"
echo ""
