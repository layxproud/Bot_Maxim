import random
import requests
import re

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

class Bot:
    def __init__(self, token, group_id, file_dir, chance):
        self.bot_token = token
        self.group_id = group_id
        self.chance = chance
        self.dir = file_dir
        self.vk_session = vk_api.VkApi(token = self.bot_token)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id = self.group_id)
        
    def sender(self, id, text):
        self.vk_session.method('messages.send', {
            'chat_id' : id, 
            'message' : text, 
            'random_id' : 0
        })
        
    def change_chance(self, chance):
        self.chance = chance
        return self.chance
    
    def sayRandom(self):
        with open(self.dir, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            return random.choice(lines)

    def check_message(self, received_message, chat_id):
        if re.match("max chance", received_message):
            word_list = received_message.split()
            if len(word_list) == 3 and int(word_list[-1]) in range (0,101):
                chance = int(word_list[-1])
                self.sender(
                    chat_id, 
                    f"Установлен шанс ответа {self.change_chance(chance)}"
                )
            else:
                self.sender(
                    chat_id, 
                    "Неправильная команда"
                )
        else:
            random_message = random.randrange(1, 100, 1)
            if random_message in range (1, self.chance + 1):
                self.sender(chat_id, self.sayRandom())
    
    def listen(self):
        while True:
            try:
                """Отслеживаем каждое событие в беседе."""
                for event in self.longpoll.listen():
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get("text") != "":                                                        
                        msg = event.message.get("text").lower()
                        chat_id = event.chat_id
                        self.from_id = event.message.get("from_id")
                        self.check_message(msg, chat_id)
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                print(e)
                    
            


