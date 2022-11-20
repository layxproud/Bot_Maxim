import random

dict = {0:'зеленое', 1:'красное', 2:'черное', 3:'красное', 4:'черное', 5:'красное', 6:'черное',
        7:'красное', 8:'черное', 9:'красное', 10:'черное', 11:'красное', 12:'черное',
        13:'красное', 14:'черное', 15:'красное', 16:'черное', 17:'красное', 18:'черное',
        19:'красное', 20:'черное', 21:'красное', 22:'черное', 23:'красное', 24:'черное',
        25:'красное', 26:'черное', 27:'красное', 28:'черное', 29:'красное', 30:'черное',
        31:'красное', 32:'черное', 33:'красное', 34:'черное', 35:'красное', 36:'черное',}

def startRoulette(bot, chat_id, user):
    if user.chips == 0:
        bot.messageSender(chat_id, f"Игроку @id{user.vk_id}({user.name}) выдано 5000 фишек")
        user.chips += 5000
        user.save()

def winner(bot, user, bet, number, chat_id):
    bot.messageSender(chat_id, f"Выпало {number}, {dict[number]}. Вы победили!")
    user.chips += bet * 2
    user.save()
    
def loser(bot, user, bet, number, chat_id):
    bot.messageSender(chat_id, f"Выпало {number}, {dict[number]}. Вы проиграли!")
    user.chips -= bet
    user.save()

def rouletteBalance(bot, chat_id, user):
    bot.messageSender(chat_id, f"@id{user.vk_id}({user.name}), на вашем счету {user.chips} фишек")

def roulette(bot, chat_id, word_list, user):
    startRoulette(bot, chat_id, user)
    number = random.randrange(0, 37, 1)
    
    if len(word_list) == 3:
        on_what = word_list[1]
        bet = int(word_list[-1])
        if bet in range (0, user.chips + 1):
            if on_what in ["черное", "красное", "зеленое"]:
                if dict[number] == on_what:
                    winner(bot, user, bet, number, chat_id)
                else:
                    loser(bot, user, bet, number, chat_id)    
            elif on_what == "чет":
                if number % 2 == 0:
                    winner(bot, user, bet, number, chat_id)
                else:
                    loser(bot, user, bet, number, chat_id)
            elif on_what == "нечет":
                if number % 2 != 0:
                    winner(bot, user, bet, number, chat_id)
                else:
                    loser(bot, user, bet, number, chat_id)
            else:
                bot.messageSender(chat_id, "Нет такого поля")
        else:
            bot.messageSender(chat_id, f"Баланс недостаточен. Ваш баланс: {user.chips}")
    else:
        bot.messageSender(chat_id, "Делайте ставку. Возможные ставки: зеленое, красное, черное, чет, нечет. Команда: Рулетка СТАВКА СУММА_СТАВКИ")