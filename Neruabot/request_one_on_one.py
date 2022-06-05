from disnake.ext import commands
import disnake
import textwrap

class requestTutor(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def format_embed(self, inter: disnake.CommandInteraction, name, class_, additional_info, **kwargs):
        description = textwrap.dedent(f"""
        Name: {name}
        Class: {class_}
        Additional Information: {additional_info}
        """)
        embed = disnake.Embed(title=kwargs['title'], description=description, colour=disnake.Colour.fuchsia())

        embed.set_footer(text=kwargs['footer_text'], icon_url=inter.user.avatar.url)
        return embed

    @commands.slash_command(name="request_tutor",
                            guild_ids=[941049795949264969])
    async def request_one_to_one(self, inter: disnake.CommandInteraction,
                                 name,
                                 your_class,
                                 additional_info=None):
        """
        Send a request to tutor to get one-on-one tutoring about coding

        Parameters
        ----------
        name: Your full name
        your_class: Your current class, if you are not enrolled, feel free to enroll here: https://neuracode.org/courses
        additional_info: Feel free to provide any additional info if you want to, this field is not required!
        inter: discord interaction
        """
        embed = await self.format_embed(inter, name, your_class, additional_info, title="Success!", footer_text="A new request has been sent!")
        await inter.response.send_message(content="**Someone will assist you soon!**", embed=embed, ephemeral=True)
        channel = self.bot.get_channel(980145969465290753)
        embed = await self.format_embed(inter, name, your_class, additional_info, title="New Request!", footer_text="A new request has appeared!")
        m = await channel.send(content="<@&980144866384302222> A new request has appeared!\nReact to claim the role to help/tutor this student.", embed=embed)
        await m.add_reaction("<:Neuracode:982843662687940638>")
