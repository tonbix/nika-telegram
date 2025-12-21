import asyncio
import requests
import json
from dotenv import load_dotenv
from os import getenv
from configparser import ConfigParser


# loading configs
load_dotenv()
AI_TOKEN=getenv("AI_TOKEN")

config = ConfigParser()
config.read("config.ini")
selectedModel = config.get("AI", "Model")


async def request_ai(history: dict):
    maxAttempts = 10

    for i in range(maxAttempts):
        # send request to open router
        response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {AI_TOKEN}",
                },
                data=json.dumps(
                    {
                        "model": selectedModel,
                        "messages": history,
                        "top_p": 1,
                        "temperature": 1,
                        "frequency_penalty": 0,
                        "presence_penalty": 0,
                        "repetition_penalty": 1,
                        "top_k": 0,
                    }
                )
            )
            
        if "error" in json.loads(response.text):
            print(f"attempt {i} failed. Retrying...")
        else:
            print(f"succeded on {i} attempt!")

            return json.loads(response.text)["choices"][0]["message"]

        await asyncio.sleep(1)

