import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("groq_api_key"))

def get_weather(city:str) -> str:
    if "kolkata" in city.lower():
        return "The temperature in Kolkata is 32C"
    return "Weather is unknown for this city"

def calculate_math(expression:str) -> str:
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Math Error {e}"

system_prompt = """
You are a reasoning agent. You have access to the following tools:
1. get_weather(city: str) - Returns the current weather for a city.
2. calculate_math(expression: str) - Evaluates a mathematical expression.

If you need to use a tool, you must output strictly a JSON object like this:
    {
        "thought":"I need to get the weather first, then multiply that number by 14.5.",
        "tool": "get_weather", 
        "input": "Kolkata"
    }

I will then provide you with the tool's result.

Once you have all the information you need to answer the user's original request, output strictly a JSON object like this:
{"final_answer": "your complete final answer here"}

Do not output any markdown formatting, code blocks, or conversational text. Output ONLY the raw JSON object.
"""

def call_llm(message_history):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=message_history,
        temperature=0.0
    )

    return response.choices[0].message.content

message = [{ "role" : "system", "content":system_prompt }]


def run_engine(user_query:str):
    message.append({"role": "user", "content": user_query})
    max_iteration = 10
    for i in range(0,max_iteration):

        print(f"Iteration {i+1}")
        response = call_llm(message)
        print(f"The plan is: {response}")
        message.append({ "role":"assistant","content":response })

        try:
            actions = json.loads(response)
        except json.JSONDecodeError:
            print("Error: LLM returned invalid format of JSON. Forcing it to correct itself")
            message.append({"role":"user","content":"Error: Your last output was not valid JSON. Output ONLY JSON."})
            continue

        if "final_answer" in actions:
            print("Mission Accomplished")
            print(actions["final_answer"])
            break

        observation = ""
        if "tool" in actions:
            tool_name = actions["tool"]
            tool_input = actions["input"]

            if tool_name == "get_weather":
                observation = get_weather(tool_input)
            elif tool_name == "calculate_math":
                observation = calculate_math(tool_input)
            else:
                observation = f"System Error : Tool {tool_name} doesn't exist"


        print(f"Observation: {observation}")
        message.append({"role":"user","content":f"The Tool result is: {observation}"})
    


if __name__ == "__main__":
    print("Agent Activated. Type exit to quit.")
    while True:
        user_query = input("Enter your query: ")

        if user_query.lower() in ['exit','quit']:
            break

        run_engine(user_query)










