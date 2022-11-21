from models import User, Blackjack


def get_user_by_id(user_id):
    try:
        return User().get(vk_id=user_id)
    except Exception:
        User(
            vk_id=user_id,
            warns=0,
            chips=1000,
            name=""
        ).save()
        return User().get(vk_id=user_id)


def get_bjplayer_by_id(user_id):
    try:
        return Blackjack().get(vk_id=user_id)
    except Exception:
        Blackjack(
            vk_id=user_id,
            player_deck='',
            player_score=0,
            dealer_deck='',
            dealer_score=0,
            bet=0,
            is_playing=0
        ).save()
        return Blackjack().get(vk_id=user_id)
