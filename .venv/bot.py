import random

import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

class Bot:
    def __init__(self, token, group_id):
        self.bot_token = token
        self.group_id = group_id
        self.chance = 100
        self.vk_session = vk_api.VkApi(token = self.bot_token)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, group_id = 217147732)
        
    def sender(self, id, text):
        self.vk_session.method('messages.send', {
            'chat_id' : id, 
            'message' : text, 
            'random_id' : 0
        })
        
    def change_chance(self, chance):
        self.chance = chance
        return self.chance

    def listen(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                
                msg = event.object.message['text'].lower()
                words = msg.split()
                
                if event.from_chat:
                    id = event.chat_id 
                    
                    if words[0] == "max":
                        try:
                            if words[1] == "chance":
                                try:
                                    if int(words[2]) in range (0, 101):
                                        # chance = int(words[2])
                                        self.sender(id, f"Установлен шанс ответа {self.change_chance(int(words[2]))}")
                                    else:
                                        self.sender(id, "Ожидался шанс в пределах 0-100")
                                except:
                                    self.sender(id, "Вы забыли указать шанс")
                        except:
                            self.sender(id, "Неизвестная команда")
                            
                    else:
                        print(self.chance)
                        random_message = random.randrange(1, 100, 1)
                        print(random_message)
                        if random_message in range (1, self.chance + 1):
                            self.sender(id, "Пися попа")

    


