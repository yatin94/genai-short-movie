from time import sleep

from sqlalchemy.orm import Session
from .celery_worker import celery_app
import logging
import time
from src.db import SessionLocal
from src.log_mechs import get_user_logger

@celery_app.task
def call_parent_agent_factory(topic: str, user_id: str, characters_count: int):
    try:
        logger = get_user_logger(user_id)
        logger.info("Background task started for user_id: {}".format(user_id))
        time.sleep(10)
        db: Session = SessionLocal()
        logger.info("Session created user_id: {}".format(user_id))
        from src.agents.parent_graph import ParentGraphAgent
        parent_obj = ParentGraphAgent(
            db_session=db,
            user_id=user_id,
            characters_count=characters_count,
            topic=topic
        )
        parent_obj.run()
        logging.info("Background task completed for user_id: {}".format(user_id))
        return True
    except Exception as e:
        logger.error(f"Error in background task for user_id {user_id}: {e}")
        return False