import ast

from claude_helper import ChatBot
import json
import re
from statistics import mean

def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete. Add the task format for each JSON object.

Example output:
```json
[
    {
        "task": "Description of python task",
        "format": "Python"
    },
    ...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    chat_bot = ChatBot(stop_sequences=['```'])
    text = chat_bot.chat(prompt, prefill='```json')

    with open('prompt_eval.json', 'w') as f:
        json.dump(json.loads(text), f, indent=2)

def run_prompt(test):
    prompt = f'''please answer the task: {test}'''
    chat_bot = ChatBot()
    return chat_bot.chat(prompt)

def grade_by_model(task, output):
    eval_prompt = f"""
    You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

    Original Task:
    <task>
    {task}
    </task>

    Solution to Evaluate:
    <solution>
    {output}
    </solution>

    Output Format
    Provide your evaluation as a structured JSON object with the following fields, in this specific order:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement
    - "reasoning": A concise explanation of your overall assessment
    - "score": A number between 1-10

    Respond with JSON. Keep your response concise and direct.
    Example response shape:
    {{
        "strengths": string[],
        "weaknesses": string[],
        "reasoning": string,
        "score": number
    }}
        """
    chat_bot = ChatBot(stop_sequences=['```'])
    text = chat_bot.chat(eval_prompt, prefill='```json')
    text = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)
    return json.loads(text)


def grade_python(python_code):
    try:
        ast.parse(python_code)
        return 10
    except SyntaxError:
        return 0

def grade_test_case(test_case):
    output = run_prompt(test_case['task'])
    model_evaluation = grade_by_model(test_case['task'], output)
    # TODO change for json or regex
    syntax_score = grade_python(output.strip())
    return {"output": output,
            "score": (model_evaluation['score'] + syntax_score)/2,
            "reasoning": model_evaluation['reasoning'],
            "test_case": test_case['task']}


# generate_dataset()
results = []
with open('prompt_eval.json', 'r') as f:
    test_cases = json.load(f)
    for test_case in test_cases:
        response = grade_test_case(test_case)
        results.append(response)

    average_score = mean([results['score'] for results in results])
    print(f'avg score is :{average_score}')



