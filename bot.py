import random
import requests
import re
from commandhandler import * # noqa
import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
import utils


class Bot:
    """Класс бота"""
    def __init__(self, token, group_id, file_dir, chance):
        self.chance = chance
        self.dir = file_dir
        self.vk_session = vk_api.VkApi(token=token)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id=group_id)

    def message_sender(self, id, text):
        """Функция отправки сообщений"""
        self.vk_session.method('messages.send', {
            'chat_id': id,
            'message': text,
            'random_id': 0
        })

    def change_chance(self, chance):
        """Функция изменения шанса отправки случайных сообщений"""
        self.chance = chance
        return self.chance

    def random_line(self):
        """Функция выбора случайного сообщения из файла"""
        with open(self.dir, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            return random.choice(lines)

    def is_admin(self, chat_id, user_id):
        """Функция проверки на статус администратора"""
        members = self.session_api.messages.getConversationMembers(
            peer_id=2000000000+chat_id)["items"]
        admin = False
        for user in members:
            if user["member_id"] == user_id and \
                    "is_admin" in user and not admin:
                admin = True
                break
        return admin

    def say_something(self, chat_id):
        """Функция говорения заготовленных фраз"""
        can_i_speak = random.randrange(1, 100, 1)
        if can_i_speak in range(1, self.chance + 1):
            self.message_sender(chat_id, self.randomLine())

    def checkMessage(self, received_message, chat_id, user_id):
        """Обработчик сообщений"""
        user = utils.get_user_by_id(user_id)
        user.name = self.vk_session.method(
            'users.get', {'user_id': user_id})[0]['first_name']
        user.save()
        word_list = received_message.split()

        if re.match("макс шанс", received_message):
            set_chance(self, word_list, chat_id, user_id) # noqa
        elif re.match("макс инфа", received_message):
            random_chance(self, word_list, chat_id) # noqa
        elif re.match("доброе утро", received_message):
            self.message_sender(chat_id, "Доброе утро, котенок &#128573;")
        elif re.match("спокойной ночи", received_message):
            self.message_sender(chat_id, "Спокойной ночи, сладкий &#127800;")
        elif re.match("рулетка", received_message):
            roulette(self, chat_id, word_list, user) # noqa
        elif re.match("мой баланс", received_message):
            roulette_balance(self, chat_id, user) # noqa
        else:
            self.saySomething(chat_id)

    def checkFwdMessage(self, received_message, chat_id, user_id, fwd):
        """Обработчик пересланных сообщений"""
        fwd_user = utils.get_user_by_id(fwd['from_id'])
        if fwd_user.vk_id == -int(MAX_ID): # noqa
            fwd_user.name = "Бот Максим"
        else:
            fwd_user.name = self.vk_session.method(
                'users.get', {'user_id': fwd_user.vk_id})[0]['first_name']

        if self.isAdmin(chat_id, user_id):
            if re.match("пред", received_message):
                warn(self, chat_id, fwd_user) # noqa
            elif re.match("снять пред", received_message):
                unwarn(self, chat_id, fwd_user) # noqa
            elif re.match("бан", received_message):
                ban(self, chat_id, fwd_user, fwd) # noqa
            else:
                self.saySomething(chat_id)
        else:
            self.saySomething(chat_id)

    def listen(self):
        """Основная функция"""
        while True:
            try:
                """Отслеживаем каждое событие в беседе."""
                for event in self.longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and \
                            event.from_chat and \
                            event.message.get("text") != "":
                        msg = event.object.message
                        text = msg['text'].lower()
                        user_id = msg['from_id']
                        chat_id = event.chat_id
                        fwd = self.vk_session.method(
                            'messages.getByConversationMessageId',
                            {'conversation_message_ids':
                                msg['conversation_message_id'],
                                'peer_id': msg['peer_id']}
                            )['items'][0]

                        if 'reply_message' in fwd:
                            fwd = fwd['reply_message']
                        else:
                            fwd = None

                        if fwd:
                            self.checkFwdMessage(text, chat_id, user_id, fwd)
                        else:
                            self.checkMessage(text, chat_id, user_id)

            except (requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError
                    ) as e:
                print(e)
