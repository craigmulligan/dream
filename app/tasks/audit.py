import logging
from app.database import celery


@celery.task
def audit_log(event_name, user_id):
    logging.info(f"New Event: {event_name}, {user_id}")
    return
