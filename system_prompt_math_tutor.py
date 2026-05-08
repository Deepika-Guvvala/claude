from claude_helper import ChatBot

tutor = ChatBot(system_prompt="As if you are a math tutor, give hints to solve the problem")
concise_answer = ChatBot(system_prompt="You are a python engineer that writes very concise code and give only one best method")
i = 0
while i>0:
    # print(f'reply is {tutor.chat("how is 5X+3=2 solved for X?")}')
    print(concise_answer.chat('python code for checking duplicate strings'))
    i=i+1
