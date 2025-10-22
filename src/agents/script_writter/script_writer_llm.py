from .prompt import prompt

from sqlalchemy.orm import Session
from agents.base_llms import State
from agents.script_writter.prompt import prompt
from agents.script_writter.prompt2 import prompt as prompt2
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, START

from agents.abstract import ChildAgentABC

from langchain_core.output_parsers.json import JsonOutputParser
from langchain_community.llms.fake import FakeListLLM
import json
from db_ops.scripts import SceneOperations
from schemas.scripts import CreateScript
from db_ops.logging import UserStateOperations




class ScriptWriterAgent(ChildAgentABC, index=2):
    def __init__(self, db: Session, user_id: str, request_id: str) -> None:
        self.db: Session = db
        self.fake = True
        UserStateOperations(self.db).create_request_state(comment="Script Agent initialised", user_id=user_id, status="success", request_id=request_id)
        super().__init__(user_id=user_id, request_id=request_id)


    @property
    def prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_template(
            prompt2
        )
    
    @property
    def chain(self):
        return self.prompt | self.llm | JsonOutputParser()
    
    @property
    def fake_llm(self):
        with open("final_script.json", "r") as f:
            script_list = json.loads(f.read())
        responses = [json.dumps(scene) for scene in script_list]
        return FakeListLLM(responses=responses, sleep=10)
    
    @property
    def fake_chain(self):
        return self.prompt | self.fake_llm | JsonOutputParser()
    
    
    def generate_script(self, state: State) -> dict:
        """
        Generate a short movie script based on the story using the LLM chain.
        """
        self.logger.info(f"Generating script from script writer with state {state}")
        generated_scenes = []
        prompt_input = {"story": state["story"], "generated_scenes": generated_scenes, "next_scene_number": 1}
        chain = self.chain if not self.fake else self.fake_chain
        for scene_num in range(1, 4):
            prompt_input["generated_scenes"] = json.dumps(generated_scenes)
            prompt_input["next_scene_number"] = scene_num
            response = chain.invoke(prompt_input)
            generated_scenes.append(response)
            self.logger.info(f"Generated scene {scene_num}: {response}")
            prompt_input['next_scene_number'] += 1

        UserStateOperations(self.db).create_request_state(comment="Script generated", user_id=self.user_id, status="success", request_id=self.request_id)
        return {"script": generated_scenes }

    def add_to_database(self, state: State) -> dict:
        """
        Stores the story into a database (placeholder for real integration).
        """
        self.logger.info(f"Add to database in script writer with state {state}")
        with open("final_script.json", "w") as f:
            json.dump(state["script"], f, indent=4)
        script_ops = SceneOperations(self.db)
        for script_scene in state["script"]:
            self.logger.info(f"Storing scene {script_scene['scene_number']} in the database...")
            script_obj = CreateScript(
                story_id=state["story_id"],
                scene_number=script_scene["scene_number"],
                dialogues=script_scene["dialogue"]
            )
            script_ops.create_script(script_data=script_obj)
        UserStateOperations(self.db).create_request_state(comment="Script Added to database", user_id=self.user_id, status="success", request_id=self.request_id)
        
        return {}

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
    


        
