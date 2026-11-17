#!/usr/bin/env bash
# ============================================================
# Build TOS deb packages for wallloop (x86_64 + aarch64)
# ============================================================
# Usage:
#   ./build.sh              # build both platforms
#   ./build.sh x86_64       # build one platform
#   ./build.sh aarch64
#
# Flow: parse UPSTREAM pin -> verify config.ini version -> fetch & verify
# upstream assets -> stage payload -> pack .deb (dpkg-deb if available,
# else scripts/build_deb.py) -> emit build/output/wallloop_<platform>.deb + .sha256
# ============================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${REPO_ROOT}"

BUILD_DIR="build"
OUTPUT_DIR="${BUILD_DIR}/output"
mkdir -p "${OUTPUT_DIR}"

# ---- parse UPSTREAM pin ----
declare -A PIN
while IFS='=' read -r key value; do
    [[ -z "${key}" || "${key}" =~ ^# ]] && continue
    PIN["${key}"]="${value}"
done < UPSTREAM

APP_ID="wallloop"
VERSION="${PIN[UPSTREAM_VERSION]}"
TAG="${PIN[UPSTREAM_TAG]}"

# ---- keep config.ini version in lockstep with the pin ----
CONFIG_VERSION=$(python3 -c "import json; print(json.load(open('config.ini'))['version'])")
if [[ "${CONFIG_VERSION}" != "${VERSION}" ]]; then
    echo "ERROR: config.ini version (${CONFIG_VERSION}) != UPSTREAM version (${VERSION})" >&2
    echo "  run: ./scripts/bump_upstream.sh ${VERSION}   # or update config.ini" >&2
    exit 1
fi

# ---- fetch + verify upstream assets ----
# scripts/fetch_upstream.sh prints FETCHED_X64=/path and FETCHED_A64=/path
EVALS="$(bash scripts/fetch_upstream.sh)"
X64_FILE="$(sed -n 's/^FETCHED_X64=//p' <<< "${EVALS}")"
A64_FILE="$(sed -n 's/^FETCHED_A64=//p' <<< "${EVALS}")"
declare -A ASSET_FILE=( [x86_64]="${X64_FILE}" [aarch64]="${A64_FILE}" )

# platform -> dpkg architecture
platform_to_dpkg() {
    case "$1" in
        x86_64)  echo "amd64" ;;
        aarch64) echo "arm64" ;;
        *) echo "ERROR: unknown platform $1" >&2; exit 1 ;;
    esac
}

# extract bin/wallloop from the upstream release tarball into $2
extract_binary() {
    local archive="$1" dest="$2"
    local member
    member="$(tar -tzf "${archive}" | grep -E '(^|/)bin/wallloop$' | head -1)"
    if [[ -z "${member}" ]]; then
        echo "ERROR: bin/wallloop not found in ${archive}" >&2
        exit 1
    fi
    mkdir -p "$(dirname "${dest}")"
    tar -xzf "${archive}" -O "${member}" > "${dest}"
    chmod 755 "${dest}"
}

build_platform() {
    local platform="$1"
    local dpkg_arch
    dpkg_arch="$(platform_to_dpkg "${platform}")"
    local staging="${BUILD_DIR}/${platform}/staging"

    echo "=== Building ${APP_ID} v${VERSION} for ${platform} (${dpkg_arch}) ==="
    rm -rf "${BUILD_DIR}/${platform}"
    mkdir -p "${staging}/usr/local/${APP_ID}/bin" \
             "${staging}/usr/local/${APP_ID}/images/icons" \
             "${staging}/usr/local/${APP_ID}/init.d" \
             "${staging}/usr/local/${APP_ID}/nginx" \
             "${staging}/usr/share/doc/${APP_ID}" \
             "${staging}/DEBIAN"

    # Debian doc files (copyright/changelog are expected by lintian and by
    # the Apache-2.0 redistribution obligations — see NOTICE)
    cat > "${staging}/usr/share/doc/${APP_ID}/copyright" <<EOF
Format: https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: WallLoop
Upstream-Homepage: ${PIN[UPSTREAM_REPO]}
Source: ${PIN[UPSTREAM_REPO]}

Files: *
Copyright: $(date +%Y) WallLoop contributors
License: Apache-2.0
 The complete text of the Apache-2.0 license is available upstream at
 https://www.apache.org/licenses/LICENSE-2.0 and in the LICENSE file of
 the packaging repository. On Debian systems it can be found in
 /usr/share/common-licenses/Apache-2.0.
EOF
    {
        echo "wallloop (${VERSION}) upstream; urgency=low"
        echo
        echo "  * Built from source ${PIN[UPSTREAM_REPO]} ${TAG} build for TOS (original app, CGO_ENABLED=0 static Go binary).."
        echo "    Binary sha256 pinned in the UPSTREAM file of the packaging repository."
        echo
        echo " -- ericbyz <ericbyz@users.noreply.github.com>  $(date -R)"
    } | gzip -9 > "${staging}/usr/share/doc/${APP_ID}/changelog.gz"

    # application payload
    extract_binary "${ASSET_FILE[${platform}]}" "${staging}/usr/local/${APP_ID}/bin/wallloop"
    install -m 644 config.ini "${staging}/usr/local/${APP_ID}/config.ini"
    install -m 644 wallloop.env    "${staging}/usr/local/${APP_ID}/wallloop.env"
    install -m 644 wallloop.lang   "${staging}/usr/local/${APP_ID}/wallloop.lang"
    install -m 644 images/icons/wallloop.svg "${staging}/usr/local/${APP_ID}/images/icons/wallloop.svg"
    install -m 644 init.d/wallloop.service   "${staging}/usr/local/${APP_ID}/init.d/wallloop.service"
    # platform nginx route (iframe embedded mode: /wallloop/ -> 127.0.0.1:18241)
    install -m 644 nginx/wallloop.conf       "${staging}/usr/local/${APP_ID}/nginx/wallloop.conf"

    # per-platform metadata
    install -m 644 DEBIAN/control "${staging}/DEBIAN/control"
    python3 - "$staging" "${dpkg_arch}" "${platform}" <<'PYEOF'
import json, sys
staging, dpkg_arch, platform = sys.argv[1], sys.argv[2], sys.argv[3]
app_root = f"{staging}/usr/local/wallloop"
cfg = json.load(open(f"{app_root}/config.ini", encoding="utf-8"))
cfg["platform"] = platform
with open(f"{app_root}/config.ini", "w", encoding="utf-8", newline="\n") as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
    f.write("\n")
ctl = open(f"{staging}/DEBIAN/control", encoding="utf-8").read()
import re
ctl = re.sub(r"^Architecture:.*$", f"Architecture: {dpkg_arch}", ctl, flags=re.M)
with open(f"{staging}/DEBIAN/control", "w", encoding="utf-8", newline="\n") as f:
    f.write(ctl)
print(f"  config.ini platform={platform}, control Architecture={dpkg_arch}")
PYEOF

    # maintainer scripts
    for s in postinst prerm postrm; do
        install -m 755 "DEBIAN/${s}" "${staging}/DEBIAN/${s}"
    done

    # ---- pack ----
    local out="${OUTPUT_DIR}/${APP_ID}_${platform}.deb"
    if command -v dpkg-deb >/dev/null 2>&1; then
        dpkg-deb --build --root-owner-group "${staging}" "${out}"
    else
        python3 scripts/build_deb.py --staging "${staging}" --output "${out}"
    fi
    (cd "${OUTPUT_DIR}" && sha256sum "$(basename "${out}")" > "$(basename "${out}").sha256")
    echo "=== done: ${out}"
}

PLATFORMS=("$@")
[[ ${#PLATFORMS[@]} -eq 0 ]] && PLATFORMS=(x86_64 aarch64)
for p in "${PLATFORMS[@]}"; do
    build_platform "${p}"
done

echo
echo "=== Artifacts ==="
ls -lh "${OUTPUT_DIR}"
