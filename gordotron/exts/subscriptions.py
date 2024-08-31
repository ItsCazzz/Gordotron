from datetime import UTC, datetime
from typing import TYPE_CHECKING
from discord.channel import VocalGuildChannel
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.member import Member, VoiceState
from discord.mentions import AllowedMentions

from gordotron.config import AFK_VC_IDS

if TYPE_CHECKING:
    from gordotron.__main__ import Gordotron


class Subscriptions(commands.Cog):
    def __init__(self, bot: "Gordotron"):
        self.conf = bot.json_store
        self.bot = bot

    async def maybe_alert(
        self, joined: Member, channel: VocalGuildChannel, target: int
    ):
        for start, end in self.conf.vc_alert_mutes(target):
            if end >= datetime.now(UTC) >= start:
                return
        target_user = await self.bot.fetch_user(target)

        dm_channel = target_user.dm_channel
        if dm_channel is None:
            dm_channel = await target_user.create_dm()

        await dm_channel.send(
            f"{joined.mention} just joined {channel.mention}",
            allowed_mentions=AllowedMentions(everyone=True),
        )

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if member == self.bot.user:
            return

        if after.channel:
            # just joined
            if before.channel is None:
                for usr_id in self.conf.subscribers(member):
                    await self.maybe_alert(member, after.channel, usr_id)

            # joined from AFK
            elif before.channel == member.guild.afk_channel:
                for usr_id in self.conf.subscribers(member):
                    await self.maybe_alert(member, after.channel, usr_id)

            # on channel switch?


async def setup(bot):
    bot.add_cog(Subscriptions(bot))