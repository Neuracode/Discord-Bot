from disnake.ext import commands
import disnake
import textwrap
import json


class requestTutor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session_path = "sessions.json"

    async def format_embed(self, inter: disnake.CommandInteraction, name, class_, additional_info, user_id=None,
                           **kwargs):
        description = textwrap.dedent(f"""
        `Name`: {name}
        `Class`: {class_}
        `Additional Information`: {additional_info}
        """)

        if user_id is not None:
            description = textwrap.dedent(f"""
            `Name`: {name}
            `Class`: {class_}
            `Additional Information`: {additional_info}
            `User ID`: {user_id}
            """)

        embed = disnake.Embed(title=kwargs['title'], description=description, colour=disnake.Colour.fuchsia())

        embed.set_footer(text=kwargs['footer_text'], icon_url=inter.user.avatar.url)
        return embed

    @commands.slash_command(name="request_tutor",
                            guild_ids=[941049795949264969])
    async def request_one_to_one(self, inter: disnake.CommandInteraction,
                                 your_name,
                                 your_class,
                                 additional_info=None):
        """
        Send a request to tutor to get one-on-one tutoring about coding

        Parameters
        ----------
        your_name: Your full name
        your_class: Your current class, if you are not enrolled, feel free to enroll here: https://neuracode.org/courses
        additional_info: Feel free to provide any additional info if you want to, this field is not required!
        inter: discord interaction
        """
        name = your_name
        embed = await self.format_embed(inter, name, your_class, additional_info, title="Success!",
                                        footer_text="A new request has been sent!")
        await inter.response.send_message(content="**Someone will assist you soon!**", embed=embed, ephemeral=True)

        channel = self.bot.get_channel(980145969465290753)
        embed = await self.format_embed(inter, name, your_class, additional_info, inter.user.id, title="New Request!",
                                        footer_text="A new request has appeared!")

        # <@&983121862118752287> A new request has appeared!\nReact to claim the role to help/tutor this student.

        m = await channel.send(
            content="A new request has appeared!\nReact to claim the role to help/tutor this student.", embed=embed)
        await m.add_reaction("<:Neuracode:982843662687940638>")

        student_data = {"name": name, "class": your_class, "info": additional_info}

        with open(self.session_path, 'r') as openfile:
            data = json.load(openfile)

        try:
            for values in data[str(inter.user.id)]:
                if values == student_data:
                    return
            data[str(inter.user.id)].append(student_data)
        except KeyError:
            data[str(inter.user.id)] = []
            data[str(inter.user.id)].append(student_data)

        json_object = json.dumps(data, indent=4)
        with open(self.session_path, "w") as outfile:
            outfile.write(json_object)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: disnake.RawReactionActionEvent):
        channel = self.bot.get_channel(payload.channel_id)
        guild = self.bot.get_guild(payload.guild_id)
        user = self.bot.get_user(payload.user_id)
        if channel.id != 980145969465290753 or payload.user_id == 982834951303102546 or payload.emoji.id != 982843662687940638:
            return
        sessions = disnake.utils.get(guild.categories, name="Private Sessions")
        with open(self.session_path, 'r') as openfile:
            data = json.load(openfile)

        found = False
        class_ = None
        user_id = 688572232087371955
        channels = disnake.utils.get(guild.text_channels, id=payload.channel_id)
        for message in await channels.history(limit=50).flatten():
            if message.id == payload.message_id:
                if found:
                    continue
                found = True
                embed_dict = message.embeds[0].to_dict()
                user_id = int(embed_dict['description'].split("\n")[3].split(": ")[1])
                student = disnake.utils.get(guild.members, id=user_id)
                class_ = embed_dict['description'].split("\n")[1].split(": ")[1]
                course_list = data[str(user_id)]
                await message.edit(content=f"Success! \n{user.mention} claimed the course request from {student.display_name} for {class_}!", embeds=[])

        student = disnake.utils.get(guild.members, id=user_id)
        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            user: disnake.PermissionOverwrite(view_channel=True),
            student: disnake.PermissionOverwrite(view_channel=True),
            guild.me: disnake.PermissionOverwrite(view_channel=True)
        }
        channel = await sessions.create_text_channel(name=f"Your {class_}", topic=f"{student.display_name}'s {class_} tutoring channel", overwrites=overwrites)

        # currently making up the course stuff, but it will display the amount of time, the tutor's discordname, the class info, what you need for this course,

        description = textwrap.dedent(text=f"""
        `Tutor's Name`: {user.display_name} | {user.mention}
        `Course`: {class_}
        """)
        embed = disnake.Embed(title="You have a tutor!", description=description)
        await channel.send(content=f"{student.mention} say hi to your teacher for `{class_}`: {user.mention}👋!", embed=embed)
