import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import MAX_TOKEN

vk_token = MAX_TOKEN

vk_session = vk_api.VkApi(token = vk_token)
session_api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id = 217147732)

def sender(id, text):
    vk_session.method('messages.send', {
        'chat_id' : id, 
        'message' : text, 
        'random_id' : 0
    })

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        
        chance = 100
        msg = event.object.message['text'].lower()
        words = msg.split()
        
        if event.from_chat:
            id = event.chat_id 
            
            if words[0] == "max":
                try:
                    if words[1] == "chance":
                        try:
                            if int(words[2]) in range (0, 100):
                                chance = words[2]
                                sender(id, f"Установлен шанс ответа {chance}")
                        except:
                            sender(id, "Ожидался шанс в пределах 0-100")
                except:
                    sender(id, "Неизвестная команда")