from langchain.prompts import PromptTemplate

from db import get_db
from .prompt import prompt
from agents.base_llms import openai_llm
from langchain.chains.llm import LLMChain
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType





class StoryTellerAgent:
    def __init__(self, topic: str, user_id: str, characters_count: int = 2):
        self.topic = topic
        self.user_id = user_id
        self.characters_count = characters_count
        
        # Step 1: Define the prompt template for storytelling
        self.story_prompt = PromptTemplate(
            input_variables=["topic", "characters_count"],
            template=prompt,
        )

        # Step 2: Define the LLM chain for generating stories
        self.story_chain = LLMChain(llm=openai_llm, prompt=self.story_prompt)

        # Step 3: Wrap core functionalities inside tools
        self.tools = [
            Tool(
                name="Generate Story",
                func=self.generate_story,
                description="Generate a short story based on the provided topic."
            ),
            Tool(
                name="Calculate Word Count",
                func=self.calculate_word_count,
                description="Calculate the total word count of the story."
            ),
            Tool(
                name="Store Story in Database",
                func=self.add_to_database,
                description="Store the generated story in a database for later use."
            ),
        ]

        # Step 4: Initialize an agent to orchestrate the tools
        self.agent = initialize_agent(
            tools=self.tools,
            llm=openai_llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # React Agent lets it reason and select tools dynamically
            verbose=True
        )

    def generate_story(self) -> str:
        """
        Generate a short creative story based on the topic using the LLM chain.
        :param: None
        :return: Generated story text.
        """
        return self.story_chain.run(topic=self.topic, characters_count=self.characters_count)

    def calculate_word_count(self, story: str) -> int:
        """
        Calculate the word count of the given story.
        :param story: Story text.
        :return: Word count.
        """
        return len(story.split())

    def add_to_database(self, story: str) -> str:
        """
        Stores the story into a database (placeholder for real integration).
        :param story: The story text to store.
        :return: Confirmation message.
        """
        # Placeholder: Actual database logic should be implemented here (e.g., using SQLite, MongoDB, etc.)
        print(f"Storing story in the database... (story: {story[:50]}...)")
        db = get_db()
        return "Story successfully stored in database."

    def run(self):
        """
        Executes the full workflow by orchestrating tools via the agent.
        """
        # Use the agent to execute tasks step by step
        final_result = self.agent.run(
            f"Create a short story about '{self.topic}', calculate its word count, and store the story in the database."
        )
        return final_result