from langchain_community.tools import ShellTool
from langchain.agents import initialize_agent, AgentType
from config import llm
import warnings
from langchain_core.globals import set_verbose, set_debug

set_verbose(False)
set_debug(False)


warnings.filterwarnings("ignore",category=DeprecationWarning)

shell_tool = ShellTool()


shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")

command_pool = initialize_agent([shell_tool],llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,verbose=True)


