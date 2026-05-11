from claude_helper import ChatBot

bot = ChatBot(temperature=0.0)
i=0
while i==0:
    print(bot.chat('Generate a one line movie idea'))
    i=i+1