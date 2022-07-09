from disnake.ext import commands
import disnake
from Neruabot.utils.json_files import write_json_data, read_json_data
from Neruabot.Firebase.access import Access
import textwrap
from Neruabot.constants import constants


class LogHours(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.access = Access()
        self.path = "data.json"

    @commands.slash_command(name="view",
                            guild_ids=[constants['ids']['main server']['id'], constants['ids']['tutor server']['id']])
    async def view_hours(self, inter: disnake.CommandInteraction, user: disnake.User = None, view_all: bool = False):
        """
        Views volunteer hours

        Parameters
        ----------
        user: the user if you want to view someone else's hours
        view_all: if you want to view all the existing volunteer hours
        inter: discord interaction
        """
        if user is None:
            user = inter.author
        else:
            user = user

        if not view_all:
            _, user_dict = self.access.read_hours("teachers", str(user.id))
            if user_dict is None:
                hours = 0
            else:
                hours = user_dict['hours']
            embed = disnake.Embed(title="Volunteer Hours", description=f"{user.mention} has a total of `{hours}` hours", colour=disnake.Colour.fuchsia())
            await inter.response.send_message(embed=embed)

        elif view_all:
            embed = disnake.Embed(title="All avaliable volunteer hours", colour=disnake.Colour.random())
            all_dict = self.access.view_all_hours("teachers")
            new_dict = {}
            for key, val in all_dict.items():
                userrr = self.bot.get_user(int(key))
                name = userrr.display_name
                new_dict[name] = val
            for key, val in new_dict.items():
                embed.add_field(name=f"{key}", value=f"Hours:`{val['hours']}`")
            embed.set_footer(text=f"Requested by {inter.author.display_name}", icon_url=inter.author.avatar.url)
            await inter.response.send_message(embed=embed)


    @commands.slash_command(name="removehours",
                            guild_ids=[constants['ids']['main server']['id'], constants['ids']['tutor server']['id']])
    async def remove_volunteer_hours(self, inter: disnake.CommandInteraction, user: disnake.User, hours: float):
        """
        Removes a user's volunteer hours - only works for admin.

        Parameters
        ----------
        hours: the amount of hours you completed
        user: the person's volunteer hours you want to remove
        inter: discord interaction
        """
        userr = inter.author
        role_ids = [roles.id for roles in userr.roles]
        if inter.guild_id == constants['ids']['main server']['id']:
            # mod id
            if constants['ids']['main server']['hour'] not in role_ids:
                await inter.response.send_message(constants['errors']['role'])
                return

            self.access.remove_hours("teachers", user.id, hours)
            await inter.response.send_message(f"Removed `{hours}` hours from {user.mention}")

        elif inter.guild_id == constants['ids']['tutor server']['id']:
            # admin id
            if constants['ids']['tutor server']['hour'] not in role_ids:
                await inter.response.send_message(
                    constants['errors']['role'])
                return

            self.access.remove_hours("teachers", user.id, hours)
            await inter.response.send_message(f"Removed `{hours}` hours from {user.mention}")

    @commands.slash_command(name="loghours",
                            guild_ids=[constants['ids']['main server']['id'], constants['ids']['tutor server']['id']])
    async def log_volunteer_hours(self, inter: disnake.CommandInteraction, hours: float, reason: str):
        """
        Logs your volunteer hours to a database.

        Parameters
        ----------
        hours: the amount of hours you completed
        reason: what you finished
        inter: discord interaction
        """
        user = inter.author
        role_ids = [roles.id for roles in user.roles]

        embed = disnake.Embed(title="Volunteer hour approval", description=textwrap.dedent(
            f"""
                                {inter.author.mention} requested to log their volunteer hours!
                                `What they finished: {reason}`

                                Volunteer: `{inter.author.display_name}` 
                                Finished Hours: `{hours}`
                                """), colour=disnake.Colour.og_blurple()
                              )

        if inter.guild_id == constants['ids']['main server']['id']:
            if constants['ids']['main server']['vol'] not in role_ids:
                await inter.response.send_message("Sorry but the system detected that you are not a volunteer")
                return

            channel = self.bot.get_channel(constants['ids']['main server']['approve'])
            m = await channel.send(f"<@&{constants['ids']['main server']['hour']}>", embed=embed)
            await m.add_reaction("✅")
            await m.add_reaction("❌")

        elif inter.guild_id == constants['ids']['tutor server']['id']:
            channel = self.bot.get_channel(constants['ids']['tutor server']['approve'])
            m = await channel.send(f"<@&{constants['ids']['tutor server']['hour']}>", embed=embed)
            await m.add_reaction("✅")
            await m.add_reaction("❌")

        embed = disnake.Embed(title="Volunteer hours approval request sent!",
                              description=f"{inter.author.mention}, the bot will dm you if your hours were approved, please wait a while!",
                              colour=disnake.Colour.blurple())
        await inter.response.send_message(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        if payload.user_id == constants['ids']['bot']['id']:
            return
        if str(payload.emoji) == "✅" or "❌" and payload.guild_id == constants['ids']['main server']['id'] or constants['ids']['tutor server']['id'] and \
                payload.channel_id == constants['ids']['main server']['approve'] or constants['ids']['tutor server']['approve']:
            try:
                channel = self.bot.get_channel(payload.channel_id)

                messages = await channel.history(limit=10).flatten()
                for msg in messages:
                    if msg.id == payload.message_id:
                        embed = msg.embeds[0].to_dict()

                        str_person_id = str(embed['description'].split(">")[0].strip("<@!"))
                        reason = str(embed['description']).split("\n\n")[0].split("\n")[1].split(": ")[1].strip("`")
                        person = self.bot.get_user(int(str_person_id))
                        hours = float(embed['description'].split("\n\n")[1].split('\n')[1].split(": ")[1].strip("`"))

                        if str(payload.emoji) == "✅":
                            await msg.edit(f"Volunteer Hours Approved! 📝✍\n Action done by: {self.bot.get_user(payload.user_id).mention}\n Info: ```By: {person.display_name}\nReason:{reason}```", embeds=[])
                            self.access.add_hours("teachers", str_person_id, hours)
                            await person.send(
                                f"Volunteer Hours Approved! 📝✍!\nYour `{hours}` were approved, you can check it by sending the command `/view`!")

                        if str(payload.emoji) == "❌":
                            await msg.edit(f"Volunteer Hours Ignored! ⛔\n Action done by: {self.bot.get_user(payload.user_id).mention}\n Info: ```By: {person.display_name}\nReason:{reason}```", embeds=[])
            except IndexError:
                return
        else:
            return
