from config import MAX_TOKEN, GROUP_ID
from bot import Bot

if __name__ == "__main__":
    bot = Bot(MAX_TOKEN, GROUP_ID)
    bot.listen()