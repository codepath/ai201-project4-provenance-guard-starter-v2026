"""
gunicorn picks this file up automatically when started from this directory.

Load GPT-2 in each worker before it takes traffic, so the first real /submit
doesn't pay the 12-16 s model load (measured: results/preload_*.md). Set
AI201_PRELOAD=0 to get the old behaviour back, which is how the "before"
numbers were taken.
"""
import os


def post_fork(server, worker):
    if os.getenv("AI201_PRELOAD", "1") == "1":
        import detector
        detector.warm_up()
