from db import get_db
from orm.stories import StoryOperations, Story
from .prompt import prompt
from agents.base_llms import openai_llm
from langchain.chains.llm import LLMChain
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from sqlalchemy.orm import Session
from langchain_openai import OpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict

from langgraph.graph import StateGraph, END, START
class State(TypedDict):
    topic: str
    story: str | None
    characters_count: int | None

class StoryTellerAgent:
    def __init__(self, topic: str, user_id: str, db: Session, characters_count: int = 2):
        self.topic: str = topic
        self.user_id: str = user_id
        self.characters_count: int = characters_count
        self.db: Session = db
        self.llm: OpenAI = openai_llm
        self.story_prompt: ChatPromptTemplate = ChatPromptTemplate.from_template(
            prompt
        )
        self.chain = self.story_prompt | self.llm


    def generate_story(self, state: State) -> State:
        """
        Generate a short creative story based on the topic using the LLM chain.
        """
        response = self.chain.invoke({"topic": state["topic"], "characters_count": self.characters_count})
        print("LLM response:", response)
        with open("latest_story.txt", "w") as f:
            f.write(response)
        return {"story": response, "topic": state["topic"], "characters_count": self.characters_count}
    
    def add_to_database(self, state: State) -> State:
        """
        Stores the story into a database (placeholder for real integration).
        """
        print("add_to_database called with kwargs:", state)
        print(f"Storing story in the database... (story: {state['story']}...)")
        story_obj = Story(
            user_id=self.user_id,
            story_text=state['story']
        )
        StoryOperations(self.db).create_story(story_obj)
        return state
    
    def run(self):
        """
        Executes the full workflow by orchestrating tools via the agent.
        """
        workflow_state = StateGraph(State)
        workflow_state.add_node('Generate Story', self.generate_story)
        workflow_state.add_node('add_to_database', self.add_to_database)

        workflow_state.add_edge('Generate Story', 'add_to_database')
        workflow_state.add_edge('add_to_database', END)

        workflow_state.set_entry_point('Generate Story')

        app = workflow_state.compile()
        app.invoke({"topic": self.topic, "story": None, "characters_count": self.characters_count})


# class StoryTellerAgent:
#     def __init__(self, topic: str, user_id: str, db: Session, characters_count: int = 2):
#         self.topic = topic
#         self.user_id = user_id
#         self.characters_count = characters_count
#         self.db = db
        
#         # Step 1: Define the prompt template for storytelling
#         self.story_prompt = PromptTemplate(
#             input_variables=["topic", "characters_count"],
#             template=prompt,
#         )
        
#         # Step 2: Define the LLM chain for generating stories
#         self.story_chain = LLMChain(llm=openai_llm, prompt=self.story_prompt)
        
#         # Step 3: Wrap core functionalities inside tools
#         self.tools = [
#             Tool(
#                 name="Generate Story",
#                 func=self.generate_story,
#                 description="Generate a short story based on the provided topic."
#             ),
#             Tool(
#                 name="Store Story in Database",
#                 func=self.add_to_database,
#                 description="Store the generated story in a database for later use."
#             ),
#         ]
        
#         # Step 4: Initialize an agent to orchestrate the tools
#         self.agent = initialize_agent(
#             tools=self.tools,
#             llm=openai_llm,
#             agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#             verbose=True
#         )
        

    
#     def calculate_word_count(self, story: str) -> int:
#         """
#         Calculate the word count of the given story.
#         """
#         return len(story.split())
    
#     def add_to_database(self, *args, **kwargs) -> str:
#         """
#         Stores the story into a database (placeholder for real integration).
#         """
#         print("add_to_database called with kwargs:", kwargs)
#         print("add_to_database called with args:", args)
#         story = "test"
#         print(f"Storing story in the database... (story: {story[:50]}...)")
#         story_obj = Story(
#             user_id=self.user_id,
#             story_text=story
#         )
#         StoryOperations(self.db).create_story(story_obj)
#         return "Story successfully stored in database."
    
