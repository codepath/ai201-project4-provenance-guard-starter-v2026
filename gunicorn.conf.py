"""
How Provenance Guard runs under gunicorn (capstone, shape A).

    gunicorn -c gunicorn.conf.py app:app

Every number here is a decision, not a default:

  workers = 1     Each worker loads its own copy of torch + GPT-2, about 1 GB
                  of RAM, so a second worker doubles the memory. It also splits
                  the in-memory rate-limit counters: with 2 workers the limit
                  of 10 a minute becomes 10 per worker.
  timeout = 120   gunicorn kills a worker that goes silent for this long. The
                  default 30 s is shorter than a cold model load on this
                  laptop, so the first request would be killed.
  warm-up         The model is loaded as the worker starts, so the first real
                  request isn't the slow one.
"""

import config as pg  # not `config`: gunicorn treats that name as a setting

bind = f"{pg.HOST}:{pg.PORT}"
workers = 1
timeout = 120
accesslog = "-"
errorlog = "-"
loglevel = "info"


def post_worker_init(worker):
    """Runs inside the worker once the app is imported: load the model now."""
    import detector

    worker.log.info("warming up %s ...", pg.DETECTOR_MODEL)
    detector.warm_up()
    worker.log.info("model loaded; ready")
