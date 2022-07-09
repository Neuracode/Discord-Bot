import disnake
from disnake.ext import commands
import textwrap
from Neruabot.constants import constants
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description = textwrap.dedent((f"""
        **General**
        `/help` - also a help command
        **Volunteer Hours**
        `/loghours` [hours] [reason] - Logs your volunteer hours, mainly for curriculum creators
        `/view` (users) (view_all) - Views volunteer hours
        *Admin*
        `/removehours` [users] [hours] - Removes hours form a volunteer
        """))

    @commands.slash_command(name="help", guild_ids=[constants['ids']['main server']['id'], constants['ids']['tutor server']['id']])
    async def slash_help(self, inter: disnake.ApplicationCommandInteraction):
        """
        Help panel

        Parameters
        ----------
        inter: discord interaction
        """
        embed = disnake.Embed(title="Help Panel", description=self.description, color=disnake.Color.og_blurple())
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Requested by {inter.author.name}", icon_url=inter.author.avatar.url)
        await inter.response.send_message(embed=embed)