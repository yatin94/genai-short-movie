from .prompt import prompt
from agents.base_llms import State
from sqlalchemy.orm import Session
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.string import StrOutputParser

from langgraph.graph import StateGraph, END
from src.agents.abstract import ChildAgentABC, logger
from langchain_community.llms.fake import FakeListLLM
from orm.stories import Story
from db_ops.stories import StoryOperations
from src.db_ops.logging import UserStateOperations


class StoryTellerAgent(ChildAgentABC, index=1):
    def __init__(self, db: Session, user_id: str):
        self.db: Session = db
        self.user_id: str = user_id
        self.fake = True
        UserStateOperations(self.db).create_request_state(comment="Story Writer Agent Initiated.", user_id=self.user_id, status="success")

        super().__init__()
    
    
    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(
            prompt
        )
    
    @property
    def fake_llm(self):
        story_text = """
           In a quiet town, Maya and Tom discovered a hidden ledger revealing corrupt dealings by the town’s officials. Instead of despair, they chose to act. Maya shared the ledger with the community, sparking conversations and awareness. Tom used his skills to verify the information, ensuring their claims were solid. Together, they organized a peaceful rally, encouraging transparency and honesty. Their courage inspired others to stand against corruption. Over time, the town’s leaders became more accountable, and trust was rebuilt. Maya and Tom learned that even small acts of integrity could ignite change, proving that courage and unity are powerful tools against corruption. Their town thrived on honesty, and hope shone brighter than ever.
        """
        return FakeListLLM(responses=[
            story_text
        ], sleep=10)
    
    @property
    def chain(self):
        return self.prompt | self.llm | StrOutputParser()
    
    @property
    def fake_chain(self):
        return self.prompt | self.fake_llm


    def generate_story(self, state: State) -> dict:
        """
        Generate a short creative story based on the topic using the LLM chain.
        """
        logger.info(f"Generating story from story teller with state {state}")
        if self.fake:
            logger.info("Using fake LLM for story generation")
            response = self.fake_chain.invoke({"topic": state["topic"], "characters_count": self.characters_count})
        else:
            response = self.chain.invoke({"topic": state["topic"], "characters_count": self.characters_count})
        logger.info(f"LLM response: {response}")
        UserStateOperations(self.db).create_request_state(comment="Story Generated.", user_id=self.user_id, status="success")

        return {"story": response}


    def add_to_database(self, state: State) -> dict:
        """
        Stores the story into a database (placeholder for real integration).
        """
        logger.info(f"Adding to db from story teller with state {state}")
        story_obj = Story(
            user_id=self.user_id,
            story_text=state['story']
        )
        StoryOperations(self.db).create_story(story_obj)
        UserStateOperations(self.db).create_request_state(comment="Story Added to database.", user_id=self.user_id, status="success")

        return {"story_id": story_obj.id}
    

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
    