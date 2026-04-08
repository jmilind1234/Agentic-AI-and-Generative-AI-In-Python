# chain of thought prompting
from openai import OpenAI
from dotenv import load_dotenv
import requests
import json

load_dotenv()
client = OpenAI()


def get_weather(city: str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}"
    return "Something went wrong"


available_tools = {"get_weather": get_weather}

DEVELOPER_PROMPT = """
You're an expert AI Assistant in resolving user queries using chain of thought.
You work on START, PLAN and OUTPUT steps.
You need to first PLAN what needs to be done. The PLAN can be multiple steps.
Once you think enough PLAN has been done, finally you can give an output.
You can also call a tool if required from the list of available tools.
for every tool call wait for the observe step which is the output from the called tool.

Rules:
- Strictly follow the given JSON output format.
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (that can be multiple times) and finally OUTPUT (which is going to be displayed to the user).

Output JSON Format:

{"step":"START" | "PLAN" | "OUTPUT" | "TOOL" | "OBSERVE", "content" : "string", "tool": "string", "input" : "string"}

Available tools:
- get_weather(city: str) :Takes city name as an input and returns the weather info about the city.

Example1: 
START: Hey, Can you solve 2 + 3 * 5 / 10
PLAN : {"step":"PLAN", "content": "seems like useris interested in mathematics problem"}
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

Example2: 
START: What is weather of Delhi?
PLAN : {"step":"PLAN", "content": "seems like user is interested in getting weather of Delhi in India"}
PLAN : {"step":"PLAN", "content": "Lets see if we have any available tool in the list of available tools"}
PLAN : {"step":"PLAN", "content": "We have one tool for getting weather and that is get_weather"}
PLAN : {"step":"PLAN", "content": "I need to call get_weather tool with Delhi as input to it"}
PLAN : {"step":"TOOL", "input": "Delhi", "tool": "get_weather"}
PLAN : {"step":"OBSERVE","tool": "get_weather", "output": "The temp of delhi is cloudy with 35 C"}
PLAN : {"step":"PLAN", "content": "Great, I got the weather info about Delhi"}
OUTPUT: {"step":"OUTPUT", "content": "The current weather of Delhi is 20 C with some cloudy sky."}

"""

print("\n\n\n")

user_query = input("👉")


message_history = [
    {"role": "developer", "content": DEVELOPER_PROMPT},
    {"role": "user", "content": user_query},
]

while True:

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_history,
        response_format={"type": "json_object"},
    )
    
    content = response.choices[0].message.content
    objectified_content = json.loads(content)

    if objectified_content.get("step") == "PLAN":
        print("🤔", objectified_content.get("content"))
        message_history.append({"role": "assistant", "content": content})
        continue

    if objectified_content.get("step") == "TOOL":
        tool = objectified_content.get("tool")
        input = objectified_content.get("input")
        tool_response = available_tools[tool](input)
        print("⛏️", tool, "(", input, ")", " = ", tool_response)
        message_history.append(
            {
                "role": "developer",
                "content": json.dumps(
                    {"step": "OBSERVE", "tool": tool, "output": tool_response}
                ),
            }
        )
        continue

    if objectified_content.get("step") == "OUTPUT":
        print("\n\n\n")
        print("🍾", objectified_content.get("content"))
        break


# few-shot prompting: The model is given question or task after some examples.
