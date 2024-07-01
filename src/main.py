import os
import dotenv
from milk import MilkV

def main():
    dotenv.load_dotenv()
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

    bot = MilkV()
    bot.run(DISCORD_BOT_TOKEN)

if __name__ == "__main__":
    main()