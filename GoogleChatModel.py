from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

def format_output(text: str):
    return text.replace('** ','').replace('**','').replace('* ','')

def simple_chat(text: str):
    result = model.invoke(text)
    return format_output(result.content)

def simple_chat_with_messages():
    messages = [
        SystemMessage("you are an expert chef"),
        HumanMessage("give process to make maggie.")
    ]
    result = model.invoke(messages)
    return format_output(result.content)

def simple_chat_with_local_history():
    chat_history = []
    chat_history.append(SystemMessage("You are a helpful school teacher."))
    
    while(True):
        query = input("You: ")
        if(query.lower()=="exit"):
            break
        
        chat_history.append(HumanMessage(query))
        response = model.invoke(chat_history)
        
        chat_history.append(AIMessage(response.content))
        print("AI: ", format_output(response.content))
        

#simple_chat_with_local_history()
# print(simple_chat_with_messages())
# print(simple_chat("what is 10 plus 10?"))