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
  PR_BRANCH_NAME
  PR_TITLE
  PR_BODY
)

for var_name in "${required_vars[@]}"; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "Missing required config: ${var_name}" >&2
    exit 1
  fi
done

REPO_ROOT="$(git rev-parse --show-toplevel)"
TARGET_ABS_PATH="${REPO_ROOT}/${TARGET_PATH}"

# Get repository owner and name from git remote
GIT_REMOTE_URL="$(git -C "${REPO_ROOT}" remote get-url origin)"
if [[ "${GIT_REMOTE_URL}" =~ github\.com[:/]([^/]+)/([^/]+)(\.git)?$ ]]; then
  TARGET_OWNER="${BASH_REMATCH[1]}"
  TARGET_REPO="${BASH_REMATCH[2]%.git}"
else
  echo "Failed to parse repository owner/name from git remote: ${GIT_REMOTE_URL}" >&2
  exit 1
fi

tmp_file="$(mktemp)"
PR_FILE_TMP=""
cleanup() {
  rm -f "${tmp_file}" "${PR_FILE_TMP}"
}
trap cleanup EXIT

# Setup curl arguments with authentication
curl_args=(-sS -L)
if [[ -n "${GH_TOKEN:-}" ]]; then
  curl_args+=(-H "Authorization: token ${GH_TOKEN}")
fi

# Download source file
api_url="${GITHUB_API_BASE}/repos/${SOURCE_OWNER}/${SOURCE_REPO}/contents/${SOURCE_PATH}?ref=${SOURCE_BRANCH}"
echo "Downloading source file from ${api_url}"
curl "${curl_args[@]}" -H "Accept: application/vnd.github.v3.raw" "${api_url}" -o "${tmp_file}"

mkdir -p "$(dirname "${TARGET_ABS_PATH}")"

# Configure git user
git -C "${REPO_ROOT}" config user.name "${GIT_AUTHOR_NAME}"
git -C "${REPO_ROOT}" config user.email "${GIT_AUTHOR_EMAIL}"

# Fetch all branches
git -C "${REPO_ROOT}" fetch origin

# Checkout or create PR branch
if git -C "${REPO_ROOT}" rev-parse --verify "${PR_BRANCH_NAME}" >/dev/null 2>&1 || \
   git -C "${REPO_ROOT}" ls-remote --exit-code --heads origin "${PR_BRANCH_NAME}" >/dev/null 2>&1; then
  echo "Branch ${PR_BRANCH_NAME} already exists."
  git -C "${REPO_ROOT}" fetch origin "${PR_BRANCH_NAME}"
  git -C "${REPO_ROOT}" checkout -B "${PR_BRANCH_NAME}" "origin/${PR_BRANCH_NAME}"
else
  echo "Creating new branch ${PR_BRANCH_NAME} from origin/master..."
  git -C "${REPO_ROOT}" checkout -b "${PR_BRANCH_NAME}" "origin/master"
fi

# Check if PR exists
pr_check_url="${GITHUB_API_BASE}/repos/${TARGET_OWNER}/${TARGET_REPO}/pulls?head=${TARGET_OWNER}:${PR_BRANCH_NAME}&state=open"
pr_check_response="$(curl "${curl_args[@]}" -H "Accept: application/vnd.github.v3+json" "${pr_check_url}")"
EXISTING_PR=""
if echo "${pr_check_response}" | grep -q '"number"'; then
  EXISTING_PR="$(echo "${pr_check_response}" | grep -o '"number":[0-9]*' | head -1 | grep -o '[0-9]*')"
fi

if [[ -n "${EXISTING_PR}" ]]; then
  echo "Found existing open PR #${EXISTING_PR}"

  # Compare with PR branch content
  pr_file_url="${GITHUB_API_BASE}/repos/${TARGET_OWNER}/${TARGET_REPO}/contents/${TARGET_PATH}?ref=${PR_BRANCH_NAME}"
  PR_FILE_TMP="$(mktemp)"
  curl "${curl_args[@]}" -H "Accept: application/vnd.github.v3.raw" "${pr_file_url}" -o "${PR_FILE_TMP}" 2>/dev/null || touch "${PR_FILE_TMP}"

  if cmp -s "${tmp_file}" "${PR_FILE_TMP}" 2>/dev/null; then
    echo "Content in existing PR #${EXISTING_PR} is identical to downloaded content. No action needed."
    exit 0
  fi

  echo "Content differs from existing PR. Will update the PR branch."
fi

# Apply new content and check if there are changes
cp "${tmp_file}" "${TARGET_ABS_PATH}"
git -C "${REPO_ROOT}" add "${TARGET_PATH}"

# Check if there are actual changes to commit
if git -C "${REPO_ROOT}" diff --cached --quiet; then
  echo "No changes to commit after staging. Content is already up to date."
  exit 0
fi

# Commit changes
git -C "${REPO_ROOT}" commit -m "${COMMIT_MESSAGE}"

# Push branch (-u is safe even if already set)
echo "Pushing branch ${PR_BRANCH_NAME}..."
git -C "${REPO_ROOT}" push -u origin "${PR_BRANCH_NAME}"

# Create PR if it doesn't exist
if [[ -z "${EXISTING_PR}" ]]; then
  echo "Creating pull request..."

  # Create PR
  pr_data="{\"title\":\"${PR_TITLE}\",\"body\":\"${PR_BODY}\",\"head\":\"${PR_BRANCH_NAME}\",\"base\":\"master\"}"

  pr_url="${GITHUB_API_BASE}/repos/${TARGET_OWNER}/${TARGET_REPO}/pulls"

  http_code="$(curl "${curl_args[@]}" -H "Accept: application/vnd.github.v3+json" \
    -w "%{http_code}" -o /dev/null \
    -X POST -d "${pr_data}" "${pr_url}" 2>&1 || echo "000")"
  http_code="$(echo -n "${http_code}" | tail -c 3)"

  if [[ "${http_code}" == "201" ]]; then
    echo "PR created"
  else
    echo "Failed to create PR (HTTP ${http_code})" >&2
    exit 1
  fi
else
  echo "Updated existing PR #${EXISTING_PR}"
fi
