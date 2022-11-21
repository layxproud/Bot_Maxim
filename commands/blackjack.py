import random

deck = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6,
        7: 7, 8: 8, 9: 9, 10: 10,
        'J': 10, 'Q': 10, 'K': 10, 'A': 11}

deck_list = [2, 3, 4, 5, 6, 7, 8, 9, 10,
             "J", "Q", "K", "A"]


def start_blackjack(bot, chat_id):
    bot.message_sender(chat_id, "Делайте ставку. Команда: "
                       "блэкджек СУММА_СТАВКИ")


def give_player_card(player):
    card = random.choice(deck_list)
    player.player_deck += str(card) + " "
    player.player_score += deck[card]
    player.save()


def give_dealer_card(player):
    card = random.choice(deck_list)
    player.dealer_deck += str(card) + " "
    player.dealer_score += deck[card]
    player.save()


def winner(bot, user, player, chat_id):
    bot.message_sender(chat_id, "Победа!\n"
                       f"Вы выиграли {player.bet * 2} фишек")
    user.chips += player.bet * 2
    user.save()
    clean_player(player)


def loser(bot, user, player, chat_id):
    bot.message_sender(chat_id, "Поражение!\n"
                       f"Вы потеряли {player.bet} фишек")
    user.chips -= player.bet
    user.save()
    clean_player(player)


def draw(bot, chat_id, player):
    bot.message_sender(chat_id, "Ничья!")
    clean_player(player)


def take_card(bot, chat_id, player, user):
    give_player_card(player)
    if player.dealer_score < 17:
        give_dealer_card(player)
    check_score(bot, chat_id, player, user)


def not_take_card(bot, chat_id, player, user):
    if player.dealer_score < 17:
        give_dealer_card(player)
    situation(bot, chat_id, player, user)


def clean_player(player):
    player.player_deck = ""
    player.dealer_deck = ""
    player.player_score = 0
    player.dealer_score = 0
    player.bet = 0
    player.is_playing = 0
    player.save()


def show_score(bot, chat_id, player):
    bot.message_sender(chat_id, f"Ваши карты: {player.player_deck}\n"
                       f"Текущий счет: {player.player_score}")
    bot.message_sender(chat_id, f"Карты дилера: {player.dealer_deck}\n"
                       f"Счет дилера: {player.dealer_score}")


def check_score(bot, chat_id, player, user):
    show_score(bot, chat_id, player)
    if player.player_score >= 21 or player.dealer_score >= 21:
        situation(bot, chat_id, player, user)
    bot.message_sender(chat_id, "Напишите 'взять карту', чтобы продолжить"
                       " игру, или 'хватит', чтобы завершить")


def situation(bot, chat_id, player, user):
    if player.player_score == player.dealer_score or \
            (player.player_score > 21 and player.dealer_score > 21):
        draw(bot, chat_id)
    elif player.player_score <= 21 and player.dealer_score > 21:
        winner(bot, user, player, chat_id)
    elif player.dealer_score <= 21 and player.player_score > 21:
        loser(bot, user, player, chat_id)
    elif player.player_score <= 21 and player.dealer_score <= 21 and \
            player.player_score > player.dealer_score:
        winner(bot, user, player, chat_id)
    else:
        loser(bot, user, player, chat_id)


def blackjack(bot, chat_id, user, player, word_list):
    if len(word_list) == 1:
        start_blackjack(bot, chat_id)
    elif len(word_list) == 2:
        bet = int(word_list[-1])
        player.bet = bet
        player.is_playing = 1

        give_player_card(player)
        give_player_card(player)
        give_dealer_card(player)
        give_dealer_card(player)

        check_score(bot, chat_id, player, user)
