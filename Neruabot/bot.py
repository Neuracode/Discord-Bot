import itertools

import disnake
from disnake.ext import commands, tasks


class Neurobot(commands.Bot):
    def __init__(self):
        super().__init__(intents=disnake.Intents.all(), command_prefix=["n.", "N."])

        self.presences = itertools.cycle([disnake.Activity(name="People Code", type=disnake.ActivityType.watching, buttons={"label": "Join us!", "url": "https://neuracode.org/"})])
        self.remove_command('help')

    @tasks.loop(seconds=120)
    async def change_presence_(self):
        await self.change_presence(activity=next(self.presences))

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_presence_.start()
        print(f"{self.user.name} is ready")
