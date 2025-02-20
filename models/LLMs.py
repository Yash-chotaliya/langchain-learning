from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = OpenAI(model="gpt-3.5-turbo-instruct", api_key=os.getenv("OPENAI_API_KEY"))

result = llm.invoke("What is the capital of India?")

print(result)
