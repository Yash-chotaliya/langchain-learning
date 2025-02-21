from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnableBranch
from dotenv import load_dotenv
import os
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

def format_output(text: str):
    return text.replace('** ','').replace('**','').replace('* ','')

def chain_chat():
    messages = [
        ('system',"you are a {professtion}. answer my doubt in 4 words."),
        ('human',"i have {experience} experience. what is my expected salary in india?")
    ]
    
    prompt = ChatPromptTemplate.from_messages(messages)

    chain = prompt | model | StrOutputParser()

    result = chain.invoke({"professtion":"android developer", "experience":"5 years"})
    return format_output(result)

def sequencial_chain():
    
    messages = [
        ('system',"you are a professional {professtion}. answer my doubt in 4 words."),
        ('human',"i have {experience} experience. what is my expected salary in india?")
    ]
    
    prompt = ChatPromptTemplate.from_messages(messages)
    
    prepare_for_translation = RunnableLambda(lambda output : {
        'language': "gujarati",
        'text': output
    })
    
    translation_prompt = ChatPromptTemplate.from_messages([
        ('system', 'you are a translator that converts input into {language}'),
        ('human', 'translate this sentence: {text}')
    ])
    
    chain = prompt | model | StrOutputParser() | prepare_for_translation | translation_prompt | model | StrOutputParser()
    
    result = chain.invoke({"professtion":"android developer", "experience":"5 years"})
    
    return format_output(result)
    
def parallel_chain():
    
    ingredient_prompt = ChatPromptTemplate.from_messages([
        ('system', 'you are a great chef'),
        ('human', 'give ingredients for {recipe}')
    ])
    
    steps_prompt = ChatPromptTemplate.from_messages([
        ('system', 'you are a great chef'),
        ('human', 'give steps to make {recipe}')
    ])
    
    find_ingredients = ingredient_prompt | model | StrOutputParser()
    find_steps = steps_prompt | model | StrOutputParser()
    
    generate_output = RunnableLambda(lambda x : "ingredients:\n\n\n"+x['ingredients']+"\n\n\nsteps: \n\n\n"+x['steps'])
    
    chain = (
        RunnableParallel(ingredients = find_ingredients, steps = find_steps)
        | generate_output
    )
    
    result = chain.invoke({"recipe": "maggie"})
    
    return format_output(result)

def conditional_chain():
    positive_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human","Generate a thank you note for this positive feedback: {feedback}.")
        ]
    )

    negative_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human","Generate a response addressing this negative feedback: {feedback}.")
        ]
    )

    neutral_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human","Generate a request for more details for this neutral feedback: {feedback}.",)
        ]
    )

    escalate_feedback_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human","Generate a message to escalate this feedback to a human agent: {feedback}.")
        ]
    )

    classification_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant."),
            ("human",
            "Classify the sentiment of this feedback as positive, negative, neutral, or escalate: {feedback}."),
        ]
    )

    branches = RunnableBranch(
        (
            lambda x: "positive" in x.lower(),
            positive_feedback_template | model | StrOutputParser()  # Positive feedback chain
        ),
        (
            lambda x: "negative" in x.lower(),
            negative_feedback_template | model | StrOutputParser()  # Negative feedback chain
        ),
        (
            lambda x: "neutral" in x.lower(),
            neutral_feedback_template | model | StrOutputParser()  # Neutral feedback chain
        ),
        escalate_feedback_template | model | StrOutputParser()
    )

    # Create the classification chain
    classification_chain = classification_template | model | StrOutputParser()
    
    chain = classification_chain | branches

    result = chain.invoke({"feedback": "The product is terrible. It broke after just one use and the quality is very poor."})

    print(result)

conditional_chain()