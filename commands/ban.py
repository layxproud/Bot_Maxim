def ban(bot, chat_id, fwd_user, fwd, user):
    """Функция блокировки пользователя"""
    if bot.is_admin(chat_id, fwd_user.vk_id):
        """Заблокировать админа не получится"""
        bot.message_sender(chat_id, 'Не получится!')

    elif not bot.is_admin(chat_id, user.vk_id):
        """Не админ не может банить"""
        bot.message_sender(chat_id, "Команда доступна только администраторам!")

    else:
        bot.vk_session.method('messages.removeChatUser', {
            'user_id': fwd['from_id'],
            'chat_id': chat_id})
