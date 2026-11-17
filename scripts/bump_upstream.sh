#!/usr/bin/env bash
# Bump the pinned upstream version: UPSTREAM + config.ini in lockstep.
# Usage: ./scripts/bump_upstream.sh 0.7.0
# After bumping, fill the new asset names + SHA256 into UPSTREAM
# (fetch upstream .sha256 files from the release page), then run ./build.sh
set -euo pipefail

NEW_VERSION="${1:?usage: bump_upstream.sh <version>}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

# UPSTREAM
sed -i "s/^UPSTREAM_TAG=.*/UPSTREAM_TAG=v${NEW_VERSION}/" UPSTREAM
sed -i "s/^UPSTREAM_VERSION=.*/UPSTREAM_VERSION=${NEW_VERSION}/" UPSTREAM
# asset names embed the version (keep upstream naming quirk: x64 vs x86_64)
sed -i "s/^ASSET_x86_64=.*/ASSET_x86_64=ADWALL_${NEW_VERSION}_x64-browser-static.tar.gz/" UPSTREAM
sed -i "s/^ASSET_aarch64=.*/ASSET_aarch64=ADWALL_${NEW_VERSION}_arm64-browser-static.tar.gz/" UPSTREAM
sed -i "s/^SHA256_x86_64=.*/SHA256_x86_64=REPLACE_WITH_UPSTREAM_SHA256/" UPSTREAM
sed -i "s/^SHA256_aarch64=.*/SHA256_aarch64=REPLACE_WITH_UPSTREAM_SHA256/" UPSTREAM

# config.ini
python3 - "$NEW_VERSION" <<'PYEOF'
import json, sys
cfg = json.load(open("config.ini", encoding="utf-8"))
cfg["version"] = sys.argv[1]
with open("config.ini", "w", encoding="utf-8", newline="\n") as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
    f.write("\n")
PYEOF

# DEBIAN/control version
sed -i "s/^Version:.*/Version: ${NEW_VERSION}/" DEBIAN/control

echo "bumped to ${NEW_VERSION}"
echo "NEXT STEPS:"
echo "  1. download upstream .sha256 files for the new release and pin them in UPSTREAM"
echo "     (SHA256_x86_64 / SHA256_aarch64)"
echo "  2. review upstream release notes for breaking changes"
echo "  3. run ./build.sh && ./scripts/validate.py"
echo "  4. commit, tag v${NEW_VERSION} and push to trigger CI"
