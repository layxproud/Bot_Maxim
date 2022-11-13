from config import MAX_TOKEN, MAX_ID
from bot import Bot

if __name__ == "__main__":
    bot = Bot(MAX_TOKEN, MAX_ID)
    bot.listen()