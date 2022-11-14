from bot import MAX_ID, Bot
from config import MAX_TOKEN, LINES_DIR

if __name__ == "__main__":
    bot = Bot(MAX_TOKEN, MAX_ID, LINES_DIR, 100)
    bot.listen()