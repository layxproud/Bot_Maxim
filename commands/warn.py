def warn(bot, chat_id, fwd_user, user):
    """Выдает пользователю предупреждение"""
    if bot.is_admin(chat_id, fwd_user.vk_id):
        bot.message_sender(chat_id, "Не получится!")

    elif not bot.is_admin(chat_id, user.vk_id):
        bot.message_sender(chat_id, "Команда доступна только администраторам!")

    else:
        fwd_user.warns += 1
        fwd_user.save()
        bot.message_sender(chat_id, f"@id{fwd_user.vk_id}({fwd_user.name}), "
                           "вам выдано предупреждение!\n"
                           f"Всего предупреждений: {fwd_user.warns}/3")

        if fwd_user.warns >= 3:
            bot.vk_session.method('messages.removeChatUser', {
                'user_id': fwd_user.vk_id,
                'chat_id': chat_id})
            fwd_user.warns = 0
            fwd_user.save()


def unwarn(bot, chat_id, fwd_user, user):
    """Снимает с пользователя предупреждение"""
    if not bot.is_admin(chat_id, user.vk_id):
        bot.message_sender(chat_id, "Команда доступна только администраторам!")

    elif fwd_user.warns > 0:
        fwd_user.warns -= 1
        fwd_user.save()
        bot.message_sender(chat_id, f"С пользователя @id{fwd_user.vk_id}"
                           f"({fwd_user.name}) снято 1 предупреждение.")

    else:
        bot.message_sender(chat_id, f"У пользователя @id{fwd_user.vk_id}"
                           f"({fwd_user.name}) нет предупреждений.")
