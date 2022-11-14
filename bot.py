import random
import requests
import re

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from models import User
import utils

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
        
    def messageSender(self, id, text):
        """Функция отправки сообщений"""
        self.vk_session.method('messages.send', {
            'chat_id' : id, 
            'message' : text, 
            'random_id' : 0
        })
        
    def changeChance(self, chance):
        """Функция изменения шанса отправки случайных сообщений"""
        self.chance = chance
        return self.chance
    
    def randomLine(self):
        """Функция выбора случайного сообщения из файла"""
        with open(self.dir, 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            return random.choice(lines)

    def isAdmin(self, chat_id, user_id):
        """Функция проверки на статус администратора"""
        members = self.session_api.messages.getConversationMembers(peer_id = 2000000000 + chat_id)["items"]
        is_admin = False
        for user in members:
            if user["member_id"] == user_id and "is_admin" in user and not is_admin:
                is_admin = True
                break
        return is_admin
    
    def saySomething(self, chat_id):
        """Функция проверки на статус администратора"""
        random_message = random.randrange(1, 100, 1)
        if random_message in range (1, self.chance + 1):
            self.messageSender(chat_id, self.randomLine())
    
    def checkMessage(self, received_message, chat_id, user_id, fwd, msg):
        """Обработчик сообщений"""
        word_list = received_message.split()
        
        if re.match("макс шанс", received_message):
            if self.isAdmin(chat_id, user_id):
                if len(word_list) == 3 and int(word_list[-1]) in range (0, 101):
                    chance = int(word_list[-1])
                    self.messageSender(chat_id, f"Установлен шанс ответа {self.changeChance(chance)}")
                else:
                    self.messageSender(chat_id, "Ожидаемый ввод: макс шанс число_от_0_до_100")
            else:
              self.messageSender(chat_id, "Команда доступна только администраторам")
              
        elif re.match("доброе утро", received_message):  
            self.messageSender(chat_id, "Доброе утро, котенок &#128573;")
            
        elif re.match("спокойной ночи", received_message):  
            self.messageSender(chat_id, "Спокойной ночи, сладкий &#127800;")
         
        elif re.match("макс инфа", received_message):
            if len(word_list) > 2:
                self.messageSender(chat_id, f"Ммм, шанс этого {random.randrange(1, 100, 1)}")
            else:
                self.messageSender(chat_id, "Так что тебя конкретно интересует, сладкий?")
        
        elif fwd:      
            fwd_user = utils.get_user_by_id(fwd['from_id'])  
            user_name = self.vk_session.method('users.get', {'user_id' : fwd_user.vk_id})[0]['first_name']   
            
            if re.match("пред", received_message):  
                fwd_user.warns += 1
                fwd_user.save()

                self.vk_session.method('messages.send', {
                    'chat_id' : msg['peer_id'] - 2000000000,
                    'message' : f'{user_name}, вам выдано предупреждение!\nВсего предупреждений: {fwd_user.warns}/3',
                    'random_id' : 0,
                })
                
                if fwd_user.warns >= 3:
                    self.vk_session.method('messages.removeChatUser', {
                        'user_id' : fwd_user.vk_id,
                        'chat_id' : msg['peer_id'] - 2000000000,
                    })
                    fwd_user.warns = 0
                    fwd_user.save()
                    
            elif re.match("бан", received_message):
                if self.isAdmin(chat_id, user_id):
                    self.vk_session.method('messages.removeChatUser', {
                        'user_id' : fwd['from_id'],
                        'chat_id' : msg['peer_id'] - 2000000000,
                    })
                    
            elif re.match("снять пред", received_message):
                if fwd_user.warns > 0:
                    fwd_user.warns -= 1
                    fwd_user.save()
                    self.vk_session.method('messages.send', {
                        'chat_id' : msg['peer_id'] - 2000000000,
                        'message' : f'С пользователя {user_name} снято 1 предупреждение.',
                        'random_id' : 0,
                    })
                    
                else:
                    self.vk_session.method('messages.send', {
                    'chat_id' : msg['peer_id'] - 2000000000,
                    'message' : f'У пользователя {user_name} нет предупреждений.',
                    'random_id' : 0,
                })
                    
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
                    if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and event.message.get("text") != "":                                                        
                        msg = event.object.message
                        text = msg['text'].lower()
                        user_id = msg['from_id']
                        chat_id = event.chat_id
                        user = utils.get_user_by_id(user_id)
                        fwd = self.vk_session.method('messages.getByConversationMessageId', {
                            'conversation_message_ids' : msg ['conversation_message_id'],
                            'peer_id' : msg['peer_id']
                        })['items'][0]
                        
                        if 'reply_message' in fwd:
                            fwd = fwd['reply_message']
                        else:
                            fwd = None
                        
                        self.checkMessage(text, chat_id, user_id, fwd, msg)

            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                print(e)
                    