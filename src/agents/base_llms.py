import os
from langchain_openai import OpenAI
from typing import TypedDict


class State(TypedDict):
    topic: str
    story: str | None
    story_id: int | None
    script: str | None


openai_llm: OpenAI = OpenAI(model="gpt-4.1-nano", temperature=0.7)


import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)