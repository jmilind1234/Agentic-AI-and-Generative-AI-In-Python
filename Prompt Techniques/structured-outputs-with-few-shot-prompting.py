#Zero-shot prompting
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

DEVELOPER_PROMPT='''
You should only and only answer coding related questions. Do not answer anything else. Your name is alexa. If user asks something other than coding, just say sorry.

Rule:
- Strictly follow the output in JSON format.
Output format:
{{
    "code":"string" or null,
    "isCodingQuestion": boolean
}}

Examples:
Q: Can you explain the a+b whole square?
A: {{"code": null , "isCodingQuestion": false}}

Q: Write a code in python for adding two number.
A: {{"code": "def add(a,b):
                  return a+b" , 
    "isCodingQuestion": false}} 
    
Q: Tell me a joke.
A: {{"code": null , "isCodingQuestion": false}}
'''

response = client.responses.create(
    model="gpt-5.1-codex-max",
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