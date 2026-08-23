#!/usr/bin/env python3
"""
AI201 environment check.

Run this before every class:

    python test.py

It checks the things that actually break: your Python version, your virtual
environment, your pinned packages, whether the local model has been
downloaded, and whether the starter service answers. It is the same file in
every unit's starter repo — the checks adapt to whatever that unit's
requirements.txt pins.

This pair needs no API key. Nothing here calls a hosted service.

Nothing here touches your project code, and nothing here is graded.
"""

import importlib
import importlib.metadata as md
import os
import platform
import re
import shutil
import sys
from pathlib import Path

# --- Course-wide pins -------------------------------------------------------
# This pair has no hosted model and no API key. The one model it uses runs on
# your machine and is named in config.py.

MIN_PYTHON = (3, 11)
MAX_PYTHON = (3, 14)  # exclusive — 3.14 breaks the pinned stack
MIN_DISK_GB = 9   # torch is most of it; the detector model adds ~550 MB
MIN_RAM_GB = 4

# Distribution name on PyPI -> module name you actually import.
IMPORT_NAMES = {
    "python-dotenv": "dotenv",
    "google-genai": "google.genai",
    "sentence-transformers": "sentence_transformers",
    "rank-bm25": "rank_bm25",
    "rank_bm25": "rank_bm25",
    "scikit-learn": "sklearn",
    "opencv-python": "cv2",
    "pyyaml": "yaml",
    "pillow": "PIL",
    "beautifulsoup4": "bs4",
}

ROOT = Path(__file__).resolve().parent

passed, failed, warned, skipped = [], [], [], []


def report(status, name, detail=""):
    line = f"[{status:<4}] {name}"
    if detail:
        line += f"\n         {detail}"
    print(line)
    {"PASS": passed, "FAIL": failed, "WARN": warned, "SKIP": skipped}[status].append(name)


# --- 1. Python --------------------------------------------------------------

def check_python():
    v = sys.version_info
    actual = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) < MIN_PYTHON:
        return report("FAIL", "Python version", f"Found {actual}. This course needs 3.11 or newer.")
    if (v.major, v.minor) >= MAX_PYTHON:
        return report(
            "FAIL",
            "Python version",
            f"Found {actual}. The pinned packages do not support 3.14 yet — "
            f"install 3.13 and rebuild your virtual environment.",
        )
    report("PASS", "Python version", f"{actual} on {platform.system()}")


def check_venv():
    active = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    if not active:
        return report(
            "FAIL",
            "Virtual environment",
            "Not active. Run the activate command for your OS, then try again. "
            "Installing into your system Python is the most common cause of "
            "'it worked yesterday'.",
        )
    report("PASS", "Virtual environment", sys.prefix)


# --- 2. Packages ------------------------------------------------------------

def parse_requirements(path):
    """Yield (distribution_name, raw_specifier) for each real requirement line."""
    reqs = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#")[0].strip()
        if not line or line.startswith("-"):
            continue
        name = re.split(r"[<>=!~\[;]", line, maxsplit=1)[0].strip()
        if name:
            reqs.append((name, line))
    return reqs


def check_packages():
    req_file = ROOT / "requirements.txt"
    if not req_file.exists():
        return report(
            "FAIL",
            "requirements.txt",
            f"Not found next to test.py. Run this from inside the starter repo folder.",
        )

    missing, wrong = [], []
    for dist, spec in parse_requirements(req_file):
        module = IMPORT_NAMES.get(dist.lower(), dist.replace("-", "_"))
        try:
            importlib.import_module(module)
        except Exception as e:
            missing.append(f"{dist} ({type(e).__name__})")
            continue
        try:
            installed = md.version(dist)
        except md.PackageNotFoundError:
            continue
        if "==" in spec:
            want = spec.split("==")[1].split(",")[0].strip()
            if installed != want:
                wrong.append(f"{dist}: pinned {want}, installed {installed}")

    if missing:
        return report(
            "FAIL",
            "Pinned packages",
            "Could not import: " + ", ".join(missing)
            + "\n         Fix: pip install -r requirements.txt",
        )
    if wrong:
        return report("WARN", "Pinned packages", "; ".join(wrong))
    report("PASS", "Pinned packages", f"all {len(parse_requirements(req_file))} import cleanly")


# --- 3. Machine -------------------------------------------------------------

def total_ram_gb():
    try:
        if hasattr(os, "sysconf") and "SC_PAGE_SIZE" in os.sysconf_names:
            return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024**3
        if sys.platform == "win32":
            import ctypes

            class MemStatus(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]

            stat = MemStatus()
            stat.dwLength = ctypes.sizeof(MemStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return stat.ullTotalPhys / 1024**3
    except Exception:
        pass
    return None


def check_machine():
    free_gb = shutil.disk_usage(ROOT).free / 1024**3
    if free_gb < MIN_DISK_GB:
        report("FAIL", "Free disk space",
               f"{free_gb:.1f} GB free, need about {MIN_DISK_GB} GB. "
               f"PyTorch and the detector model cache are most of it.")
    else:
        report("PASS", "Free disk space", f"{free_gb:.1f} GB")

    ram = total_ram_gb()
    if ram is None:
        report("SKIP", "Memory", "Could not read total RAM on this OS — check manually.")
    elif ram < MIN_RAM_GB:
        report("WARN", "Memory",
               f"{ram:.1f} GB total, {MIN_RAM_GB} GB recommended. Things will run, "
               f"but close other apps while the model is loaded.")
    else:
        report("PASS", "Memory", f"{ram:.1f} GB")


# --- 4. What this pair actually runs ----------------------------------------

def check_torch():
    """Signal one runs a model on this machine."""
    try:
        import torch
    except ImportError:
        return report("FAIL", "PyTorch", "Not installed. Run: pip install -r requirements.txt")
    report("PASS", "PyTorch", torch.__version__)


def check_flask():
    """The web service, and unit 8's rate limiter."""
    try:
        import flask  # noqa: F401
    except ImportError as exc:
        return report("FAIL", "Flask", f"Could not import: {exc}")
    try:
        import flask_limiter  # noqa: F401
    except ImportError:
        return report("WARN", "Flask", "flask-limiter missing — you need it in unit 8")
    report("PASS", "Flask", "flask and flask-limiter both import")


def check_detector_model():
    """Is the ~550 MB model already downloaded?"""
    from pathlib import Path as _P

    cache = _P.home() / ".cache" / "huggingface" / "hub"
    if cache.exists() and any("gpt2" in p.name for p in cache.iterdir()):
        return report("PASS", "Detector model", "already downloaded")
    report(
        "WARN",
        "Detector model",
        "Not downloaded yet (~550 MB). Run `python detector.py` once BEFORE\n"
        "         class — downloading it during the session costs you the breakout.",
    )


def check_service():
    """Does the service start and does the example route answer?"""
    sys.path.insert(0, str(ROOT))
    try:
        import app as appmod
    except Exception as exc:  # noqa: BLE001
        return report("FAIL", "The service", f"app.py wouldn't import: {exc}")

    try:
        client = appmod.app.test_client()
        response = client.post("/ping", json={"message": "check"})
    except Exception as exc:  # noqa: BLE001
        return report("FAIL", "The service", f"/ping raised: {exc}")

    if response.status_code != 200:
        return report("FAIL", "The service", f"/ping returned {response.status_code}")
    report("PASS", "The service", "/ping answers — the starter works before you edit it")


def main():
    print("\nAI201 environment check\n" + "-" * 60)
    check_python()
    check_venv()
    check_packages()
    check_machine()
    check_torch()
    check_flask()
    check_detector_model()
    check_service()

    print("-" * 60)
    print(f"{len(passed)} passed, {len(failed)} failed, "
          f"{len(warned)} to look at, {len(skipped)} skipped\n")
    if failed:
        print("Not ready yet. Fix the FAIL lines above, then run test.py again.")
        print("Still stuck after one honest attempt? Post the whole output in the")
        print("help channel — the day before class, not the morning of.\n")
        return 1
    if skipped:
        print("You're set for what's installed. The skipped checks are packages")
        print("this unit's requirements.txt doesn't pin yet — that's expected.\n")
        return 0
    print("You're set. See you in class.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
