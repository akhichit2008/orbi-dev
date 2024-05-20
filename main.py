from config import llm
#from code_gen import *
#from shell_tool import command_pool
from parsers import ActionPlanParser
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from task_scheduler import main_llm_chain

topic = input("Enter the topic of software: ")
'''
Example Prompt : rite a flask app to display hello world at the index endpoint. write the code in a file named program.py

action_plan_prompt = PromptTemplate(
    input_variables=["topic"],
    template="You are a programmer. Given an app idea {topic}, provide an action plan (at coding level) on how to approach the problem and divide it into smaller tasks"
)
action_llm = LLMChain(llm=llm,prompt=action_plan_prompt,output_key="action_plan")
action_plan = action_llm.run({"topic":topic})
main_llm_chain.invoke(f"follow these instructions and do the needfull :- {action_plan}")

'''


main_llm_chain.invoke({"input":f"You are a software engineer. Using the tools provided to you install all the required dependencies and write the code for the given problem :- {topic}"})
