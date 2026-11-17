#!/usr/bin/env python3
"""Minimal dpkg-deb-compatible .deb packer (pure stdlib).

Produces the standard Debian binary package format:
    ar archive { debian-binary, control.tar.gz, data.tar.xz }

Why not dpkg-deb: this project must build identically on Windows dev
machines (no dpkg) and in CI. The output is a normal deb accepted by
dpkg -i, dpkg-deb -c/-I and lintian.

Determinism rules:
  - fixed mtime (SOURCE_DATE_EPOCH if set, else 0)
  - sorted entry order, dirs before their contents
  - fixed uid/gid 0, uname/gname root
  - rule-based permissions (bin/* and maintainer scripts 0755, rest 0644)
    so the build does not depend on host umask or git checkout flags
"""
import argparse
import io
import lzma
import os
import stat
import sys
import tarfile
import time

EXECUTABLE_RULES = (
    "bin/",  # application binaries
)
MAINT_SCRIPTS = {"preinst", "postinst", "prerm", "postrm", "config"}
DIR_MODE = 0o755
FILE_MODE = 0o644
EXEC_MODE = 0o755


def _mtime() -> int:
    v = os.environ.get("SOURCE_DATE_EPOCH")
    return int(v) if v and v.isdigit() else 0


def _is_exec(rel: str) -> bool:
    name = os.path.basename(rel)
    if name in MAINT_SCRIPTS:
        return True
    return any(rel.startswith(p) or f"/{p}" in rel for p in EXECUTABLE_RULES)


def _add_tree(tf: tarfile.TarFile, root: str, arc_prefix: str) -> None:
    """Add `root` dir tree into tar with names `arc_prefix/<rel>` (arc_prefix like './DEBIAN')."""
    all_entries = []
    for cur, dirs, files in os.walk(root):
        dirs.sort()
        for d in dirs:
            all_entries.append(("dir", os.path.join(cur, d)))
        for f in sorted(files):
            all_entries.append(("file", os.path.join(cur, f)))
    all_entries.sort(key=lambda e: e[1])

    mtime = _mtime()
    for kind, abs_path in all_entries:
        rel = os.path.relpath(abs_path, root).replace(os.sep, "/")
        arc = f"{arc_prefix}/{rel}"
        info = tarfile.TarInfo(arc)
        info.mtime = mtime
        info.uid = 0
        info.gid = 0
        info.uname = "root"
        info.gname = "root"
        if kind == "dir":
            info.type = tarfile.DIRTYPE
            info.mode = DIR_MODE
            info.size = 0
            tf.addfile(info)
        else:
            st = os.stat(abs_path)
            info.size = st.st_size
            info.mode = EXEC_MODE if _is_exec(rel) else FILE_MODE
            with open(abs_path, "rb") as f:
                tf.addfile(info, f)


def _ar_header(name: str, size: int) -> bytes:
    hdr = f"{name:<16}{_mtime():<12}{'0':<6}{'0':<6}{'100644':<8}{size:<10}".encode("ascii")
    assert len(hdr) == 58, len(hdr)
    return hdr + b"\x60\x0a"  # 60 bytes total


def gzip_bytes(data: bytes) -> bytes:
    import gzip as _gzip

    out = io.BytesIO()
    with _gzip.GzipFile(fileobj=out, mode="wb", mtime=0) as g:
        g.write(data)
    return out.getvalue()


def build_deb(staging: str, output: str) -> None:
    debian_dir = os.path.join(staging, "DEBIAN")
    if not os.path.isdir(debian_dir):
        raise SystemExit(f"ERROR: {debian_dir} not found in staging directory")

    # control member: dpkg expects control files at the tar ROOT
    # (./control, ./postinst, ...) — NOT under a ./DEBIAN prefix
    control_buf = io.BytesIO()
    with tarfile.open(fileobj=control_buf, mode="w", format=tarfile.GNU_FORMAT) as tf:
        root_info = tarfile.TarInfo("./")
        root_info.type = tarfile.DIRTYPE
        root_info.mode = DIR_MODE
        root_info.mtime = _mtime()
        root_info.uid = root_info.gid = 0
        root_info.uname = root_info.gname = "root"
        tf.addfile(root_info)
        _add_tree(tf, debian_dir, ".")
    control_gz = gzip_bytes(control_buf.getvalue())

    # data member: everything except DEBIAN, rooted at ./
    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode="w", format=tarfile.GNU_FORMAT) as tf:
        root_info = tarfile.TarInfo("./")
        root_info.type = tarfile.DIRTYPE
        root_info.mode = DIR_MODE
        root_info.mtime = _mtime()
        root_info.uid = root_info.gid = 0
        root_info.uname = root_info.gname = "root"
        tf.addfile(root_info)
        for entry in sorted(os.listdir(staging)):
            if entry == "DEBIAN":
                continue
            abs_path = os.path.join(staging, entry)
            if os.path.isdir(abs_path):
                dir_info = tarfile.TarInfo(f"./{entry}")
                dir_info.type = tarfile.DIRTYPE
                dir_info.mode = DIR_MODE
                dir_info.mtime = _mtime()
                dir_info.uid = dir_info.gid = 0
                dir_info.uname = dir_info.gname = "root"
                tf.addfile(dir_info)
                _add_tree(tf, abs_path, f"./{entry}")
            else:
                info = tarfile.TarInfo(f"./{entry}")
                st = os.stat(abs_path)
                info.size = st.st_size
                info.mode = FILE_MODE
                info.mtime = _mtime()
                info.uid = info.gid = 0
                info.uname = info.gname = "root"
                with open(abs_path, "rb") as f:
                    tf.addfile(info, f)
    filters = [{"id": lzma.FILTER_LZMA2, "preset": 6}]
    data_xz = lzma.compress(data_buf.getvalue(), format=lzma.FORMAT_XZ, filters=filters)

    members = [
        ("debian-binary", b"2.0\n"),
        ("control.tar.gz", control_gz),
        ("data.tar.xz", data_xz),
    ]
    with open(output, "wb") as out:
        out.write(b"!<arch>\n")
        for name, payload in members:
            out.write(_ar_header(name, len(payload)))
            out.write(payload)
            if len(payload) % 2:
                out.write(b"\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--staging", required=True, help="staging dir containing DEBIAN/ and payload")
    ap.add_argument("--output", required=True, help="output .deb path")
    args = ap.parse_args()
    t0 = time.time()
    build_deb(args.staging, args.output)
    size = os.path.getsize(args.output)
    print(f"built {args.output} ({size/1024/1024:.1f} MB) in {time.time()-t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
