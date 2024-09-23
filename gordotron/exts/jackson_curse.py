from typing import TYPE_CHECKING
from discord import Message, TextChannel
from discord.ext import commands
from discord.member import Member, VoiceState
from discord.mentions import AllowedMentions

if TYPE_CHECKING:
    from gordotron.__main__ import Gordotron

everyone = AllowedMentions(everyone=True)


class JacksonCurse(commands.Cog):
    def __init__(self, bot: "Gordotron"):
        self.conf = bot.json_store
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user or message.author.id == self.conf.jackson_id:
            return

        if message.content == "jackson, i curse thee":
            self.conf.usr(self.conf.jackson_id)["cursed"] = True
            self.conf.commit()


async def setup(bot):
    bot.add_cog(JacksonCurse(bot))
