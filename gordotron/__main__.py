from pathlib import Path
import traceback
from typing import Any
import discord
from discord.ext import commands

from .config import EXTENSION_DIR, BOT_TOKEN
from .json_store import JsonStore


class Gordotron(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.json_store = JsonStore()

    async def on_error(self, event_method: str, *args: Any, **kwargs: Any) -> None:
        print(f"An error occurred in {event_method}.\n{traceback.format_exc()}")

    async def on_ready(self) -> None:
        assert self.user
        print(f"Logged in as {self.user} ({self.user.id})")

    async def setup_hook(self) -> None:
        for file in EXTENSION_DIR.glob("*.py"):
            await self.load_extension(f"{EXTENSION_DIR.stem}.{file.stem}")


bot = Gordotron(command_prefix="Linus-", intents=discord.Intents.all())
bot.run(BOT_TOKEN)
