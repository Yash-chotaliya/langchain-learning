from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

chatModel = ChatOpenAI(model="gpt-3.5-turbo-instruct", api_key=os.getenv("OPENAI_API_KEY"))

result = chatModel.invoke("What is the capital of India?")

print(result)