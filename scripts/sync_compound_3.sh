#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${CONFIG_FILE:-${SCRIPT_DIR}/sync_compound_3.conf}"

if [[ ! -f "${CONFIG_FILE}" ]]; then
  echo "Config file not found: ${CONFIG_FILE}" >&2
  exit 1
fi

# shellcheck source=/dev/null
source "${CONFIG_FILE}"

required_vars=(
  SOURCE_OWNER
  SOURCE_REPO
  SOURCE_BRANCH
  SOURCE_PATH
  TARGET_PATH
  GIT_AUTHOR_NAME
  GIT_AUTHOR_EMAIL
  COMMIT_MESSAGE
  GITHUB_API_BASE
)

for var_name in "${required_vars[@]}"; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "Missing required config: ${var_name}" >&2
    exit 1
  fi
done

REPO_ROOT="$(git rev-parse --show-toplevel)"
TARGET_ABS_PATH="${REPO_ROOT}/${TARGET_PATH}"

tmp_file="$(mktemp)"
cleanup() {
  rm -f "${tmp_file}"
}
trap cleanup EXIT

api_url="${GITHUB_API_BASE}/repos/${SOURCE_OWNER}/${SOURCE_REPO}/contents/${SOURCE_PATH}?ref=${SOURCE_BRANCH}"

curl_args=(-sS -L -H "Accept: application/vnd.github.v3.raw")
if [[ -n "${GH_TOKEN:-}" ]]; then
  curl_args+=(-H "Authorization: token ${GH_TOKEN}")
fi

echo "Downloading source file from ${api_url}"
curl "${curl_args[@]}" "${api_url}" -o "${tmp_file}"

mkdir -p "$(dirname "${TARGET_ABS_PATH}")"

if [[ -f "${TARGET_ABS_PATH}" ]] && cmp -s "${tmp_file}" "${TARGET_ABS_PATH}"; then
  echo "No changes detected. Exiting."
  exit 0
fi

cp "${tmp_file}" "${TARGET_ABS_PATH}"

git -C "${REPO_ROOT}" add "${TARGET_PATH}"

if git -C "${REPO_ROOT}" diff --cached --quiet; then
  echo "No changes to commit after staging. Exiting."
  exit 0
fi

git -C "${REPO_ROOT}" config user.name "${GIT_AUTHOR_NAME}"
git -C "${REPO_ROOT}" config user.email "${GIT_AUTHOR_EMAIL}"
git -C "${REPO_ROOT}" commit -m "${COMMIT_MESSAGE}"
git -C "${REPO_ROOT}" push origin master
