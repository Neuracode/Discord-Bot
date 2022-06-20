import disnake
from disnake.ext import commands
from Neruabot.utils.json_files import write_json_data, read_json_data

class createVc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.session_path = "students.json"
        self.teachers = "teachers.json"
        return

    @commands.slash_command(name="start_vc", guild_ids=[941049795949264969])
    async def start_vc(self,
                       inter: disnake.CommandInteraction,
                       student: disnake.User,
                       teacher: disnake.member.Member):
        """
        Start a private vc with your student

        Parameters
        ----------
        student: The student in the 1-to-1 class
        teacher: The teacher in the 1-to-1 class
        inter: discord interaction
        """
        user_roles = teacher.roles
        user_roles_ids = []
        for role in user_roles:
            user_roles_ids.append(role.id)
        if 980144866384302222 not in user_roles_ids:
            await inter.response.send_message(f"{inter.author.mention}, sorry, we currently don't allow students to start vc sessions.")
            return

        overwrites = {
            inter.guild.default_role: disnake.PermissionOverwrite(view_channel=False),
            teacher: disnake.PermissionOverwrite(view_channel=True),
            student: disnake.PermissionOverwrite(view_channel=True),
            inter.guild.me: disnake.PermissionOverwrite(view_channel=True)
        }
        sessions = disnake.utils.get(inter.guild.categories, name="Private Sessions")
        vc = await sessions.create_voice_channel(name=f"{student.display_name} - tutoring channel", overwrites=overwrites)
        student_data = read_json_data(self.session_path)
        teacher_data = read_json_data(self.teachers)
        try:
            teacher_data[str(teacher.id)]["vcid"] = vc.id
            teacher_data[str(teacher.id)]["svc"] = "True"
            teacher_data[str(teacher.id)]["with_who_vc"] = student.id
            write_json_data(teacher_data, self.teachers)
        except KeyError:
            await inter.response.send_message(f"{teacher.mention}, please do not create a vc if you don't have any students!")
            return
        try:
            student_data[str(student.id)]["svc"] = "True"
            student_data[str(student.id)]["vcid"] = vc.id
            student_data[str(student.id)]["with_who_vc"] = teacher.id
            write_json_data(student_data, self.session_path)
        except KeyError:
            await inter.response.send_message(f"{teacher.mention}, please make sure you are selecting the correct student!")
            return
        await inter.response.send_message(f"Vc created for {teacher.display_name} and {student.display_name}")
        return


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.member.Member, before: disnake.VoiceState, after: disnake.VoiceState):
        student_data = read_json_data(self.session_path)
        teacher_data = read_json_data(self.teachers)
        strike = 0
        session_start = False
        try:
            teacher = teacher_data[str(member.id)]
            if teacher["svc"] == "True":
                if after.channel is not None:
                    if teacher['vcid'] == after.channel.id:
                        teacher["invc"] = "True"
            if teacher["invc"] and student_data[teacher["with_who_vc"]]['invc'] == "True":
                session_start = True
            else:
                strike += 1
        except KeyError:
            strike += 1

        try:
            student = student_data[str(member.id)]
            if student["svc"] == "True":
                if after.channel is not None:
                    if student['vcid'] == after.channel.id:
                        student["invc"] = "True"

            if student["invc"] and teacher_data[student["with_who_vc"]]['invc'] == "True":
                session_start = True
            else:
                strike += 1
        except KeyError:
            strike += 1

        print(session_start)

        if strike == 2:
            return

        print(before)
        print(after)
        write_json_data(student_data, self.session_path)
        write_json_data(teacher_data, self.teachers)

    # i want to make a def strike counter but kinda lazy xd
