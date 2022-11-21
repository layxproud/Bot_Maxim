def set_chance(bot, word_list, chat_id, user_id):
    """Устанавливает шанс ответа"""
    if bot.is_admin(chat_id, user_id):

        if len(word_list) == 3 and int(word_list[-1]) in range(0, 101):
            chance = int(word_list[-1])
            bot.message_sender(chat_id, f"Установлен шанс ответа "
                               f"{bot.change_chance(chance)}")

        else:
            bot.message_sender(chat_id, "Ожидаемый ввод: макс шанс "
                               "число_от_0_до_100")

    else:
        bot.message_sender(chat_id, "Команда доступна только администраторам")
