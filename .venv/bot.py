import random
import requests
import re

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

class Bot:
    """Класс бота"""
    def __init__(self, token, group_id, file_dir, chance):
        self.bot_token = token
        self.group_id = group_id
        self.chance = chance
        self.dir = file_dir
        self.vk_session = vk_api.VkApi(token = self.bot_token)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id = self.group_id)
        
    def sender(self, id, text):
        """Функция отправки сообщений"""
        self.vk_session.method('messages.send', {
            'chat_id' : id, 
            'message' : text, 
            'random_id' : 0
        })
        
    def change_chance(self, chance):
        """Функция изменения шанса отправки случайных сообщений"""
        self.chance = chance
        return self.chance
    
    def sayRandom(self):
        """Функция выбора случайного сообщения из файла"""
        with open(self.dir, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            return random.choice(lines)

    def isAdmin(self, chat_id, from_id):
        """Функция проверки на статус администратора"""
        members = self.session_api.messages.getConversationMembers(peer_id = 2000000000 + chat_id)["items"]
        is_admin = False
        for user in members:
            if user["member_id"] == from_id and "is_admin" in user and not is_admin:
                is_admin = True
                break

        return is_admin
    
    def check_message(self, received_message, chat_id, from_id):
        """Обработчик сообщений"""
        if re.match("max chance", received_message):
            if self.isAdmin(chat_id, from_id):
                word_list = received_message.split()
                if len(word_list) == 3 and int(word_list[-1]) in range (0, 101):
                    chance = int(word_list[-1])
                    self.sender(
                        chat_id, 
                        f"Установлен шанс ответа {self.change_chance(chance)}"
                    )
                else:
                    self.sender(
                        chat_id, 
                        "Ожидаемый ввод: max chance число_от_0_до_100"
                    )
            else:
              self.sender(
                        chat_id, 
                        "Команда доступна только администраторам"
                    )  
        else:
            random_message = random.randrange(1, 100, 1)
            if random_message in range (1, self.chance + 1):
                self.sender(chat_id, self.sayRandom())
    
    def listen(self):
        """Основная функция"""
        while True:
            try:
                """Отслеживаем каждое событие в беседе."""
                for event in self.longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get("text") != "":                                                        
                        msg = event.message.get("text").lower()
                        chat_id = event.chat_id
                        from_id = event.message.get("from_id")
                        self.check_message(msg, chat_id, from_id)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                print(e)
                    
            


