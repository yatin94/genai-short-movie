from langgraph.graph import StateGraph, END
from src.agents.story_teller.story_teller_llm import StoryTellerAgent
from src.agents.script_writter.script_writer_llm import ScriptWriterAgent
from src.agents.base_llms import State, logger

from src.agents.abstract import ChildAgentABC




class ParentGraphAgent:
    def __init__(self, db_session, user_id: str, topic:str, characters_count: int = 2):
        self.db_session = db_session
        self.user_id = user_id
        self.topic = topic
        self.characters_count = characters_count  # Default value, can be parameterized
    
    def _get_child_graphs(self):
        child_graphs = {
            'story_teller_agent': StoryTellerAgent,
            'script_writer_agent': ScriptWriterAgent
        }
        return child_graphs

    def _initiate_child_agents(self):
        for agent_name, agent_class in self._get_child_graphs().items():
            agent: ChildAgentABC  = agent_class(user_id=self.user_id, db=self.db_session)
            yield agent_name, agent

    def _add_child_nodes(self, parent_graph: StateGraph):
        first_agent_name = None
        last_agent_name = None
        for agent_name, agent in self._initiate_child_agents():
            logger.info(f"Adding agent class {agent_name} for user - {self.user_id}")

            parent_graph.add_node(agent_name, agent.run)

            if first_agent_name is None:
                first_agent_name = agent_name
            if last_agent_name is not None:
                parent_graph.add_edge(last_agent_name, agent_name)
                last_agent_name = agent_name
            elif not last_agent_name and agent_name != first_agent_name:
                parent_graph.add_edge(first_agent_name, agent_name)
                last_agent_name = agent_name
        
        parent_graph.set_entry_point(first_agent_name)
        if not last_agent_name:
            parent_graph.set_finish_point(last_agent_name) 

    
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
        
        
