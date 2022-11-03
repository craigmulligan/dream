from flask import current_app


def is_dev():
    return current_app.config.get("DEBUG")
