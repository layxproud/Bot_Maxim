def setChance(bot, word_list, chat_id, user_id):
    if bot.isAdmin(chat_id, user_id):
        if len(word_list) == 3 and int(word_list[-1]) in range (0, 101):
            chance = int(word_list[-1])
            bot.messageSender(chat_id, f"Установлен шанс ответа {bot.changeChance(chance)}")
        else:
            bot.messageSender(chat_id, "Ожидаемый ввод: макс шанс число_от_0_до_100")
    else:
        bot.messageSender(chat_id, "Команда доступна только администраторам")
