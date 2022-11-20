import random

def randomchance(bot, word_list, chat_id):
    if len(word_list) > 2:
        bot.messageSender(chat_id, f"Ммм, шанс этого {random.randrange(1, 100, 1)}")
    else:
        bot.messageSender(chat_id, "Так что тебя конкретно интересует, сладкий?")