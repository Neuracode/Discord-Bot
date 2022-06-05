import os
from dotenv import load_dotenv
load_dotenv()

from Neruabot import Neurobot
from Neruabot import requestTutor
bot = Neurobot()

if __name__ == '__main__':
    bot.add_cog(requestTutor(bot))
    bot.run(os.getenv("TOKEN"))
