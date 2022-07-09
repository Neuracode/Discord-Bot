import os
from dotenv import load_dotenv
load_dotenv()

from Neruabot import Neurobot
from Neruabot import requestTutor
from Neruabot import createVc
from Neruabot import LogHours
from Neruabot import Help

bot = Neurobot()

if __name__ == '__main__':
    bot.add_cog(requestTutor(bot))
    # bot.add_cog(createVc(bot))
    bot.add_cog(Help(bot))
    bot.add_cog(LogHours(bot))
    bot.run(os.getenv("TOKEN"))
