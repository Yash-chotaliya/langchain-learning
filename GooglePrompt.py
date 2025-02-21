from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

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


#print(prompt_template_chat_with_messages())