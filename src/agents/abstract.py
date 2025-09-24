from abc import ABC, abstractmethod
from langgraph.graph import StateGraph
from langchain_core.prompts import ChatPromptTemplate
from src.agents.base_llms import openai_llm, State, logger

from langchain_core.runnables.base import RunnableSerializable
from langgraph.graph.state import CompiledStateGraph



class ChildAgentABC(ABC):

    def __init__(self) -> None:
        self.app: CompiledStateGraph = self.compile_graph()
        super().__init__()

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
        logger.info("Compiling Graph")
        workflow_state = self.get_graph()
        app = workflow_state.compile(debug=True)
        return app