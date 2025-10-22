from time import sleep

from sqlalchemy.orm import Session
from .celery_worker import celery_app
import logging
import time
from src.db import SessionLocal
from src.log_mechs import get_user_logger
from db_ops.logging import UserStateOperations

@celery_app.task
def call_parent_agent_factory(topic: str, user_id: str, characters_count: int, request_id: str) -> bool:
    logger = get_user_logger(request_id)
    db: Session = SessionLocal()

    try:
        logger.info("Background task started for user_id: {}".format(user_id))
        time.sleep(10)
        logger.info("Session created user_id: {}".format(user_id))
        raise Exception("Testing error logging in background task")
        from src.agents.parent_graph import ParentGraphAgent
        parent_obj = ParentGraphAgent(
            db_session=db,
            user_id=user_id,
            characters_count=characters_count,
            topic=topic,
            request_id=request_id
        )
        parent_obj.run()
        logging.info("Background task completed for user_id: {}".format(user_id))
        return True
    except Exception as e:
        logger.error(f"Error in background task for user_id {user_id}: {e}")
        UserStateOperations(db).create_request_state(
            comment="Error raised. Please connect with Admin", 
            user_id=user_id, status="error", 
            request_id=request_id
        )
        raise Exception(f"Background task failed for user_id {user_id}: {e}")