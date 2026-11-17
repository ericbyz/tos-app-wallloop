#!/usr/bin/env bash
# Fetch pinned upstream wallloop browser-static assets and verify SHA256.
# Usage: ./scripts/fetch_upstream.sh [cache-dir]
#   cache-dir defaults to .upstream-cache (git-ignored).
# Exit non-zero on any version/checksum mismatch.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="${1:-${REPO_ROOT}/.upstream-cache}"
mkdir -p "${CACHE}"

# --- parse UPSTREAM pin (KEY=VALUE lines) ---
PIN_FILE="${REPO_ROOT}/UPSTREAM"
declare -A PIN
while IFS='=' read -r key value; do
    [[ -z "${key}" || "${key}" =~ ^# ]] && continue
    PIN["${key}"]="${value}"
done < "${PIN_FILE}"

TAG="${PIN[UPSTREAM_TAG]:?UPSTREAM_TAG missing}"
BASE_URL="${PIN[UPSTREAM_REPO]:?UPSTREAM_REPO missing}/releases/download/${TAG}"

fetch_one() {
    local platform="$1" asset="$2" expect="$3"
    local url="${BASE_URL}/${asset}"
    local out="${CACHE}/${asset}"

    # Local override: build from a local dist dir without a published release
    if [[ -n "${UPSTREAM_DIST_DIR:-}" && -f "${UPSTREAM_DIST_DIR}/${asset}" ]]; then
        echo "== using local dist asset ${UPSTREAM_DIST_DIR}/${asset}" >&2
        cp "${UPSTREAM_DIST_DIR}/${asset}" "${out}"
    elif [[ -f "${out}" && -f "${out}.verified" && "$(cat "${out}.verified")" == "${expect}" ]]; then
        echo "== ${asset}: cached (sha256 ok)" >&2
    else
        echo "== downloading ${url}" >&2
        curl -fsSL --retry 3 -o "${out}" "${url}"
        local actual
        actual="$(sha256sum "${out}" | cut -d' ' -f1)"
        if [[ "${expect}" == REPLACE_WITH_UPSTREAM_SHA256 || -z "${expect}" ]]; then
            echo "WARNING: no pinned sha256 for ${platform} — recording observed value" >&2
            echo "  observed sha256: ${actual}" >&2
            echo "  (pin it in UPSTREAM before submitting)" >&2
        elif [[ "${actual}" != "${expect}" ]]; then
            echo "ERROR: sha256 mismatch for ${asset}" >&2
            echo "  expected: ${expect}" >&2
            echo "  actual:   ${actual}" >&2
            exit 1
        fi
        printf '%s' "${actual}" > "${out}.verified"
    fi
    printf '%s\n' "${out}"
}

X64_ASSET="${PIN[ASSET_x86_64]:?}"
A64_ASSET="${PIN[ASSET_aarch64]:?}"

X64_FILE=$(fetch_one x86_64 "${X64_ASSET}" "${PIN[SHA256_x86_64]:-}")
A64_FILE=$(fetch_one aarch64 "${A64_ASSET}" "${PIN[SHA256_aarch64]:-}")

echo "FETCHED_X64=${X64_FILE}"
echo "FETCHED_A64=${A64_FILE}"
