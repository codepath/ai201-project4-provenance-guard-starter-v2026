#!/usr/bin/env python3
"""
Provenance Guard — the web service.

    python app.py

Then, in another terminal:

    curl -X POST http://127.0.0.1:5000/ping \
      -H "Content-Type: application/json" \
      -d '{"message": "hello"}'

That's the example route. It works right now, before you've written anything.
**Leave it alone** — it's your control. When something breaks later, check that
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself.

Routes:

    POST /ping        the worked example. Already works. Don't edit it
    POST /submit      ← YOU BUILD THIS (Milestone 3, 4, 5)
    POST /appeal      ← YOU BUILD THIS (Milestone 5)
    GET  /log         the audit log. Already works
    GET  /health      is the service up, and is the model loaded
"""

import uuid
import time

from flask import Flask, jsonify, request, g

import audit
import config
import detector
import uuid
import stylometry
import scoring


app = Flask(__name__)

# Unit 9 Capstone: Request timing and structured operational logs.
@app.before_request
def capstone_start_timer():
    if request.path == "/submit":
        g.capstone_start_time = time.perf_counter()


@app.after_request
def capstone_request_timing(response):
    if request.path == "/submit" and hasattr(g, "capstone_start_time"):
        duration_ms = round(
            (time.perf_counter() - g.capstone_start_time) * 1000,
            3
        )

        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}

        submitted_text = payload.get("text")
        input_chars = len(submitted_text) if isinstance(submitted_text, str) else None

        import audit
        try:
            audit.log_operation(
                creator_id=payload.get("creator_id", ""),
                input_chars=input_chars,
                http_status=response.status_code,
                duration_ms=duration_ms
            )
        except OSError:
            app.logger.exception(
                "Operational audit logging failed; preserving HTTP response"
            )

    return response




# ── Rate limiting — UNIT 8 ────────────────────────────────────────────────────
# Off until you turn it on. In unit 8, Milestone 1:
#
#   1. Set RATE_LIMITING_ENABLED = True in config.py (or AI201_RATE_LIMITS=1)
#   2. Choose your numbers there
#   3. Uncomment the @limiter.limit(...) line on /submit below
#
# The order doesn't matter. While limiting is off, that decorator is a no-op
# that quietly does nothing, so uncommenting it early costs you nothing — but
# it also means no 429 until you've done step 1.
#
# The storage backend is preconfigured, which stops Flask-Limiter printing a
# warning on every start. In-memory is right for one laptop and wrong for
# anything real — a restart forgets every count.

class _LimiterOff:
    """
    Stands in for the real limiter while rate limiting is off.

    It makes @limiter.limit(...) a decorator that returns the route
    untouched, so uncommenting the line before you flip the setting is
    harmless instead of a crash on startup.
    """

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()
if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        """
        Who a request counts against.

        Falling back to the caller's address is the easy version. Unit 8's
        stretch asks about per-creator limits instead — and the difference
        matters: one script can look like a thousand callers, and one household
        can look like one.
        """
        payload = request.get_json(silent=True)
        # A body that parses as JSON but isn't an object — a bare list or
        # string — has no .get. Without this guard the key function raises
        # BEFORE the route runs, and a malformed request becomes a 500 that
        # looks like your handler crashed when your handler never ran.
        if not isinstance(payload, dict):
            return get_remote_address()
        creator = payload.get("creator_id")
        return creator if isinstance(creator, str) and creator.strip() else get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        """
        A rejected request still leaves a trace.

        ⚠️ An attack that shows up only as an absence is one you'll never find.
        """
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            payload = {}
        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )
        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# ── The worked example. Already works. Don't edit. ────────────────────────────

@app.post("/ping")
def ping():
    """
    Everything a route needs, in six lines.

    JSON arrives as a dict. You pull things out of it. You return a dict and
    the framework turns it into a response. That's the whole idea.
    """
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Is the service up, and has the model been downloaded yet?"""
    import detector

    loaded = detector._model is not None
    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


# ── YOU BUILD THIS ────────────────────────────────────────────────────────────


@app.post("/submit")
@limiter.limit(
    f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day"
)
def submit():
    """
    Validate submitted text, calculate detection scores,
    record the decision, and return a classification.

    Invalid submissions return HTTP 400 and are logged.
    """

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        audit.log_rejection(
            creator_id="",
            reason="invalid_json"
        )
        return jsonify({
            "error": "invalid_json",
            "message": "Please submit a valid JSON object."
        }), 400

    text = payload.get("text")
    creator_id = payload.get("creator_id", "")

    if not isinstance(creator_id, str):
        creator_id = ""

    # Reject missing, empty, or whitespace-only text.
    if not isinstance(text, str) or not text.strip():
        audit.log_rejection(
            creator_id=creator_id,
            reason="missing_or_empty_text"
        )
        return jsonify({
            "error": "invalid_text",
            "message": "Text is required and cannot be empty."
        }), 400

    # Unit 9: Reject oversized submissions before model inference.
    if len(text) > config.MAX_SUBMISSION_CHARS:
        audit.log_rejection(
            creator_id=creator_id,
            reason="submission_too_large"
        )
        return jsonify({
            "error": "submission_too_large",
            "message": "Submission exceeds the maximum character limit."
        }), 400

    # Unit 9: Reject unsupported control characters.
    if any(ord(char) < 32 and char not in "\\n\\r\\t" for char in text):
        audit.log_rejection(
            creator_id=creator_id,
            reason="unsupported_control_character"
        )
        return jsonify({
            "error": "unsupported_control_character",
            "message": "Submission contains unsupported control characters."
        }), 400

    # Unit 9: Reject submissions without alphabetic words.
    if not any(char.isalpha() for char in text):
        audit.log_rejection(
            creator_id=creator_id,
            reason="no_meaningful_words"
        )
        return jsonify({
            "error": "no_meaningful_words",
            "message": "Submission must contain meaningful words."
        }), 400

    # Preserve the detector's minimum-input requirement.
    if len(text.split()) < 3:
        audit.log_rejection(
            creator_id=creator_id,
            reason="text_too_short"
        )
        return jsonify({
            "error": "text_too_short",
            "message": "Please provide at least three words."
        }), 400

    # Existing Unit 7 detection and scoring logic.
    model_score = detector.model_signal(text)
    style_score = stylometry.style_signal(text)

    combined_score = scoring.combine_signals(
        model_score,
        style_score
    )

    guess, label_text = scoring.score_to_label(combined_score)

    content_id = str(uuid.uuid4())

    # Record the complete classification decision.
    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id,
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label=label_text,
        status="decided"
    )

    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": combined_score,
        "label": label_text,
        "model_score": model_score,
        "style_score": style_score,
        "combined_score": combined_score
    }), 200



@app.post("/appeal")
def appeal():
    """
    Accept an appeal against a previous classification.
    """
    payload = request.get_json(silent=True) or {}
    content_id = payload.get("content_id", "")
    reasoning = payload.get("reasoning", "")

    if not isinstance(content_id, str) or not content_id.strip():
        return jsonify({
            "error": "missing_content_id",
            "message": "Please provide a valid content ID."
        }), 400

    entries = audit.entries_for(content_id)

    if not entries:
        return jsonify({
            "error": "content_not_found",
            "message": "No submission was found with this content ID."
        }), 404

    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({
            "error": "missing_reasoning",
            "message": "Please provide a reason for your appeal."
        }), 400

    audit.log_appeal(
        content_id=content_id,
        creator_id=entries[0].get("creator_id", ""),
        reasoning=reasoning.strip()
    )

    return jsonify({
        "content_id": content_id,
        "status": "under_review",
        "message": "Your appeal has been received and recorded for human review."
    }), 200


# ── Audit log ──────────────────────────────────────────────────────────────

@app.get("/log")
def get_log():
    """
    Return audit log entries, most recent last.
    """
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)

    return jsonify({
        "count": len(entries),
        "entries": entries
    })


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()
    # debug=True hands out an interactive debugger, so it's local-only — see config.py
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
