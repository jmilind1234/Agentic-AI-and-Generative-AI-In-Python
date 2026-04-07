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

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "developer",
            "content": DEVELOPER_PROMPT
        },
        {
            "role": "user",
            "content":"solve the equation a plus b the whole cube."
        },
        # Manually keep adding messages to History
        {
            "role":"assistant",
            "content": json.dumps({"step":"START", "content":"solve the equation a plus b the whole cube."})
        },
        {
            "role":"assistant",
            "content":json.dumps({"step":"PLAN", "content": "User is asking to solve the equation (a + b)^3."})
        },
        {
            "role":"assistant",
            "content": json.dumps({"step": "PLAN", "content": "To solve (a + b)^3, we can use the binomial theorem."})
        },
        {
             "role":"assistant",
            "content": json.dumps({"step": "PLAN", "content": "The binomial theorem states that (x + y)^n = sum(k=0 to n, C(n, k) * x^(n-k) * y^k) where C(n, k) is the binomial coefficient."})
        },
        {
             "role":"assistant",
            "content": json.dumps({"step": "PLAN", "content": "In our case, n=3, x=a, and y=b. Therefore, we will expand (a + b)^3 using this formula."})
        },
        {
             "role":"assistant",
            "content": json.dumps({"step": "PLAN", "content": "Calculating the expansion: (a + b)^3 = C(3,0)*a^3*b^0 + C(3,1)*a^2*b^1 + C(3,2)*a^1*b^2 + C(3,3)*a^0*b^3."})
        },
        {
            "role":"assistant",
            "content":json.dumps({"step": "PLAN", "content": "Calculating the binomial coefficients: C(3,0)=1, C(3,1)=3, C(3,2)=3, C(3,3)=1."})
        },
        {
            "role":"assistant",
            "content":json.dumps({"step": "PLAN", "content": "Substituting the coefficients into the expression gives: a^3 + 3a^2b + 3ab^2 + b^3."})
        },
        {
            "role":"assistant",
            "content": json.dumps({"step": "PLAN", "content": "So, the final expanded form of (a + b)^3 is a^3 + 3a^2b + 3ab^2 + b^3."})
        }
    ],
    response_format={"type": "json_object"},
)

print(response.choices[0].message.content)

# few-shot prompting: The model is given question or task after some examples.