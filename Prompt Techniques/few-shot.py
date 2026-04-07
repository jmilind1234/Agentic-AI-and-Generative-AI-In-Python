#Zero-shot prompting
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

DEVELOPER_PROMPT='''
You should only and only answer coding related questions. Do not answer anything else. Your name is alexa. If user asks something other than coding, just say sorry.

Examples:
Q: Can you explain the a+b whole square?
A: Sorry, I can help only with coding related questions.

Q: Write a code in python for adding two number.
A: def add(a,b):
    return a+b
    
Q: Tell me a joke.
A: Sorry, I can help only with coding related questions.
'''

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {
            "role": "developer",
            "content": DEVELOPER_PROMPT
        },
        {
            "role": "user",
            "content":"solve the equation a plus b the whole cube."
        }
    ]
)

print(response.output_text)

# few-shot prompting: The model is given question or task after some examples.