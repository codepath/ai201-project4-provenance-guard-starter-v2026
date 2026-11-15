"""Apply narrow stage timers without replacing the existing service."""
from pathlib import Path

root = Path(__file__).resolve().parent
path = root / 'app.py'
text = path.read_text(encoding='utf-8')
if 'from telemetry import stage' not in text:
    text = text.replace('import uuid\n', 'import uuid\n\nfrom telemetry import stage\n')
    text = text.replace('        model_score = detector.model_signal(text)',
                        '        with stage("model"):\n            model_score = detector.model_signal(text)')
    text = text.replace('    style_score = stylometry.style_signal(text)',
                        '    with stage("style"):\n        style_score = stylometry.style_signal(text)')
    text = text.replace('    confidence = scoring.combine_signals(model_score, style_score)\n    guess, label = scoring.score_to_label(confidence)',
                        '    with stage("combine"):\n        confidence = scoring.combine_signals(model_score, style_score)\n        guess, label = scoring.score_to_label(confidence)')
    text = text.replace('    audit.log_decision(content_id=content_id, creator_id=creator,\n                       guess=guess, model_score=model_score, style_score=style_score,\n                       combined_score=confidence, label=label)',
                        '    with stage("audit"):\n        audit.log_decision(content_id=content_id, creator_id=creator,\n                           guess=guess, model_score=model_score, style_score=style_score,\n                           combined_score=confidence, label=label)')
    path.write_text(text, encoding='utf-8')
