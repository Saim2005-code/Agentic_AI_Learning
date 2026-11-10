import os
import json
from groq import Groq
from dotenv import load_dotenv
from Dummy_VectorDB import vector_db
import systemPrompt

system_prompt = systemPrompt.system_prompt

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


def call_llm(message_history):
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=message_history,
        temperature=0.0
    )

    return response.choices[0].message.content

messages = [{ "role" : "system", "content":system_prompt }]


def run_engine(user_query:str):
    messages.append({"role": "user", "content": user_query})
    max_iteration = 10
    for i in range(0,max_iteration):

        print(f"Iteration {i+1}")
        
        
        response = call_llm(messages)
        print(f"The plan is: {response}")
        messages.append({ "role":"assistant","content":response })

        try:
            actions = json.loads(response)
        except json.JSONDecodeError:
            print("Error: LLM returned invalid format of JSON. Forcing it to correct itself")
            messages.append({"role":"user","content":"Error: Your last output was not valid JSON. Output ONLY JSON."})
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
            elif tool_name == "search_knowledge_base":
                observation = vector_db.search_knowledge_base(tool_input)
            else:
                observation = f"System Error : Tool {tool_name} doesn't exist"


        print(f"Observation: {observation}")
        messages.append({"role":"user","content":f"The Tool result is: {observation}"})
    


if __name__ == "__main__":
    print("Agent Activated. Type exit to quit.")
    while True:
        user_query = input("Enter your query: ")

        if user_query.lower() in ['exit','quit']:
            break

        run_engine(user_query)










