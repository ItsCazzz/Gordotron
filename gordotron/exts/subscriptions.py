from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, List, Tuple
from discord.channel import VocalGuildChannel
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.member import Member, VoiceState
from discord.mentions import AllowedMentions

from gordotron.json_store import IntoUserId, JsonStore

if TYPE_CHECKING:
    from gordotron.__main__ import Gordotron


class Subscriptions(commands.Cog):
    def __init__(self, bot: "Gordotron"):
        self.conf = bot.json_store
        self.bot = bot

    def subscribers(self, u: IntoUserId) -> List[int]:
        usr = self.conf.usr(u)
        subs = usr.get("subscribers", [])
        if isinstance(subs, list):
            return subs
        return []

    def vc_alert_mutes(self, u: IntoUserId) -> List[Tuple[datetime, datetime]]:
        usr = self.conf.usr(u)
        mutes = usr.get("vc_alert_mutes", [])
        if isinstance(mutes, list):
            mutes = [
                (datetime.fromtimestamp(start), datetime.fromtimestamp(end))
                for start, end in mutes
            ]
            return mutes
        return []

    def last_alert(self, u: IntoUserId) -> datetime:
        usr = self.conf.usr(u)
        last = usr.get("vc_alert_last", 0)
        if isinstance(last, int):
            return datetime.fromtimestamp(last)
        return datetime.min

    async def maybe_alert(
        self, joined: Member, channel: VocalGuildChannel, target: int
    ):
        for start, end in self.vc_alert_mutes(target):
            if end >= datetime.now(UTC) >= start:
                return

        if self.last_alert(target) < datetime.now() + timedelta(minutes=10):
            return  # less than 10 min since last alert

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
                for usr_id in self.subscribers(member):
                    await self.maybe_alert(member, after.channel, usr_id)

            # joined from AFK
            elif before.channel == member.guild.afk_channel:
                for usr_id in self.subscribers(member):
                    await self.maybe_alert(member, after.channel, usr_id)

    @commands.command()
    async def subscribe(self, ctx: commands.Context, member: Member):
        mentioned = self.conf.usr(member)
        if not "subscribers" in mentioned:
            mentioned["subscribers"] = [ctx.author.id]
            self.conf.commit()
            return

        subs = mentioned["subscribers"]
        if isinstance(subs, list):
            subs.append(ctx.author.id)
            self.conf.commit()


async def setup(bot):
    bot.add_cog(Subscriptions(bot))
