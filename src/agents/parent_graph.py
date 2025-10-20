from langgraph.graph import StateGraph, END
from orm.users import User
from src.agents.story_teller.story_teller_llm import StoryTellerAgent
from src.agents.script_writter.script_writer_llm import ScriptWriterAgent
from src.agents.base_llms import State
from src.log_mechs import get_user_logger

from src.agents.abstract import ChildAgentABC
from typing import List, Callable
from src.db_ops.logging import UserStateOperations


class ParentGraphAgent:
    def __init__(self, db_session, user_id: str, topic:str, characters_count: int = 2):
        self.logger = get_user_logger(user_id)
        self.db_session = db_session
        self.user_id = user_id
        self.topic = topic
        self.characters_count = characters_count  # Default value, can be parameterized
        UserStateOperations(db_session).create_request_state(comment="Parent Graph initiated.", user_id=self.user_id, status="success")

    

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
            self.logger.info(f"here - {self.user_id}")

            agent_instance: ChildAgentABC = agent_cls(user_id=self.user_id, db=self.db_session)
            self.logger.info(f"here2 - {self.user_id}")

            agent_name = agent_cls.__name__
            self.logger.info(f"here3 - {self.user_id}")

            agent_instances.append(agent_instance)
            self.logger.info(f"here4 - {self.user_id}")

            agent_names.append(agent_name)
            self.logger.info(f"here5 - {self.user_id}")

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
        UserStateOperations(self.db_session).create_request_state(comment="Children nodes added.", user_id=self.user_id, status="success")

        self.logger.info(f"Child nodes added for user - {self.user_id}")

        app = parent_graph.compile()
        self.logger.info(f"Parent graph compiled added for user - {self.user_id}")
        UserStateOperations(self.db_session).create_request_state(comment="Parent node Compiled.", user_id=self.user_id, status="success")


        result = app.invoke(
            {
                "topic": self.topic,
            }
        )
        return result
        
        
