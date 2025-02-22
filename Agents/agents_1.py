from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor, tool
import datetime
from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

@tool
def get_current_date_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ returns the current date and time in specified format """
    current_time = datetime.datetime.now().strftime(format = format)
    return current_time

def current_time_without_agent():
    query = "what is current date and time"
    prompt = ChatPromptTemplate.from_template("what is the current time in {query}?")
    chain = prompt | model | StrOutputParser()
    result = chain.invoke({"query": query})
    print(result)
    
def current_time_with_agent():
    prompt = hub.pull("hwchase17/react")
    tools = [get_current_date_time]
    agent = create_react_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = agent_executor.invoke({"input": "what is the current date and time. just show the current time"})
    
current_time_with_agent()