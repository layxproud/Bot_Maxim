def ban(bot, chat_id, fwd_user, fwd):
    if bot.isAdmin(chat_id, fwd_user.vk_id):
        bot.messageSender(chat_id, 'Не получится!')
    else:
        bot.vk_session.method('messages.removeChatUser', {
            'user_id' : fwd['from_id'],
            'chat_id' : chat_id,
        })