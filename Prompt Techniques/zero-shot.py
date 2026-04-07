#Zero-shot prompting
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

DEVELOPER_PROMPT="You should only and only answer coding related questions. Do not answer anything else. Your name is alexa. If user asks something other than coding, just say sorry."

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {
            "role": "developer",
            "content": DEVELOPER_PROMPT
        },
        {
            "role": "user",
            "content":"covert the 'snake' to hindi"
        }
    ]
)

print(response.output_text)

# Zero-shot prompting: The model is given a direct question or task without prior examples.