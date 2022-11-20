from bot import Bot
from config import MAX_TOKEN, LINES_DIR, MAX_ID

if __name__ == "__main__":
    bot = Bot(MAX_TOKEN, MAX_ID, LINES_DIR, 100)
    bot.listen()