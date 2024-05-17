''' Custom output parsers to extract specific pieces of information from LLM outputs'''
class ActionPlanParser:
    '''An Output Parser to parse the action plan provided by LLM in a specific format'''
    def __init__(self,text:str) -> dict:
        self.text = text
        self.tasks = {}
        current_task = None
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("Task "):
                current_task = line
                self.tasks[current_task] = []
            elif current_task and line:
                self.tasks[current_task].append(line)

    def format_parsed_output(self) -> str:
        formatted_output = []
        for task, steps in self.tasks.items():
            formatted_output.append(f"{task}:")
            for step in steps:
                formatted_output.append(f"  {step}")
        return "\n".join(formatted_output)


'''
action_plan = """
Task 1: Create Dev Environment
- Set up virtual environment
- Install necessary packages
- Configure IDE

Task 2: Design Database Schema
- Define tables and relationships
- Create ER diagrams
- Review schema with team

Task 3: Implement Authentication
- Set up user model
- Integrate with OAuth
- Create login and registration endpoints
"""
action_plan_parser = ActionPlanParser(action_plan)


Sample code on how to use the action plan output parser
@parser_job
def test_job(task,steps):
    print("Task : {}".format(task))
    print("Steps: {}".format(steps))
test_job()
'''
