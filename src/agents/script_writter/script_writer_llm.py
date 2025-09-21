from db import get_db
from orm.scripts import ScriptOperations
from .prompt import prompt

from typing import TypedDict
from sqlalchemy.orm import Session
from agents.base_llms import openai_llm, OpenAI
from agents.script_writter.prompt import prompt
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, START

class State(TypedDict):
    topic: str
    story: str | None
    script: str | None


class ScriptWriterAgent:
    def __init__(self, story: str, user_id: str, db: Session, topic: str) -> None:
        self.story: str = story
        self.topic: str = topic
        self.user_id: str = user_id
        self.db: Session = db
        self.llm: OpenAI = openai_llm
        self.script_prompt: ChatPromptTemplate = ChatPromptTemplate.from_template(
            prompt
        )
        self.chain = self.script_prompt | self.llm
    
    def generate_script(self, state: State) -> State:
        """
        Generate a short creative story based on the topic using the LLM chain.
        """
        response = self.chain.invoke({"story": state["story"]})
        return {"script": response, "topic": state["topic"], "story": state["story"]}
    
    def add_to_database(self, state: State) -> State:
        """
        Stores the story into a database (placeholder for real integration).
        """
        print("add_to_database called with kwargs:", state)
        print(f"Storing script in the database... (script: {state['script']}...)")
        # Here you would add the logic to store the script in the database
        # For example:
        return {"script": "response", "topic": state["topic"], "story": state["story"]}
    
    def run(self) -> None:
        """
        Executes the full workflow by orchestrating tools via the agent.
        """
        workflow_state = StateGraph(State)
        workflow_state.add_node('Generate Script', self.generate_script)
        workflow_state.add_node('add_to_database', self.add_to_database)

        workflow_state.add_edge(START, 'Generate Script')
        workflow_state.add_edge('Generate Script', 'add_to_database')
        workflow_state.add_edge('add_to_database', END)

        app = workflow_state.compile()
        app.invoke({"topic": self.topic, "story": self.story, "script": None})

        
