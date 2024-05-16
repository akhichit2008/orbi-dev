from langchain_core.tools import tool
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
from config import llm
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer

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

tools = [add_code,append_code,extract_web_docs,add_documentation_as_md]
llm = llm.bind_tools(tools)
tool_map = {tool.name: tool for tool in tools}



def invoke_tools(message: AIMessage) -> Runnable:
    tool_map = {tool.name: tool for tool in tools}
    tool_calls = message.tool_calls.copy()
    for call in tool_calls:
        call['output'] = tool_map[call['name']].invoke(call['args'])
    return tool_calls


chain = llm | invoke_tools