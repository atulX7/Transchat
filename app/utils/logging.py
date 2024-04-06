import logging
import sys
from werkzeug import serving
import re
import os

parent_log_request = serving.WSGIRequestHandler.log_request


def log_setup(app):
    logger = logging.getLogger()

    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler = logging.StreamHandler(sys.stdout)

    dformat = "[%(filename)s:%(lineno)d] :%(levelname)8s: %(message)s"
    handler.setFormatter(logging.Formatter(dformat))
    logger.addHandler(handler)
    log_level = logging.INFO
    if app.debug or os.getenv("DEBUG", False):
        log_level = logging.DEBUG
    logger.setLevel(log_level)

    # Suppress the more verbose modules
    logging.getLogger("botocore").setLevel(logging.WARN)

    logging.info("Log level to %s" % log_level)
    disable_endpoint_logs()


def disable_endpoint_logs():
    """Disable logs for requests to specific endpoints."""

    disabled_endpoints = ("/liveness", "/readiness")

    parent_log_request = serving.WSGIRequestHandler.log_request

    def log_request(self, *args, **kwargs):
        if not any(re.match(f"{de}$", self.path) for de in disabled_endpoints):
            parent_log_request(self, *args, **kwargs)

    serving.WSGIRequestHandler.log_request = log_request
