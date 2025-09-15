import os
from langchain_openai import OpenAI



openai_llm: OpenAI = OpenAI(model="gpt-4.1-nano", temperature=0.7)
