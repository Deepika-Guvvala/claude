from claude_helper import ChatBot
import json

def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
    {
        "task": "Description of task",
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

def grade_test_case(test_case):
    output = run_prompt(test_case)
    score = 10

    return {"output": output, "score": score, "test_case": test_case}

results = []
with open('prompt_eval.json', 'r') as f:
    test_cases = json.load(f)
    for test_case in test_cases:
        response = grade_test_case(test_case['task'])
        results.append(response)

    print(json.dumps(results, indent=2))



