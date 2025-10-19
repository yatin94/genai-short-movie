from sqlalchemy.orm import Session
import logging

# async def call_story_teller_factory(topic: str, user_id: str, characters_count: int, db: Session):
#     from src.agents.story_teller.story_teller_llm import StoryTellerAgent

#     teller_obj = StoryTellerAgent(
#         topic=topic, user_id=user_id, characters_count=characters_count, db=db
#     )
#     teller_obj.run()


async def call_parent_agent_factory(topic: str, user_id: str, characters_count: int, db: Session):    
    from src.agents.parent_graph import ParentGraphAgent
    parent_obj = ParentGraphAgent(
        db_session=db,
        user_id=user_id,
        characters_count=characters_count,
        topic=topic
    )
    parent_obj.run()
    logging.info("Background task completed for user_id: {}".format(user_id))