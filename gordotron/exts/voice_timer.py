from typing import TYPE_CHECKING
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.member import Member, VoiceState

from gordotron.config import AFK_VC_IDS

if TYPE_CHECKING:
    from gordotron.__main__ import Gordotron


class VoiceTimer(commands.Cog):
    def __init__(self, bot: "Gordotron"):
        self.conf = bot.json_store
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if member == self.bot.user:
            return

        if after.channel:
            # just joined
            if before.channel is None:
                self.conf.vc_join(member)

            # joined from AFK
            elif before.channel == member.guild.afk_channel:
                self.conf.vc_join(member)

            # switched channels
            elif before.channel.id != after.channel.id:
                self.conf.vc_left(member)
                self.conf.vc_join(member)

            # left to afk channel
            elif after.channel.id == member.guild.afk_channel:
                self.conf.vc_left(member)

        else:
            # left
            if before.channel:
                self.conf.vc_left(member)


async def setup(bot):
    bot.add_cog(VoiceTimer(bot))
