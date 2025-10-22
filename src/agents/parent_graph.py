from langgraph.graph import StateGraph, END
from orm.users import User
from agents.story_teller.story_teller_llm import StoryTellerAgent
from agents.script_writter.script_writer_llm import ScriptWriterAgent
from agents.base_llms import State
from log_mechs import get_user_logger

from agents.abstract import ChildAgentABC
from typing import List, Callable
from db_ops.logging import UserStateOperations


class ParentGraphAgent:
    def __init__(self, db_session, user_id: str, topic:str, request_id: str, characters_count: int = 2):
        self.logger = get_user_logger(request_id)
        self.db_session = db_session
        self.user_id = user_id
        self.topic = topic
        self.request_id = request_id
        self.characters_count = characters_count  # Default value, can be parameterized
        UserStateOperations(db_session).create_request_state(
            comment="Parent Graph initiated.", 
            user_id=self.user_id, status="success", 
            request_id=self.request_id
        )

    

    def _initiate_child_agents(self):
        for agent_class in ChildAgentABC.agent_index:
            agent: ChildAgentABC  = agent_class(user_id=self.user_id, db=self.db_session)
            yield agent_class.__name__, agent
        
    
    def _add_child_nodes(self, parent_graph: StateGraph):
        all_agents_cls: List[Callable[...]] = ChildAgentABC.agent_index
        agent_instances = []
        agent_names = []

        # Instantiate agents and add nodes
        for agent_cls in all_agents_cls:

            agent_instance: ChildAgentABC = agent_cls(user_id=self.user_id, db=self.db_session, request_id=self.request_id)

            agent_name = agent_cls.__name__

            agent_instances.append(agent_instance)

            agent_names.append(agent_name)

            self.logger.info(f"Adding agent class {agent_name} for user - {self.user_id}")
            parent_graph.add_node(agent_name, agent_instance.run)

        # Add edges in a linear chain
        for i in range(len(agent_names) - 1):
            parent_graph.add_edge(agent_names[i], agent_names[i + 1])

        # Set entry and finish points
        if agent_names:
            parent_graph.set_entry_point(agent_names[0])
            parent_graph.set_finish_point(agent_names[-1])

    
    def run(self):
        self.logger.info("Starting with Stategraph")
        parent_graph = StateGraph(State)
        self.logger.info(f"Parent Stategraph created for user - {self.user_id}")

        # Instantiate agents
        self._add_child_nodes(parent_graph)
        UserStateOperations(self.db_session).create_request_state(
            comment="Children nodes added.", 
            user_id=self.user_id, 
            status="success",
            request_id=self.request_id
            )

        self.logger.info(f"Child nodes added for user - {self.user_id}")

        app = parent_graph.compile()
        self.logger.info(f"Parent graph compiled added for user - {self.user_id}")
        UserStateOperations(self.db_session).create_request_state(
            comment="Parent node Compiled.",
            user_id=self.user_id,
            status="success",
            request_id=self.request_id
        )


        result = app.invoke(
            {
                "topic": self.topic,
            }
        )
        return result
        
        
if __name__ == "__main__":
    from db import SessionLocal
    db = SessionLocal()
    parent_agent = ParentGraphAgent(db_session=db, user_id="user_123", topic="A thrilling adventure in space", request_id="req_456", characters_count=3)
    output = parent_agent.run()
    print("Final Output:", output)
