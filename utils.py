from models import User


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
