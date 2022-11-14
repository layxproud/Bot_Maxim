from config import MAX_TOKEN, MAX_ID, LINES_DIR
from bot import Bot

if __name__ == "__main__":
    bot = Bot(MAX_TOKEN, MAX_ID, LINES_DIR, 100)
    bot.listen()