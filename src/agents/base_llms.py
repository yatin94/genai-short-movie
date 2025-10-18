import os
from langchain_openai import OpenAI, ChatOpenAI
from typing import TypedDict

class State(TypedDict):
    topic: str
    story: str
    story_id: int
    script: list


openai_llm: OpenAI = OpenAI(model="gpt-4.1-nano", temperature=0.7)
chatopenai_llm: ChatOpenAI = ChatOpenAI(model="gpt-5-nano", temperature=0.7)

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)