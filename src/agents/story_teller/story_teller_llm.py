from .prompt import prompt
from agents.base_llms import State
from sqlalchemy.orm import Session
from langchain_core.prompts import ChatPromptTemplate

from langgraph.graph import StateGraph, END
from src.agents.abstract import ChildAgentABC, logger



class StoryTellerAgent(ChildAgentABC):
    def __init__(self, db: Session, user_id: str):
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


    def generate_story(self, state: State) -> State:
        """
        Generate a short creative story based on the topic using the LLM chain.
        """
        logger.info(f"Generating story from story teller with state {state}")
        state['story'] = "Once upon a time in a distant galaxy..."
        # response = self.chain.invoke({"topic": state["topic"], "characters_count": self.characters_count})
        # print("LLM response:", response)
        # state["story"] = response
        return state


    def add_to_database(self, state: State) -> State:
        """
        Stores the story into a database (placeholder for real integration).
        """
        logger.info(f"Adding to db from story teller with state {state}")
        state['story_id'] = 123  # Placeholder for actual story ID

        # print("add_to_database called with kwargs:", state)
        # print(f"Storing story in the database... (story: {state['story']}...)")
        # story_obj = Story(
        #     user_id=self.user_id,
        #     story_text=state['story']
        # )
        # StoryOperations(self.db).create_story(story_obj)
        # state['story_id'] = story_obj.id
        return state
    

    def run(self, state: State) -> dict:
        """
        Executes the full workflow by orchestrating tools via the agent.
        """
        return self.app.invoke(state)
    
    
    def get_graph(self) -> StateGraph:
        workflow_state = StateGraph(State)
        workflow_state.add_node('generate_story', self.generate_story)
        workflow_state.add_node('add_to_database', self.add_to_database)

        workflow_state.add_edge('generate_story', 'add_to_database')
        workflow_state.add_edge('add_to_database', END)

        workflow_state.set_entry_point('generate_story')
        return workflow_state
    