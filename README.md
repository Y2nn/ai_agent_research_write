# CrewAI Multiple AI Agent Systems

### Purposes
- Here, our goal is to create AI Agents to research and write an article.

- Here, our goal is to create AI Agents for a customer support automation.

- Here, our goal is to create AI Agents to automate the planning of an event.

- Here, our goal is to create AI Agents to perform financial analysis.

- Here, our goal is to create AI Agents to build a CV based on a job offer.

### Main Features
- Create Agents
- Create Tasks
- Create the Crew
- Run the Crew

### Popular Models as LLM for your Agents
Hugging Face (HuggingFaceHub endpoint):
```Python
from langchain_community.llms import HuggingFaceHub

# Pass "llm" to your agent function
llm = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token="<HF_TOKEN_HERE>",
    task="text-generation",
)
```

Mistral API:
```Python
OPENAI_API_KEY="your-mistral-api-key"
OPENAI_API_BASE="https://api.mistral.ai/v1"
OPENAI_MODEL_NAME="mistral-small"
```

Cohere:
```Python
from langchain_community.chat_models import ChatCohere
import os

# Initialize language model
os.environ["COHERE_API_KEY"] = "your-cohere-api-key"
# Pass "llm" to your agent function
llm = ChatCohere()
```