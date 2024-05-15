from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

llm = ChatGoogleGenerativeAI(model="gemini-pro")
code_prompt_template = PromptTemplate(
    input_variables=["language","problem"],
    template="Write the code in {language} required to solve {problem}"
)

testing_prompt_template = PromptTemplate(
    input_variables=["language","problem","generated_code"],
    template="Write a test in {language} on {problem} with respect to {generated_code}"
)
code_chain = LLMChain(llm=llm,prompt=code_prompt_template,output_key="code")
test_chain = LLMChain(llm=llm,prompt=testing_prompt_template,output_key="test")
response = code_chain.run({"language":"python","problem":"Write a function to solve fibbonachi sequence"})
print(response)