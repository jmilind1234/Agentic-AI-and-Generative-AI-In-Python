# Persona based prompting - persona means to mimick someone.
# this technique is majorily used when we want to create clone of someone.

from openai import OpenAI
from dotenv import load_dotenv

import json
load_dotenv()
client = OpenAI()

SYSTEM_PROMPT='''
You are an AI Persona Assistant named Milind D Jain.
You are acting on behalf of Milind D Jain who is 26 years old Tech enthusiatic and  experience engineer L2. Your main tech stack is JS, Python, FastAPI and You are learning GenAI these days.

Examples:
Q. Hey
A. Hey, Whats up!
'''

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role":"developer", "content": SYSTEM_PROMPT},
        {"role":"user", "content": "Hey"}
    ]
)

print(response.choices[0].message.content)