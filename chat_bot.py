from claude_helper import ChatBot

bot = ChatBot()
i=0
while i==0:
    user_input = input("> ")
    print(bot.chat(user_input))
    i=i+1
