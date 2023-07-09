import discord
from discord.ext import commands

from .utils.Trivia import trivia


def get_trivia(category=None, difficulty=None, type=None):
    new_trivia = trivia.get_trivia(category=None, difficulty=None, type=None)
    question = trivia.question(new_trivia)
    answers = trivia.all_answers_shuffled(new_trivia)
    correct_answer = trivia.answer(new_trivia)
    trivia_type = trivia.type(new_trivia)
    difficulty = trivia.difficulty(new_trivia)
    category = trivia.category(new_trivia)
    if ":" in category:
        category = category.split(":")[1]
        category = category.strip()

    return question, answers, trivia_type, correct_answer, difficulty, category


def create_embed(title, description, color, question, category, difficulty, trivia_type, answers=None):
    if trivia_type == "boolean":
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        embed.add_field(
            name="**Category:**",
            value=f"| __{category}__ |",
        )

        embed.set_thumbnail(
            url="https://i.postimg.cc/L8q7qjz9/coollogo-com-111951555.png"
        )

        embed.add_field(
            name="**Difficulty:**",
            value=f"| __{difficulty}__ |",
        )

        embed.add_field(
            name="**Type:**",
            value=f"| __{trivia_type}__ |",
        )

        embed.add_field(
            name="Question",
            value=question,
        )

        return embed
    else:
        embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

        embed.add_field(
            name="**Category:**",
            value=f"| __{category}__ |",
        )

        embed.set_thumbnail(
            url="https://i.postimg.cc/L8q7qjz9/coollogo-com-111951555.png"
        )

        embed.add_field(
            name="**Difficulty:**",
            value=f"| __{difficulty}__ |",
        )

        embed.add_field(
            name="**Type:**",
            value=f"| __{trivia_type}__ |",
        )

        embed.add_field(
            name="Question",
            value=question,
        )

        embed.add_field(
            name="Answers:",
            value=f"**1.** *{answers[0]}*\n**2.** *{answers[1]}*\n**3.** *{answers[2]}*\n**4.** *{answers[3]}*",
            inline=False
        )

        return embed


class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="trivia", description="Get a random trivia question")
    async def trivia(self, ctx, title=None, description=None, category=None, difficulty=None):
        question, answers, trivia_type, correct_answer, difficulty, category = get_trivia(category=category,
                                                                                          difficulty=difficulty)
        color = discord.Color.random()
        embed = create_embed(title, description, color, question, category, difficulty, trivia_type, answers=answers)

        if trivia_type == "boolean":
            await ctx.send(embed=embed, view=TrueFalseButtons(correct_answer, trivia_type=trivia_type))
        else:
            await ctx.send(embed=embed,
                           view=MultipleQuestionButtons(correct_answer,
                                                        trivia_type=trivia_type, answers=answers))


class TrueFalseButtons(discord.ui.View):
    def __init__(self, correct_answer, trivia_type):
        super().__init__()
        self.correct_answer = correct_answer
        self.type = trivia_type

        self.guessed = []
        self.answered_correctly = []
        self.answered_incorrectly = []
        self.answered = []

    async def handle_already_guessed(self, interaction: discord.Interaction):
        if interaction.user.id in self.guessed:
            if interaction.user.id in self.answered_correctly:
                for user, answer in self.answered:
                    if user == interaction.user.id:
                        await interaction.response.send_message(f"You already answered {answer}, which was correct!",
                                                                ephemeral=True)
            elif interaction.user.id in self.answered_incorrectly:
                for user, answer in self.answered:
                    if user == interaction.user.id:
                        await interaction.response.send_message(f"You already answered {answer}, which was incorrect!",
                                                                ephemeral=True)

    async def handle_correct(self, interaction: discord.Interaction):
        if self.correct_answer == "True" and interaction.user.id not in self.guessed:
            await interaction.response.send_message(f"Your answer, {True}, was correct!", ephemeral=True)
            self.answered_correctly.append(interaction.user.id)
            self.answered.append((interaction.user.id, "True"))

    async def handle_incorrect(self, interaction: discord.Interaction):
        if self.correct_answer == "False" and interaction.user.id not in self.guessed:
            await interaction.response.send_message(f"Your answer, {False}, was incorrect!", ephemeral=True)
            self.answered_incorrectly.append(interaction.user.id)
            self.answered.append((interaction.user.id, "False"))

    async def handle_not_guessed(self, interaction: discord.Interaction):
        if interaction.user.id not in self.guessed:
            self.guessed.append(interaction.user.id)
            message = interaction.message.id
            message = await interaction.channel.fetch_message(message)
            embed = message.embeds[0]
            embed.set_footer(
                text=f"Correct: {len(self.answered_correctly)} | Incorrect: {len(self.answered_incorrectly)} | Total: {len(self.guessed)}")
            await message.edit(embed=embed)

    @discord.ui.button(label="True", style=discord.ButtonStyle.gray)
    async def true(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_correct(interaction)
        await self.handle_incorrect(interaction)
        await self.handle_already_guessed(interaction)
        await self.handle_not_guessed(interaction)

    @discord.ui.button(label="False", style=discord.ButtonStyle.gray)
    async def false(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_correct(interaction)
        await self.handle_incorrect(interaction)
        await self.handle_already_guessed(interaction)
        await self.handle_not_guessed(interaction)


class MultipleQuestionButtons(discord.ui.View):
    def __init__(self, correct_answer, trivia_type, answers):
        super().__init__()
        self.correct_answer = correct_answer
        self.type = trivia_type
        self.answer_one = answers[0]
        self.answer_two = answers[1]
        self.answer_three = answers[2]
        self.answer_four = answers[3]

        self.guessed = []
        self.answered_correctly = []
        self.answered_incorrectly = []
        self.answered = []

    async def handle_already_guessed(self, interaction: discord.Interaction):
        if interaction.user.id in self.guessed:
            if interaction.user.id in self.answered_correctly:
                for user, answer in self.answered:
                    if user == interaction.user.id:
                        await interaction.response.send_message(f"You already answered {answer}, which was correct!",
                                                                ephemeral=True)
            elif interaction.user.id in self.answered_incorrectly:
                for user, answer in self.answered:
                    if user == interaction.user.id:
                        await interaction.response.send_message(f"You already answered {answer}, which was incorrect!",
                                                                ephemeral=True)

    async def handle_correct(self, interaction: discord.Interaction, answer):
        if self.correct_answer == answer and interaction.user.id not in self.guessed:
            await interaction.response.send_message(f"Your answer, {answer}, was correct!", ephemeral=True)
            self.answered_correctly.append(interaction.user.id)
            self.answered.append((interaction.user.id, answer))

    async def handle_incorrect(self, interaction: discord.Interaction, answer):
        if self.correct_answer != answer and interaction.user.id not in self.guessed:
            await interaction.response.send_message(f"Your answer, {answer}, was incorrect!", ephemeral=True)
            self.answered_incorrectly.append(interaction.user.id)
            self.answered.append((interaction.user.id, answer))

    async def handle_not_guessed(self, interaction: discord.Interaction):
        if interaction.user.id not in self.guessed:
            self.guessed.append(interaction.user.id)
            message = interaction.message.id
            message = await interaction.channel.fetch_message(message)
            embed = message.embeds[0]
            embed.set_footer(
                text=f"Correct: {len(self.answered_correctly)} | Incorrect: {len(self.answered_incorrectly)} | Total: {len(self.guessed)}")
            await message.edit(embed=embed)

    @discord.ui.button(label="Answer 1", style=discord.ButtonStyle.gray)
    async def answer_one(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.correct_answer == self.answer_one:
            await self.handle_correct(interaction, self.answer_one)
        await self.handle_incorrect(interaction, self.answer_one)
        await self.handle_already_guessed(interaction)
        await self.handle_not_guessed(interaction)

    @discord.ui.button(label="Answer 2", style=discord.ButtonStyle.gray)
    async def answer_two(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_correct(interaction, self.answer_two)
        await self.handle_incorrect(interaction, self.answer_two)
        await self.handle_already_guessed(interaction)
        await self.handle_not_guessed(interaction)

    @discord.ui.button(label="Answer 3", style=discord.ButtonStyle.gray)
    async def answer_three(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_correct(interaction, self.answer_three)
        await self.handle_incorrect(interaction, self.answer_three)
        await self.handle_already_guessed(interaction)
        await self.handle_not_guessed(interaction)

    @discord.ui.button(label="Answer 4", style=discord.ButtonStyle.gray)
    async def answer_four(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.handle_correct(interaction, self.answer_four)
        await self.handle_incorrect(interaction, self.answer_four)
        await self.handle_already_guessed(interaction)
        await self.handle_not_guessed(interaction)


def setup(bot):
    bot.add_cog(Trivia(bot))
