from datetime import datetime
from typing import TYPE_CHECKING
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.member import Member, VoiceState

from gordotron.json_store import IntoUserId, JsonStore

if TYPE_CHECKING:
    from gordotron.__main__ import Gordotron


class VoiceTimer(commands.Cog):
    def __init__(self, bot: "Gordotron"):
        self.conf = bot.json_store
        self.bot = bot

    def vc_join(self, u: IntoUserId):
        self.conf.usr(u)["vc_join"] = datetime.now().timestamp()
        self.conf.commit()

    def vc_left(self, u: IntoUserId):
        usr = self.conf.usr(u)
        join = usr.get("vc_join")
        if isinstance(join, float):
            diff = abs(datetime.now() - datetime.fromtimestamp(join))
            usr["vc_join"] = None
            vc_time = usr.get("vc_time", 0.0)
            if isinstance(vc_time, float):
                vc_time += diff.total_seconds()
                usr["vc_time"] = vc_time
                self.conf.commit()

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if member == self.bot.user:
            return

        if after.channel:
            # just joined
            if before.channel is None:
                self.vc_join(member)

            # joined from AFK
            elif before.channel == member.guild.afk_channel:
                self.vc_join(member)

            # switched channels
            elif before.channel.id != after.channel.id:
                self.vc_left(member)
                self.vc_join(member)

            # left to afk channel
            elif after.channel.id == member.guild.afk_channel:
                self.vc_left(member)

        else:
            # left
            if before.channel:
                self.vc_left(member)


async def setup(bot):
    bot.add_cog(VoiceTimer(bot))
