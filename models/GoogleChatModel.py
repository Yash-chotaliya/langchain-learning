from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
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
        
def prompt_template_chat(animal: str, bird: str):
    
    template = "{animal} and {bird} has how many legs in total?"
    
    prompt = ChatPromptTemplate.from_template(template).format(animal=animal, bird=bird)
    
    result = model.invoke(prompt)
    return format_output(result.content)

def prompt_template_chat_with_messages():
    messages = [
        ('system',"you are a {professtion}"),
        ('human',"i have {experience} experience. what is my expected salary in india?")
    ]
    
    prompt = ChatPromptTemplate.from_messages(messages).format(professtion="android developer", experience="5 years")

    result = model.invoke(prompt)
    return format_output(result.content)

def chain_chat():
    messages = [
        ('system',"you are a {professtion}"),
        ('human',"i have {experience} experience. what is my expected salary in india?")
    ]
    
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | model | StrOutputParser()

    result = chain.invoke({"professtion":"android developer", "experience":"5 years"})
    return format_output(result)

#print(chain_chat())
#print(prompt_template_chat_with_messages())
#simple_chat_with_local_history()
# print(simple_chat_with_messages())
# print(simple_chat("what is 10 plus 10?"))