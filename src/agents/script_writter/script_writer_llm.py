from .prompt import prompt

from sqlalchemy.orm import Session
from agents.base_llms import State
from agents.script_writter.prompt import prompt
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, START

from src.agents.abstract import ChildAgentABC, logger



class ScriptWriterAgent(ChildAgentABC):
    def __init__(self, db: Session, user_id: str) -> None:
        self.db: Session = db
        self.user_id: str = user_id
        super().__init__()


    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(
            prompt
        )
    
    @property
    def chain(self):
        return self.prompt | self.llm
    
    def generate_script(self, state: State) -> State:
        """
        Generate a short creative story based on the topic using the LLM chain.
        """
        logger.info(f"Generating script from script writer with state {state}")
        state['script'] = "In a galaxy far, far away..."
        # response = self.chain.invoke({"story": state["story"]})
        # state["script"] = response
        return state

    def add_to_database(self, state: State) -> State:
        """
        Stores the story into a database (placeholder for real integration).
        """
        logger.info(f"Add to database in script writer with state {state}")
        # print("add_to_database called with kwargs:", state)
        # print(f"Storing script in the database... (script: {state['script']}...)")
        # Here you would add the logic to store the script in the database
        # For example:
        return state

    def run(self, state: State) -> dict:
        """
        Executes the full workflow by orchestrating tools via the agent.
        """
        return self.app.invoke(state)

    
    def get_graph(self) -> StateGraph:
        workflow_state = StateGraph(State)
        workflow_state.add_node('generate_script', self.generate_script)
        workflow_state.add_node('add_to_database', self.add_to_database)

        workflow_state.add_edge(START, 'generate_script')
        workflow_state.add_edge('generate_script', 'add_to_database')
        workflow_state.add_edge('add_to_database', END)

        return workflow_state
    


        
