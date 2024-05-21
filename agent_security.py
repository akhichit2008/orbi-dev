import subprocess
import json

def scan_project(dir_path:str):
    result = subprocess.run(['snyk','test',dir_path,'--json'],capture_output=True,text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        print("Error in performing security scan of the code")
        raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)

"""
Sample usage:-
from agent_security import scan_project
import json

"""

dir_path="/Backend/"

result = scan_project(dir_path)

print(json.dumps(result,indent=2))
