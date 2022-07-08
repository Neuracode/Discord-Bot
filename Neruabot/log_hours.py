from disnake.ext import commands
import disnake

class LogHours(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="loghours",
                            guild_ids=[941049795949264969, 991799149357957230])
    async def log_volunteer_hours(self, inter: disnake.CommandInteraction, hours: int):
        """
        Logs your volunteer hours to a database.

        Parameters
        ----------
        hours: the amount of hours you completed
        inter: discord interaction
        """

        
