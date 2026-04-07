#chain of thought prompting
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import json
load_dotenv()
client = OpenAI()

DEVELOPER_PROMPT='''
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps. Once you think enough PLAN has been done, finally you can give an output.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

Output JSON Format:

{"step":"START" | "PLAN" | "OUTPUT", "content" : "string"}

Example: 
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN : {"step":"PLAN", "content": "seemslike useris interested in mathematics problem"}
PLAN : {"step":"PLAN", "content": "seems like useris interested in mathematics problem"}
PLAN : {"step":"PLAN", "content": "looking at the problem, we should solve this using BODMAS method"}
PLAN : {"step":"PLAN", "content": "Yes, the BODMAS is correct thing to be done here"}
PLAN : {"step":"PLAN", "content": "first we should divide 5 by 10"}
PLAN : {"step":"PLAN", "content": "now new equation is 2 + 3 * 0.5"}
PLAN : {"step":"PLAN", "content": "now we should carry out the multiplication operation of 3 and 0.5"}
PLAN : {"step":"PLAN", "content": "now new equation is 2 + 1.5"}
PLAN : {"step":"PLAN", "content": "now we have to add 2 and 1.5"}
PLAN : {"step":"PLAN", "content": "finally lets add them"}
PLAN : {"step":"PLAN", "content": "Great, we have solved the equation and finally left with 3.5 as answer"}
OUTPUT: {"step":"OUTPUT", "content": "3.5"}
'''




print("\n\n\n")

user_query = input("👉")
    



message_history = [{
            "role": "developer",
            "content": DEVELOPER_PROMPT
        },{
            "role":"user",
            "content": user_query
        }]

while True:
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = message_history,
        response_format={"type": "json_object"},
    )
    
    content = response.choices[0].message.content
    objectified_content = json.loads(content)
    
    
    if objectified_content.get("step")=="PLAN":
        print("🤔", objectified_content.get("content"))
        message_history.append({"role":"assistant", "content": content})
        continue
    if objectified_content.get("step")=="OUTPUT":
        print("\n\n\n")
        print("🍾",objectified_content.get("content") )
        break


# few-shot prompting: The model is given question or task after some examples.