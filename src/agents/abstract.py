from abc import ABC, abstractmethod
from langgraph.graph import StateGraph
from langchain_core.prompts import ChatPromptTemplate
from agents.base_llms import openai_llm, State
from log_mechs import get_user_logger

from langchain_core.runnables.base import RunnableSerializable
from langgraph.graph.state import CompiledStateGraph
from typing import List



class ChildAgentABC(ABC):
    agent_index: List = []

    def __init__(self, user_id: str, characters_count: int = 2) -> None:
        self.logger = get_user_logger(user_id)
        self.user_id: str = user_id
        self.app: CompiledStateGraph = self.compile_graph()
        self.characters_count: int = characters_count  # Default value, can be parameterized
        super().__init__()


    def __init_subclass__(cls, index: int, **kwargs) -> None:
        if index in cls.agent_index:
            raise ValueError(f"Agent with index {index} already exists.")
        cls.agent_index.insert(index-1, cls) 
        return super().__init_subclass__(**kwargs)
    

    @property
    def llm(self):
        return openai_llm
    
 
    @property
    @abstractmethod
    def chain(self) -> RunnableSerializable:
        pass

    @property
    @abstractmethod
    def prompt(self) -> ChatPromptTemplate:
        pass    

    @abstractmethod
    def get_graph(self) -> StateGraph:
        pass

    @abstractmethod
    def run(self, state: State) -> dict:
        pass

    def compile_graph(self) -> CompiledStateGraph:
        self.logger.info("Compiling Graph")
        workflow_state = self.get_graph()
        app = workflow_state.compile(debug=True)
        return app