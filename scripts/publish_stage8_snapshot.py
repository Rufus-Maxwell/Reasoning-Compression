#!/usr/bin/env python3
"""Archive Stage 8 evidence to the existing private project. Never delete sources."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime
import zipfile

REPO = "Rufus-Maxwell/Reasoning-Compression"
DEFAULT_PROJECT = "/mnt/ai-storage/Projects/Model_Compression"


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--run", action="store_true", help="Package, upload and verify; default lists candidates only")
    args = parser.parse_args()
    project = Path(args.project).resolve()
    cutoff = datetime(2026, 9, 29).timestamp()
    files = {}

    def add(path, archive_name):
        if not path.is_symlink() and path.is_file() and path.stat().st_mtime >= cutoff:
            files[archive_name] = path

    for root in sorted((project / "results").glob("stage8-*")):
        if root.is_symlink() or not root.is_dir():
            continue
        for path in sorted(root.glob("*.zip")):
            add(path, "Project/" + path.relative_to(project).as_posix())
    extensions = {".py", ".md", ".json", ".toml", ".yaml", ".yml", ".txt", ".sh", ".csv"}
    for root in sorted((project / "experiments").glob("stage8_*")):
        if root.is_symlink() or not root.is_dir():
            continue
        for directory, folders, names in os.walk(root, followlinks=False):
            folders[:] = sorted(n for n in folders if not n.startswith(".") and n != "__pycache__" and not (Path(directory) / n).is_symlink())
            for name in sorted(names):
                path = Path(directory) / name
                if not name.startswith(".") and path.suffix.lower() in extensions:
                    add(path, "Project/" + path.relative_to(project).as_posix())
    for path in sorted((Path.home() / "Downloads").glob("Stage8*.zip")):
        add(path, "Downloads/" + path.name)
    script = Path(__file__).resolve()
    add(script, "Project/scripts/publish_stage8_snapshot.py")
    if not any("stage8-merged-final/stage8_merged_" in name for name in files):
        raise SystemExit("No merged-final results ZIP found. Nothing uploaded.")
    print("Stage 8 archive candidates (on/after 29 September 2026):", flush=True)
    for name, path in sorted(files.items()):
        print(f"  {path.stat().st_size / 1024**2:8.2f} MiB  {name}")
    print(f"{len(files)} files; source files will stay in place.", flush=True)
    if not args.run:
        return
    if not json.loads(gh("repo", "view", REPO, "--json", "isPrivate"))["isPrivate"]:
        raise SystemExit("Repository is not private. Nothing uploaded.")
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    record = project / "archive-records" / ("stage8_" + stamp)
    record.mkdir(parents=True, exist_ok=False)
    archive = record / ("stage8_progress_" + stamp + ".zip")
    manifest = {"created_local": datetime.now().astimezone().isoformat(), "repository": REPO, "files": {}}
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, path in sorted(files.items()):
            before = digest(path)
            if path.suffix.lower() == ".zip":
                with zipfile.ZipFile(path) as source:
                    bad = source.testzip()
                    if bad:
                        raise SystemExit(f"Invalid source archive: {path}: {bad}")
            bundle.write(path, name, compress_type=zipfile.ZIP_STORED if path.suffix.lower() == ".zip" else zipfile.ZIP_DEFLATED)
            if digest(path) != before:
                raise SystemExit(f"File changed while packaging: {path}; nothing uploaded.")
            manifest["files"][name] = {"source": str(path), "sha256": before, "bytes": path.stat().st_size}
        for remote in ("README.md", "docs/project-report-2026-11-04.md"):
            content = gh("api", f"repos/{REPO}/contents/{remote}", "-H", "Accept: application/vnd.github.raw+json")
            name = "GitHub/" + remote
            data = content.encode("utf-8")
            bundle.writestr(name, data)
            manifest["files"][name] = {"source": REPO + "/" + remote, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        bundle.writestr("MANIFEST.json", json.dumps(manifest, indent=2) + "\n")
    with zipfile.ZipFile(archive) as bundle:
        for name, entry in manifest["files"].items():
            h = hashlib.sha256()
            with bundle.open(name) as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(block)
            if h.hexdigest() != entry["sha256"]:
                raise SystemExit(f"Archive verification failed: {name}")
    if archive.stat().st_size >= 2_000_000_000:
        raise SystemExit(f"Archive exceeds this uploader's 2 GB limit; kept locally: {archive}")
    expected = digest(archive)
    checksum = record / "SHA256SUMS.txt"
    checksum.write_text(f"{expected}  {archive.name}\n")
    (record / "INDEX.json").write_text(json.dumps(manifest, indent=2) + "\n")
    notes = record / "RELEASE_NOTES.md"
    notes.write_text("Stage 8 evidence and launcher snapshot, with original folder paths and SHA-256 manifest. Includes the verified merged-model final evaluation and the current project report. Full model weights and Python environments are excluded. Local source files have not been deleted.\n")
    tag = "stage8-results-" + stamp
    print("Uploading to a draft release in the private repository...", flush=True)
    gh("release", "create", tag, str(archive), str(checksum), "--repo", REPO, "--draft", "--title", "Stage 8 results — " + stamp.replace("_", " "), "--notes-file", str(notes))
    print("Downloading the uploaded archive to verify it...", flush=True)
    with tempfile.TemporaryDirectory(prefix="github-verify-", dir=record) as temporary:
        gh("release", "download", tag, "--repo", REPO, "--pattern", archive.name, "--dir", temporary)
        if digest(Path(temporary) / archive.name) != expected:
            raise SystemExit("Downloaded hash mismatch. Release left as draft; all sources retained.")
    gh("release", "edit", tag, "--repo", REPO, "--draft=false")
    print("VERIFIED: https://github.com/" + REPO + "/releases/tag/" + tag)
    print("LOCAL ARCHIVE: " + str(archive))
    print("Local source files and model weights remain in place.")


if __name__ == "__main__":
    main()
