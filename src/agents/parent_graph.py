from langgraph.graph import StateGraph, END
from src.agents.story_teller.story_teller_llm import StoryTellerAgent
from src.agents.script_writter.script_writer_llm import ScriptWriterAgent
from src.agents.base_llms import State, logger

from src.agents.abstract import ChildAgentABC
from typing import List, Callable



class ParentGraphAgent:
    def __init__(self, db_session, user_id: str, topic:str, characters_count: int = 2):
        self.db_session = db_session
        self.user_id = user_id
        self.topic = topic
        self.characters_count = characters_count  # Default value, can be parameterized
    

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
            agent_instance: ChildAgentABC = agent_cls(user_id=self.user_id, db=self.db_session)
            agent_name = agent_cls.__name__
            agent_instances.append(agent_instance)
            agent_names.append(agent_name)
            logger.info(f"Adding agent class {agent_name} for user - {self.user_id}")
            parent_graph.add_node(agent_name, agent_instance.run)

        # Add edges in a linear chain
        for i in range(len(agent_names) - 1):
            parent_graph.add_edge(agent_names[i], agent_names[i + 1])

        # Set entry and finish points
        if agent_names:
            parent_graph.set_entry_point(agent_names[0])
            parent_graph.set_finish_point(agent_names[-1])

    
    def run(self):
        logger.info("Starting with Stategraph")
        parent_graph = StateGraph(State)
        logger.info(f"Parent Stategraph created for user - {self.user_id}")

        # Instantiate agents
        self._add_child_nodes(parent_graph)
        logger.info(f"Child nodes added for user - {self.user_id}")

        app = parent_graph.compile()
        logger.info(f"Parent graph compiled added for user - {self.user_id}")

        result = app.invoke(
            {
                "topic": self.topic,
                "story": None,
                "script": None,
                "story_id": None
            }
        )
        return result
        
        
