from typing import TYPE_CHECKING
from discord import TextChannel
from discord.ext import commands
from discord.member import Member, VoiceState
from discord.mentions import AllowedMentions

if TYPE_CHECKING:
    from gordotron.__main__ import Gordotron

everyone = AllowedMentions(everyone=True)


class BrandonWaitingRoom(commands.Cog):
    def __init__(self, bot: "Gordotron"):
        self.conf = bot.json_store
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if member.id != self.conf.brandon_id:
            return

        text_channel = self.bot.get_channel(self.conf.general_chat_id)
        if not isinstance(text_channel, TextChannel):
            raise ValueError("general needs to be text channel")

        # if brandon joins any chanel, set its name
        if after.channel and after.channel.id in self.conf.brandon_vc_ids:
            await after.channel.edit(name="BRANDON IS HERE!!!")

        # if brandon leaves, reset
        if before.channel and before.channel.id in self.conf.brandon_vc_ids:
            await before.channel.edit(name="brandon waiting room")

        # send alert if he joined
        if before.channel is None and after.channel:
            async with text_channel.typing():
                await text_channel.send(
                    content="@everyone BRANDON IS HERE!!!",
                    allowed_mentions=everyone,
                )


async def setup(bot):
    bot.add_cog(BrandonWaitingRoom(bot))
