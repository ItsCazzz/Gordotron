from pathlib import Path
import re
from typing import TYPE_CHECKING
from discord import Message, TextChannel
import discord
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
        if message.author == self.bot.user:
            return

        replies = self.conf.replies
        for rep in replies.keys():
            rep = str(rep)
            if re.match(rep, message.content):
                msg = replies[rep].get("msg", "")
                file = replies[rep].get("file", "")
                if len(file) == 0:
                    await message.reply(msg)
                else:
                    await message.reply(
                        msg, file=discord.File(Path("./assets/") / file)
                    )


async def setup(bot):
    bot.add_cog(JacksonCurse(bot))
