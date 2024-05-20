from langchain_core.tools import tool
from typing import Callable
import shutil
import os
import _io
from operator import itemgetter
from typing import Dict,List,Union
from langchain_core.messages import AIMessage,HumanMessage
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langchain.agents import initialize_agent, AgentExecutor, create_openai_functions_agent
from langchain_core.runnables import (
    Runnable,
    RunnableLambda,
    RunnableSequence,
    RunnableMap,
    RunnablePassthrough
)
from config import llm,prompt
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.tools import ShellTool
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from parsers import ActionPlanParser, CodeParser, format_code



@tool
def shell_tool(command:str)->str:
    '''A Bash Shell Tool for the agent to use to install dependecies and execute code'''
    shell = ShellTool()
    result = shell.run(command)
    print(result)
    return result

@tool
def create_project_dir(dir_name:str,dir_path:str=""):
    """A Simple tool that can be used to create a new project directory. It can also be used to create a subdirectory inside of a project (in case needed)"""
    if not os.path.exists(os.path.join(dir_path,dir_name)):
        os.makedirs(os.path.join(dir_path,dir_name))

@tool
def copy_file(file_name:str,copy_to_path:str):
    """A simple tool to help move around code files from current directory to the required project directory"""
    shutil.copy(file_name,copy_to_path)

@tool
def add_code(file_name:str,code:str,path:str=os.path.join(os.path.expanduser("~"),"/orbidev/")) -> _io.TextIOWrapper:
    """Creates a file and adds contents to it"""
    #code_parser = CodeParser(code)
    #code = code_parser.format()
    code = format_code(code)
    with open(file_name,"w") as file_handle:
        file_handle.write(code)
    return file_handle

@tool
def append_code(file_name:str,code:str,path:str=os.path.join(os.path.expanduser("~"),"/orbidev/")) -> _io.TextIOWrapper:
    """Appends code to an existing code file"""
    #code_parser = CodeParser(code)
    #code = code_parser.format()
    code = format_code(code)
    with open(file_name,"a") as file_handle:
        file_handle.write(code)
    return file_handle

tools = [create_project_dir,add_code,append_code,shell_tool,copy_file]
#main_agent = initialize_agent(tools,llm,agent="structured-chat-zero-shot-react-description",verbose=True)
#llm = llm.bind_tools(tools)
main_agent = create_openai_functions_agent(llm, tools, prompt)
tool_map = {tool.name: tool for tool in tools}

#print(main_agent.agent.llm_chain.prompt.template)



def invoke_tools(message: AIMessage) -> Runnable:
    tool_map = {tool.name: tool for tool in tools}
    tool_calls = message.tool_calls.copy()
    for idx, call in enumerate(tool_calls):
        print(f"Processing tool call {idx}: {call}")
        if call['name'] in tool_map:
            try:
                call['output'] = tool_map[call['name']].invoke(call['args'])
            except Exception as e:
                print(f"Error invoking tool {call['name']} with args {call['args']}: {e}")
        else:
            print(f"Tool {call['name']} not found in tool_map.")
    return tool_calls


#main_llm_chain = main_agent 
main_llm_chain = AgentExecutor(agent=main_agent,tools=tools,verbose=True)


def parser_job(routine:Callable):
    '''A decorator to pass in any routine to be executed as a job in each task entry from a LLM'''
    def wrapper():
        for task, steps in action_plan_parser.tasks.items():
            routine(task,steps)

    return wrapper

@parser_job
def execute_task_llm(task:str,steps:str):
    print("Doing Job")
    main_llm_chain.invoke("Do the required Setup and Code (if required) for all the steps mentioned in the provided task. Use the shell tool provided to you in case you want to install any dependencies using commands through the command line")