from config import llm
#from code_gen import *
#from shell_tool import command_pool
from parsers import ActionPlanParser
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

topic = input("Enter the topic of software: ")
action_plan_prompt = PromptTemplate(
    input_variables=["topic"],
    template="You are a programmer. Given a app idea {topic}, provide an action plan (at coding level) on how to approach the problem and divide it into smaller tasks"
)
action_llm = LLMChain(llm=llm,prompt=action_plan_prompt,output_key="action_plan")
action_plan = action_llm.run({"topic":topic})