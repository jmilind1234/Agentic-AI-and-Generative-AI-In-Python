from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input=[
        {
            "role": "developer",
            "content": "Yo are an expert in the mathematics and only answer mathematics questions. If asked question that is not relaated to mathematics just say sorry."
        },
        {
            "role": "user",
            "content":"Hey There, write a code in c++to add any number of numbers."
        }
    ]
)

print(response.output_text)