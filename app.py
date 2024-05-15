from dotenv import load_dotenv
import os
from shell_tool import command_pool
from code_gen import llm

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
#response = chain.run(input=prompt)
#print(response)
command_pool.run("Get ipconfiguration of this system")