# Import the necessary Python package with the functions.
from langchain_community.chat_models import ChatCohere

from dotenv import load_dotenv, find_dotenv

from crewai import Agent, Task, Crew

import warnings
warnings.filterwarnings('ignore')

import os


_ = load_dotenv(find_dotenv())

# Get Cohere API KEY
cohere_api_key = os.environ.get('COHERE_API_KEY')

# Initialize language model
llm = ChatCohere(
    model='command-r-plus',  # Command R+ as the language model
    temperature=0.7,
    cohere_api_key=cohere_api_key
)


# crewai crewai_tools
if __name__ == '__main__':
    """Creating Agents"""
    # Note: The benefit of using multiple strings :
    #
    # varname = "line 1 of text"
    #           "line 2 of text"
    # versus the triple quote docstring:
    #
    # varname = """line 1 of text
    #              line 2 of text
    #           """
    # is that it can avoid adding those whitespaces and newline characters, making it better formatted to be passed to the LLM.

    # Agent: Planner
    planner = Agent(
        llm=llm,
        role="Content Planner",  # It has been seen that LLMs perform better when they are role playing.
        goal="Plan engaging and factually accurate content on {topic}",
        backstory="You're working on planning a blog article "
                  "about the topic: {topic}."
                  "You collect information that helps the "
                  "audience learn something "
                  "and make informed decisions. "
                  "Your work is the basis for "
                  "the Content Writer to write an article on this topic.",
        allow_delegation=False,
        verbose=True,
    )

    # Agent: Writer
    writer = Agent(
        llm=llm,
        role="Content Writer",
        goal="Write insightful and factually accurate "
             "opinion piece about the topic: {topic}",
        backstory="You're working on a writing "
                  "a new opinion piece about the topic: {topic}. "
                  "You base your writing on the work of "
                  "the Content Planner, who provides an outline "
                  "and relevant context about the topic. "
                  "You follow the main objectives and "
                  "direction of the outline, "
                  "as provide by the Content Planner. "
                  "You also provide objective and impartial insights "
                  "and back them up with information "
                  "provide by the Content Planner. "
                  "You acknowledge in your opinion piece "
                  "when your statements are opinions "
                  "as opposed to objective statements.",
        allow_delegation=False,
        verbose=True
    )

    # Agent Editor
    editor = Agent(
        llm=llm,
        role="Editor",
        goal="Edit a given blog post to align with "
             "the writing style of the organization. ",
        backstory="You are an editor who receives a blog post "
                  "from the Content Writer. "
                  "Your goal is to review the blog post "
                  "to ensure that it follows journalistic best practices,"
                  "provides balanced viewpoints "
                  "when providing opinions or assertions, "
                  "and also avoids major controversial topics "
                  "or opinions when possible.",
        allow_delegation=False,
        verbose=True
    )

    """Creating Tasks"""

    # Task: Plan
    plan = Task(
        description=(
            "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering "
                "their interests and pain points.\n"
            "3. Develop a detailed content outline including "
                "an introduction, key points, and a call to action.\n"
            "4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document "
                        "with an outline, audience analysis, "
                        "SEO keywords, and resources.",
        agent=planner
    )

    # Task: Write
    write = Task(
        description=(
            "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Sections/Subtitles are properly named "
                "in an engaging manner.\n"
            "4. Ensure the post is structured with an "
                "engaging introduction, insightful body, "
                "and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors and "
                "alignment with the brand's voice.\n"
        ),
        expected_output="A well-written blog post "
                        "in markdown format, ready for publication, "
                        "each section should have 2 or 3 paragraphs.",
        agent=writer
    )

    # Task: Edit
    edit = Task(
        description=(
            "Proofread the given blog post for "
            "grammatical errors and "
            "alignment with the brand's voice."
        ),
        expected_output="A well-written blog post in markdown format, "
                        "ready for publication, ",
        agent=editor
    )

    """Creating the Crew"""
    # Create your crew of Agents
    # Pass the tasks to be performed by those agents.
    # Note: For this simple example,
    # the tasks will be performed sequentially (i.e they are dependent on each other),
    # so the order of the task in the list matters.
    # verbose=2 allows you to see all the logs of the execution.

    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[plan, write, edit],
        verbose=True
    )

    """Running the Crew"""
    # Note: LLMs can provide different outputs for they same input,

    result = crew.kickoff(
        inputs={"topic": "Artificial Intelligence"}
    )
