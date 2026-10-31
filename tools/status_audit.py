#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check that the Nemo repository describes its current status accurately."""
from pathlib import Path
import os
import subprocess

root = Path(__file__).resolve().parents[1]
readme = (root / "README.md").read_text()
profile = (root / "nemo-hardware.conf").read_text()
for phrase in [
    "does not yet contain a buildable UEFI firmware package",
    "not yet HakiOS-compatible",
    "No CI job can prove physical memory handoff",
    "Roadmap",
    "not an EDK II build",
]:
    if phrase.lower() not in readme.lower():
        raise SystemExit(f"README is missing a required status statement: {phrase}")
for field in ["model: RMX2001", "codename: Nemo", "memory_map: unknown", "gop: unavailable_or_unverified", "hakiOS_compatibility: no"]:
    if field not in profile:
        raise SystemExit(f"Nemo profile is missing or misstates: {field}")
try:
    tracked = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"]).decode().split("\0")
except subprocess.CalledProcessError as exc:
    raise SystemExit("This audit must run in a Git checkout") from exc
forbidden = {".fd", ".efi", ".img", ".bin", ".dtb", ".dtbo"}
artifacts = [p for p in tracked if p and (Path(p).suffix.lower() in forbidden or p.startswith("Build/"))]
if artifacts:
    raise SystemExit("Do not track unverified firmware/device artifacts: " + ", ".join(artifacts))
report = (
    "## Nemo UEFI status audit\n\n"
    "Repository claims and artifact hygiene checked. This is a documentation audit only; no UEFI firmware was built, emulated, or tested on Nemo.\n"
)
summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a", encoding="utf-8") as stream:
        stream.write(report)
print(report)
