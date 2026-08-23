#!/usr/bin/env python3
"""
Run the attack set against your service.  <- UNIT 8, MILESTONE 2

    python app.py                                   # in one terminal
    python run_attacks.py --set path/to/attack_set  # in another

    python run_attacks.py --set ... --label before
    python run_attacks.py --set ... --label after   # after your improvement

And for Milestone 1, to prove your rate limit works:

    python run_attacks.py --flood 15

That sends 15 submissions from ONE creator_id in a burst and prints the run of
status codes, which is what your README's **Rate Limiting** section asks for.
The attack set can't do this for you: every attack row gets its own creator_id,
so an attack run looks like 44 different callers and never trips a limit.

Sending the whole set by hand would eat the milestone, so this does the sending
and the recording. What it does **not** do is decide whether an attack held or
broke — that judgment is the milestone.

That judgment is yours, and it has to be: whether an evasion "worked" depends
on where you put your thresholds, and two students with different bands will
honestly reach different verdicts on the same input. The `targets` column says
what each attack was going for; you say whether it got there.

The one thing it does decide for you is the unambiguous case. A 500, a
connection drop, or an unhandled exception is **broke** — no threshold makes a
crash acceptable.

Writes `results/attack_run_<date>.md`, which is what you paste into your README.
"""

import argparse
import csv
import datetime as dt
import json
import sys
from pathlib import Path

import config

# Windows consoles often run a codepage that can't print every character in
# this file's help text. Without this, `--help` ends in a UnicodeEncodeError
# traceback instead of the help — which is a miserable first thing to hit.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):  # not a normal text stream
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def load_attacks(folder: Path):
    """
    Read both attack files. Returns (attacks, problems).

    A row that won't parse is skipped and reported rather than raising. One
    stray comma in a file you didn't write should cost you that attack, not
    every other attack in the set.

    `attacks_malformed_requests.csv` may carry two optional columns:

        send_as       `json` (default) parses raw_body and sends it as JSON.
                      `raw` sends raw_body's bytes exactly as written — which
                      is the only way to send JSON that doesn't parse, or an
                      empty body.
        content_type  what to claim it is. Defaults to application/json.
    """
    attacks, problems = [], []

    text_file = folder / "attacks.csv"
    if text_file.exists():
        with text_file.open(encoding="utf-8") as f:
            for n, row in enumerate(csv.DictReader(f), 2):
                try:
                    attacks.append({
                        "id": row["id"],
                        "family": row["family"],
                        "targets": row["targets"],
                        "body": {"text": row["text"],
                                 "creator_id": f"attacker_{row['id']}"},
                    })
                except (KeyError, TypeError) as exc:
                    problems.append(f"attacks.csv line {n}: {exc}")

    request_file = folder / "attacks_malformed_requests.csv"
    if request_file.exists():
        with request_file.open(encoding="utf-8") as f:
            for n, row in enumerate(csv.DictReader(f), 2):
                try:
                    attack = {
                        "id": row["id"],
                        "family": row["family"],
                        "targets": row["targets"],
                    }
                    if (row.get("send_as") or "json").strip().lower() == "raw":
                        attack["raw"] = row["raw_body"]
                        attack["content_type"] = (
                            row.get("content_type") or "application/json"
                        )
                    else:
                        attack["body"] = json.loads(row["raw_body"])
                    attacks.append(attack)
                except (KeyError, TypeError, json.JSONDecodeError) as exc:
                    problems.append(
                        f"attacks_malformed_requests.csv line {n}: {exc}. "
                        f"If the body is meant to be unparseable, set send_as=raw."
                    )

    return attacks, problems


def send(url, attack, timeout):
    """
    One request. Returns (status_code, parsed_body_or_none, error_or_none).

    A crash on the far end is a result, not a reason to stop — the stop rule
    for this milestone is explicit that a service dying partway through is
    something to record and keep going from.
    """
    import requests

    try:
        if "raw" in attack:
            response = requests.post(
                f"{url}/submit",
                data=attack["raw"].encode("utf-8"),
                headers={"Content-Type": attack["content_type"]},
                timeout=timeout,
            )
        else:
            response = requests.post(f"{url}/submit", json=attack["body"],
                                     timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        return None, None, f"{type(exc).__name__}: {exc}"

    try:
        return response.status_code, response.json(), None
    except ValueError:
        return response.status_code, None, f"response wasn't JSON: {response.text[:200]}"


def warn_about_rate_limits(attacks, health):
    """
    Some attacks only mean something against a limiter that's switched on.

    Run those with rate limiting off and every one comes back `200`, which
    reads exactly like the attack failing to get through — the most
    misleading result this tool can produce, because it looks like a pass.
    So say so before the run rather than after.
    """
    needs_limits = sorted({a["family"] for a in attacks
                           if "flood" in a["family"]})
    if not needs_limits:
        return
    if health.get("rate_limiting"):
        return

    print("\n" + "!" * 60, file=sys.stderr)
    print(f"The service says rate limiting is OFF, and this set contains "
          f"{', '.join(needs_limits)}.", file=sys.stderr)
    print("Those attacks will all come back 200 because nothing is counting "
          "them — which\nlooks like they were stopped, and is the opposite of "
          "what it means.", file=sys.stderr)
    print("\nTurn the limiter on first (Milestone 1), then re-run.",
          file=sys.stderr)
    print("!" * 60 + "\n", file=sys.stderr)


def auto_verdict(status, payload, error):
    """
    The only verdicts a script can honestly reach on its own.

    Everything else comes back blank for you to fill in.
    """
    if error and "ConnectionError" in error:
        return "BROKE", "the service stopped responding"
    if error:
        return "BROKE", error[:60]
    if status is None:
        return "BROKE", "no response"
    if status >= 500:
        return "BROKE", f"{status} — unhandled error"
    return "", ""


FLOOD_TEXT = (
    "This is an ordinary submission, sent over and over from the same account "
    "to find out where the rate limit sits. Nothing about the text matters here."
)


def run_flood(args):
    """
    Send N submissions from one creator_id and report the status codes.

    This is Milestone 1's evidence: a run of 200s followed by 429s. It lives
    here rather than in a shell loop because a shell loop is a different
    command on every operating system, and this one isn't.

    If you get no 429 at all, the usual cause is that rate limiting is still
    off — check `GET /health`, which reports it.
    """
    import requests

    print(f"{args.flood} submissions as '{args.creator}' against {args.url}")
    print("The first one is slow while the model loads.\n")

    codes = []
    for i in range(1, args.flood + 1):
        try:
            response = requests.post(f"{args.url}/submit",
                                     json={"text": FLOOD_TEXT,
                                           "creator_id": args.creator},
                                     timeout=args.timeout)
            codes.append(str(response.status_code))
        except Exception as exc:  # noqa: BLE001
            codes.append(type(exc).__name__)
        print(f"  [{i:>2}/{args.flood}] {codes[-1]}")

    run = " ".join(codes)
    limited = sum(1 for c in codes if c == "429")

    print(f"\n{'=' * 60}")
    print(run)
    print(f"{'=' * 60}")
    if limited:
        print(f"\n{limited} of {len(codes)} were rate limited. Paste the run above "
              f"into your README\nunder **Rate Limiting**, and check GET /log "
              f"recorded the rejections.")
    else:
        print("\nNo 429 at all. Either your limit is above "
              f"{len(codes)} a minute, or rate limiting\nis still off — "
              "GET /health tells you which.")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    path = config.RESULTS_DIR / f"flood_{stamp}.md"
    path.write_text(
        f"# Rate limit check\n\n"
        f"- Produced by: `run_attacks.py::run_flood`\n"
        f"- {len(codes)} submissions as `{args.creator}` · "
        f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"- Rate limited: **{limited}**\n\n"
        f"```\n{run}\n```\n",
        encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--set", dest="folder",
                        help="folder holding attacks.csv")
    parser.add_argument("--flood", type=int, metavar="N",
                        help="skip the attack set: send N submissions from one "
                             "creator_id and print the status codes (Milestone 1)")
    parser.add_argument("--creator", default="flood_tester",
                        help="who --flood submits as")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--label", default="", help="e.g. before / after")
    parser.add_argument("--timeout", type=float, default=90.0,
                        help="seconds per request — signal one runs a model, so be generous")
    parser.add_argument("--family", help="run only one family")
    args = parser.parse_args()

    try:
        import requests  # noqa: F401
    except ImportError:
        print("The `requests` package isn't installed.\n"
              "Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    if args.flood:
        run_flood(args)
        return

    if not args.folder:
        print("Give me an attack set: --set path/to/folder\n"
              "Or test your rate limit instead: --flood 15", file=sys.stderr)
        sys.exit(1)

    folder = Path(args.folder)
    attacks, problems = load_attacks(folder)
    if problems:
        print(f"{len(problems)} row(s) in the attack set wouldn't parse and were "
              f"SKIPPED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print("Say so in your write-up — a skipped row is a gap in your run.\n",
              file=sys.stderr)
    if not attacks:
        print(f"No attack files found in {folder}.\n"
              f"Expected attacks.csv — check the path.", file=sys.stderr)
        sys.exit(1)

    if args.family:
        attacks = [a for a in attacks if a["family"] == args.family]

    import requests
    try:
        health = requests.get(f"{args.url}/health", timeout=5).json()
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}.\n"
              f"Start your service first:  python app.py", file=sys.stderr)
        sys.exit(1)

    warn_about_rate_limits(attacks, health)

    print(f"{len(attacks)} attacks against {args.url}")
    print("Signal one runs a model. The first request is slow while it loads;\n"
          "after that, a second or two each.\n")

    rows = []
    for i, attack in enumerate(attacks, 1):
        status, payload, error = send(args.url, attack, args.timeout)
        verdict, note = auto_verdict(status, payload, error)

        payload = payload or {}
        row = {
            "id": attack["id"],
            "family": attack["family"],
            "targets": attack["targets"],
            "status": status,
            "content_id": payload.get("content_id"),
            "creator_id": attack.get("body", {}).get("creator_id"),
            "guess": payload.get("guess"),
            "confidence": payload.get("confidence"),
            "model_score": payload.get("model_score"),
            "style_score": payload.get("style_score"),
            "label": payload.get("label"),
            "error": error,
            "verdict": verdict,
            "note": note,
        }
        rows.append(row)

        mark = verdict or "?"
        print(f"  [{i:>2}/{len(attacks)}] {attack['id']:<6} {attack['family']:<17} "
              f"{str(status):<5} {str(payload.get('guess') or '—'):<8} {mark}")

    write_report(rows, args)


def write_report(rows, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"attack_run_{stamp}{label}.md"

    broke = sum(1 for r in rows if r["verdict"] == "BROKE")
    undecided = sum(1 for r in rows if not r["verdict"])

    lines = [
        f"# Attack run{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_attacks.py::main`",
        "- Service: `app.py::submit`",
        f"- {len(rows)} attacks · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"- Auto-marked BROKE (5xx, crash, no response): **{broke}**",
        f"- Left for you to judge: **{undecided}**",
        "",
        "The Verdict column is blank where a script can't honestly decide. Whether",
        "an evasion worked depends on where you put your thresholds — read the",
        "`targets` column, look at what came back, and write HELD or BROKE yourself.",
        "",
        "Each attack submits as creator_id `attacker_<id>`, and the content_id it",
        "came back with is in the table — either one will match this run against your",
        "audit log when you go looking for the ten entries to paste.",
        "",
        "| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for row in rows:
        score = row["confidence"]
        score_text = f"{score:.3f}" if isinstance(score, (int, float)) else "—"
        targets = row["targets"].replace("|", "\\|")
        lines.append(
            f"| {row['id']} | {row['family']} | {targets} | "
            f"{row['status'] or '—'} | `{row['content_id'] or '—'}` | "
            f"{row['guess'] or '—'} | {score_text} | "
            f"{row['verdict'] or ''} |"
        )

    lines += ["", "---", "", "## By family", ""]
    families = {}
    for row in rows:
        families.setdefault(row["family"], []).append(row)
    lines += ["| Family | Attacks | Auto-BROKE | Left to judge |", "|---|---|---|---|"]
    for family, items in sorted(families.items()):
        auto = sum(1 for r in items if r["verdict"] == "BROKE")
        lines.append(f"| `{family}` | {len(items)} | {auto} | {len(items) - auto} |")

    lines += [
        "",
        "> The **false_positive** family is the one to look at hardest. Those are",
        "> written to be genuine human writing that reads as machine-like. Every one",
        "> your service calls AI is a real writer it would have accused.",
        "",
        "---",
        "",
        "## What came back",
        "",
        "The detail behind the table. Paste the interesting failures into your",
        "README — the ones that show something, not the ten easiest.",
        "",
    ]

    for row in rows:
        lines += [
            f"### {row['id']} — `{row['family']}`",
            "",
            f"*Targeting:* {row['targets']}",
            "",
            "```json",
            json.dumps({k: v for k, v in row.items()
                        if k not in ("targets", "family", "note")}, indent=2),
            "```",
            "",
        ]

    path.write_text("\n".join(lines), encoding="utf-8")

    print(f"\n{'=' * 60}")
    print(f"Wrote {path.relative_to(config.ROOT)}")
    print(f"  auto-marked BROKE: {broke}")
    print(f"  left for you:      {undecided}")
    print(f"{'=' * 60}")
    print("\nNow pull your audit log for the run and paste ten entries into your")
    print("README. Choose the ones that show the interesting failures.")
    print("\n  curl \"http://127.0.0.1:5000/log?limit=200\" > results/audit_extract.json")


if __name__ == "__main__":
    main()
