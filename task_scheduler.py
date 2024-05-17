from langchain_core.tools import tool
from typing import Callable
import os
import _io
from operator import itemgetter
from typing import Dict,List,Union
from langchain_core.messages import AIMessage,HumanMessage
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnableSequence,
    RunnableMap,
    RunnablePassthrough
)
from config import llm, LLMOutputCode
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.tools import ShellTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from parsers import ActionPlanParser


@tool
def shell_tool(command:str)->str:
    '''A Bash Shell Tool for the agent to use to install dependecies and execute code'''
    shell = ShellTool()
    result = shell.run(command)
    return result

@tool
def add_code(file_name:str,code:str,path:str="/std/code") -> _io.TextIOWrapper:
    """Creates a file and adds contents to it"""
    with open(file_name,"w") as file_handle:
        file_handle.write(code)
    return file_handle

@tool
def append_code(file_name:str,code:str,path:str="/std/code") -> _io.TextIOWrapper:
    """Appends code to an existing code file"""
    with open(file_name,"a") as file_handle:
        file_handle.write(code)
    return file_handle

@tool
def extract_web_docs(urls:str) -> str:
    '''Extracts code documentation from a source and formats it'''
    loader = AsyncHtmlLoader(urls)
    docs = loader.load()
    html2text_transformer = Html2TextTransformer()
    docs_text = html2text_transformer.transform_documents(docs)
    print(docs_text)
    return docs_text[0].page_content[0:1000]


@tool
def add_documentation_as_md(documentation:str) -> _io.TextIOWrapper:
    '''Adds Generated documentation for a piece of code to a file'''
    with open("documentation.md","a") as file_handle:
        file_handle.write(documentation)
    return file_handle

tools = [add_code,append_code,extract_web_docs,add_documentation_as_md,shell_tool]
llm = llm.bind_tools(tools)
tool_map = {tool.name: tool for tool in tools}



def invoke_tools(message: AIMessage) -> Runnable:
    tool_map = {tool.name: tool for tool in tools}
    tool_calls = message.tool_calls.copy()
    for call in tool_calls:
        call['output'] = tool_map[call['name']].invoke(call['args'])
    return tool_calls


main_llm_chain = llm | invoke_tools


topic = input("Enter the topic of software: ")
action_plan_prompt = PromptTemplate(
    input_variables=["topic"],
    template="You are a programmer. Given a app idea {topic}, provide an action plan (at coding level) on how to approach the problem and divide it into smaller tasks"
)
action_llm = LLMChain(llm=llm,prompt=action_plan_prompt,output_key="action_plan")
action_plan = action_llm.run({"topic":topic})
print(action_plan)
action_plan_parser = ActionPlanParser(action_plan)

def parser_job(routine:Callable):
    '''A decorator to pass in any routine to be executed as a job in each task entry from a LLM'''
    def wrapper():
        for task, steps in action_plan_parser.tasks.items():
            routine(task,steps)

    return wrapper

@parser_job
def execute_task_llm(task:str,steps:str) -> LLMOutputCode:
    main_llm_chain.invoke("""Do the required Setup and Code (if required) for all the steps mentioned in the provided task.
    Use the shell tool provided to you in case you want to install any dependencies using commands through the
    command line. Also provide explanation of what you are doing in a concise manner
    """)
    code : LLMOutputCode = 1
    return code

execute_task_llm()
