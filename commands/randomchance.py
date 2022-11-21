import random


def random_chance(bot, word_list, chat_id):
    if len(word_list) > 2:
        bot.message_sender(chat_id, f"Ммм, шанс этого "
                           f"{random.randrange(1, 100, 1)}")
    else:
        bot.message_sender(chat_id, "Так что тебя конкретно "
                           "интересует, сладкий?")
