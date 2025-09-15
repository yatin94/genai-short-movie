from sqlalchemy.orm import Session


async def call_story_teller_factory(topic: str, user_id: str, characters_count: int, db: Session):
    from agents.story_teller.llm_init import StoryTellerAgent

    teller_obj = StoryTellerAgent(
        topic=topic, user_id=user_id, characters_count=characters_count, db=db
    )
    teller_obj.run()
