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
            'random_id': 0})

    def change_chance(self, chance):
        """Функция изменения шанса отправки случайных сообщений"""
        self.chance = chance
        return self.chance

    def can_convert_to_int(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False

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

    def my_balance(self, chat_id, user):
        """Функция проверки баланса"""
        self.message_sender(chat_id, f"@id{user.vk_id}({user.name}), "
                            f"на вашем счету {user.chips} фишек")

    def say_something(self, chat_id):
        """Функция говорения заготовленных фраз"""
        can_i_speak = random.randrange(1, 100, 1)
        if can_i_speak in range(1, self.chance + 1):
            self.message_sender(chat_id, self.random_line())

    def check_message(self, received_message, chat_id, user_id):
        """Обработчик сообщений"""
        user = utils.get_user_by_id(user_id)
        bjplayer = utils.get_bjplayer_by_id(user_id)
        user.name = self.vk_session.method(
            'users.get', {'user_id': user_id})[0]['first_name']
        user.save()
        word_list = received_message.split()

        if re.match("макс шанс", received_message):
            """Установка шанса ответа"""
            set_chance(self, word_list, chat_id, user_id) # noqa

        elif re.match("макс инфа", received_message):
            """Получение вероятности события"""
            random_chance(self, word_list, chat_id) # noqa

        elif re.match("доброе утро", received_message):
            """Желает доброе утро"""
            self.message_sender(chat_id, "Доброе утро, котенок &#128573;")

        elif re.match("спокойной ночи", received_message):
            """Желает спокойной ночи"""
            self.message_sender(chat_id, "Спокойной ночи, сладкий &#127800;")

        elif re.match("рулетка", received_message):
            """Игра в рулетку"""
            roulette(self, chat_id, word_list, user) # noqa

        elif re.match("мой баланс", received_message):
            """Проверка баланса фишек"""
            self.my_balance(chat_id, user)

        elif re.match("блэкджек", received_message):
            """Игра в блэкджек"""
            if bjplayer.is_playing:
                self.message_sender(chat_id, "Вы уже играете! "
                                    "Напишите 'Стоп игра', "
                                    "если хотите закончить")
            else:
                blackjack(self, chat_id, user, bjplayer, word_list) # noqa

        elif re.match("взять карту", received_message) \
                and bjplayer.is_playing:
            """Взять карту в блэкджеке"""
            take_card(self, chat_id, bjplayer, user) # noqa

        elif re.match("хватит", received_message) \
                and bjplayer.is_playing:
            """Отказаться от карт в блэкджеке"""
            not_take_card(self, chat_id, bjplayer, user) # noqa

        elif re.match("стоп игра", received_message) \
                and bjplayer.is_playing:
            """Остановить игру в блэкджек"""
            clean_player(bjplayer) # noqa
            self.message_sender(chat_id, "Вы завершили игру.")

        else:
            """Начислить пользователю 10 фишек и сказать что-то"""
            user.chips += 10
            user.save()
            self.say_something(chat_id)

    def check_fwd_message(self, received_message, chat_id, user_id, fwd):
        """Обработчик пересланных сообщений"""
        user = utils.get_user_by_id(user_id)
        fwd_user = utils.get_user_by_id(fwd['from_id'])

        if fwd_user.vk_id == -int(MAX_ID): # noqa
            fwd_user.name = "Бот Максим"
        else:
            fwd_user.name = self.vk_session.method(
                'users.get', {'user_id': fwd_user.vk_id})[0]['first_name']

        if re.match("пред", received_message):
            warn(self, chat_id, fwd_user, user) # noqa

        elif re.match("снять пред", received_message):
            unwarn(self, chat_id, fwd_user, user) # noqa

        elif re.match("бан", received_message):
            ban(self, chat_id, fwd_user, fwd, user) # noqa

        else:
            fwd_user.chips += 10
            fwd_user.save()
            self.say_something(chat_id)

    def listen(self):
        """Основная функция"""
        while True:
            try:
                """Отслеживаем каждое событие в беседе"""
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
                                'peer_id': msg['peer_id']})['items'][0]

                        if 'reply_message' in fwd:
                            fwd = fwd['reply_message']
                        else:
                            fwd = None

                        if fwd:
                            self.check_fwd_message(text, chat_id, user_id, fwd)
                        else:
                            self.check_message(text, chat_id, user_id)

            except (requests.exceptions.ReadTimeout,
                    requests.exceptions.ConnectionError) as e:
                print(e)
