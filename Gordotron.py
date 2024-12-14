import json
from typing import TYPE_CHECKING, Any, DefaultDict, Dict, Optional, TypeVar, Union
import discord
import os
from discord.abc import User
from discord.ext import commands
from datetime import datetime
import asyncio
import random
import re
from pathlib import Path
from collections import defaultdict

from discord.member import Member, VoiceState
from discord.message import Message
from discord.threads import Thread

from dotenv import load_dotenv

load_dotenv()

ASSET_PATH = Path("./assets")

BOT_TOKEN = os.getenv("BOT_TOKEN")
assert BOT_TOKEN is not None, "Bot Token Not Found. ~Ari Stinks~"

JACKSON_SECRET_MESSAGE = os.getenv("JACKSON_SECRET_MESSAGE")
assert JACKSON_SECRET_MESSAGE is None, "Jackson message not found."

# declaring constants and global variables
BRANDON_ID = 159981115413626880
JACKSON_ID = 147309825296957440
CAZ_ID = 483750276977917983
JESSE_ID = 128283945203662848
ARI_ID = 1048693844750901359

GENERAL_CHAT_ID = 813512089259474946


brandon_vc_ids = [1116030251617759263]
afk_vc_ids = [1116030288322109531]

NUMBER_REGEX = re.compile(r"\d+")
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
TIME_FORMATER = datetime.strptime("0:0:0", TIME_FORMAT)


intents = discord.Intents.all()
intents.messages = True
intents.members = True

client = commands.Bot(command_prefix="Linus-", intents=intents)

everyone = discord.AllowedMentions(everyone=True)


class Assets:
    schwab = ASSET_PATH / "schawb.png"
    jojo = ASSET_PATH / "jojo.png"
    rigby_speech = ASSET_PATH / "Rigbyspeech.png"




def space_check(st: str, delimiter=" "):
    check = True

    lst = st.split(delimiter)  # create list of chars separated by space

    if len(lst) == 1:
        check = False

    for item in lst:
        if len(item) != 1:
            check = False
    return check


############ Compare Jackson's Hours to Average ############


def jackson_average():
    total = 0
    count = 0
    jackson_time = 0
    check = False

    with open("time.txt", "r") as f:
        lines = f.readlines()

        f.seek(0)

        for line in lines:
            split_line = line.split(",")

            if line.startswith(str(JACKSON_ID)):
                jackson_time = float(split_line[1])

            elif float(split_line[1]) > 0:
                total += float(split_line[1])
                count += 1

        f.close()

    average = total / count

    if average <= jackson_time:
        check = True

    return check


################################################################################################################################


@client.event
async def on_ready():
    print("ready")


############ Thread Edit ############


@client.event
async def on_thread_create(thread: Thread):
    """
    the bot will edit any thread that is crated to become
    inactive after 1 hour instead of the deafault of 7 days
    """
    await thread.edit(auto_archive_duration=60)


############ Add New Members to Leaderboard ############


@client.event
async def on_member_join(member: Member):
    if member == client.user:
        return

    with open("time.txt", "a") as f:
        f.write(f"{member.id}" + ",0, ,\n")
        f.close()

    with open("subscriptions.txt", "a") as f:
        f.write(f"{member.id},\n")
        f.close()


############ Remove Members From Leaderboard When Leaving Server ############


@client.event
async def on_member_remove(member: Member):
    if member == client.user:
        return

    with open("time.txt", "r+") as f:
        lines = f.readlines()

        f.seek(0)

        for line in lines:
            if not line.startswith(f"{member.id}"):
                f.write(line)

        f.close()

    with open("subscriptions.txt", "r+") as f:
        lines = f.readlines()

        f.seek(0)

        for line in lines:
            if not line.startswith(f"{member.id}"):
                f.write(line)

        f.close()


@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    if member == client.user:
        return

    text_channel = client.get_channel(GENERAL_CHAT_ID)

    if not isinstance(text_channel, discord.TextChannel):
        raise Exception("Dont be an idiot!!! General Chat is no longer a text channel!")

    ############ vc time leaderboard ############

    if (
        (not before.channel) or (before.channel and before.channel.id in afk_vc_ids)
    ) and (after.channel and after.channel.id not in afk_vc_ids):
        join_time = datetime.now().strftime(DATETIME_FORMAT)

        with open("time.txt", "r+") as f:
            lines = f.readlines()

            f.seek(0)
            f.truncate()

            for line in lines:
                if line.startswith(f"{member.id}"):
                    split_ln = line.split(",")
                    split_ln[2] = join_time
                    new_line = ",".join(split_ln)
                    f.write(new_line)

                else:
                    f.write(line)

            f.close()

    elif ((not after.channel) or after.channel.id in afk_vc_ids) and (
        before.channel and before.channel.id not in afk_vc_ids
    ):
        leave_time = datetime.now().strftime(DATETIME_FORMAT)
        leave_time = datetime.strptime(leave_time, DATETIME_FORMAT)

        with open("time.txt", "r+") as f:
            lines = f.readlines()

            f.seek(0)
            f.truncate()

            for line in lines:
                if line.startswith(f"{member.id}"):
                    split_ln = line.split(",")

                    if split_ln[2] != " ":
                        joined_time = datetime.strptime(split_ln[2], DATETIME_FORMAT)

                        previous_time = float(split_ln[1])

                        new_time_in_vc = (leave_time - joined_time).total_seconds() / (
                            # Mogdello Time!!!
                            60
                            * 60
                        )

                        split_ln[1] = f"{previous_time + new_time_in_vc}"
                        new_line = ",".join(split_ln)
                        f.write(new_line)

                    else:
                        f.write(line)

                else:
                    f.write(line)

            f.close()

    ############ Subcriptions ############

    if not before.channel and after.channel:
        with open("subscriptions.txt", "r") as f:
            lines = f.readlines()

            current_vc_users = []
            for discord_member in after.channel.members:
                current_vc_users.append(discord_member.id)

            for line in lines:
                line_contents = line.split(",")

                if (
                    str(member.id) in line_contents[1:]
                    and int(line_contents[0]) not in current_vc_users
                ):
                    subscribed_member = await client.fetch_user(int(line_contents[0]))
                    print(subscribed_member)
                    await subscribed_member.send(
                        f'<@{subscribed_member.id}> {member.global_name} just joined the "{after.channel.name}" vc!!!'
                    )

            f.close()

    ############ Brandon Waiting Room ############

    if member.id == BRANDON_ID:
        if before.channel and after.channel:
            if (
                before.channel.id in brandon_vc_ids
                and after.channel.id in brandon_vc_ids
            ):
                await before.channel.edit(name="brandon waiting room")
                await after.channel.edit(name="BRANDON IS HERE!!!")

            elif after.channel.id in brandon_vc_ids:
                await after.channel.edit(name="BRANDON IS HERE!!!")
                async with text_channel.typing():
                    await text_channel.send(
                        content="@everyone BRANDON IS HERE!!!",
                        allowed_mentions=everyone,
                    )

            elif (
                before.channel.id in brandon_vc_ids
                and after.channel.id not in brandon_vc_ids
            ):
                await before.channel.edit(name="brandon waiting room")

        elif (
            not before.channel and after.channel and after.channel.id in brandon_vc_ids
        ):
            await after.channel.edit(name="BRANDON IS HERE!!!")
            async with text_channel.typing():
                await text_channel.send(
                    content="@everyone BRANDON IS HERE!!!", allowed_mentions=everyone
                )

        elif (
            not after.channel and before.channel and before.channel.id in brandon_vc_ids
        ):
            await before.channel.edit(name="brandon waiting room")


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return
    if message.guild is None:
        return

    jackson_imunity = False

    ############ Subcriptions ############

    if message.content.startswith("!subscribe ") and len(message.mentions) > 0:
        for user in message.mentions:
            if user.id != message.author.id:
                with open("subscriptions.txt", "r") as f:
                    lines = f.readlines()
                    f.close()

                line_count = 0
                for line in lines:
                    line_contents = line.split(",")

                    if line.startswith(str(message.author.id)):
                        if str(user.id) not in line:
                            lines[line_count] = (
                                lines[line_count].strip() + str(user.id) + ",\n"
                            )
                            with open("subscriptions.txt", "w") as f:
                                f.writelines(lines)
                                f.close()

                    line_count += 1

    ############ Jackson Curse ############

    if message.content.lower() == "jackson, i curse thee":
        with open("jackson.txt", "r+") as f:
            lines = f.readlines()

            if len(lines) > 0:
                if lines[0] != "curse":
                    f.seek(0)
                    f.truncate()

                    f.write("curse")

            else:
                f.write("curse")

            f.close()

    ############ Schwab ############

    if "schwab" in message.content.lower():
        async with message.channel.typing():
            await asyncio.sleep(1.3)
            await message.channel.send(file=discord.File(Assets.schwab))

        chance = 2

    ############ jojo ############

    elif "jojo" in message.content.lower():
        async with message.channel.typing():
            await asyncio.sleep(1.3)
            await message.channel.send(file=discord.File(Assets.jojo))

        chance = 2

    ############ show leaderboard ############

    elif message.content == "!leaderboard":
        dict = {}
        message_content = ""

        with open("time.txt", "r") as f:
            lines = f.readlines()

            for line in lines:
                line_contents = line.split(",")

                total_time = line_contents[1]

                dict[line_contents[0]] = float(total_time)

            sorted_dict = sorted(dict.items(), key=lambda x: x[1])

            f.close()

        count = 1
        for user in reversed(sorted_dict):
            user_obj = client.get_user(int(user[0]))
            username = ""

            if user_obj is not None:
                username = user_obj.display_name
            else:
                with open("time.txt", "w") as f:
                    list_count = 0
                    for line in lines:
                        line_contents = line.split(",")

                        if line_contents[0] == user[0]:
                            del lines[list_count]
                            for line in lines:
                                f.write(line)

                        list_count += 1
                    f.close()

            message_content += f"{count}. {username}: {user[1]:.2f} hours\n"

            count += 1

        embed = discord.Embed(
            colour=discord.Colour.dark_grey(),
            title="VC Leaderboard",
            description=message_content,
        )

        await message.channel.send(embed=embed)

    ############ Jackson Messages ############

    if message.author.id == JACKSON_ID:
        msg_num = NUMBER_REGEX.search(message.guild.name)

        if msg_num is not None:
            jcksn_msg_num = int(msg_num.group())
        else:
            raise Exception("There is no number in server name for Jackson's messages.")

        if jcksn_msg_num == 0:
            await message.channel.send(
                "You have run out of message tokens. Boost this server for 500 more message tokens."
            )
            await message.delete()

        else:
            message_weight = 1
            rigby_chance = random.randint(1, 50)
            bonus_chance = random.randint(1, 15)

            with open("jackson.txt", "r+") as f:
                lines = f.readlines()

                if bonus_chance == 1 and (len(lines) == 0 or lines[0] != "curse"):
                    jackson_imunity = True
                    message_weight = -1
                    await message.add_reaction("<:schwabstache:1047284248157106266>")

                elif (message.content).isdigit():
                    pass
                elif len(message.content) != 0 and message.content == (
                    len(message.content) * "?"
                ):
                    message_weight = 10
                    print("Condition 1")
                elif message.content.lower() == f"please {JACKSON_SECRET_MESSAGE}":
                    jackson_imunity = True
                    message_weight = -1
                    print("Condition 2")
                elif (
                    message.content
                    == "https://tenor.com/view/caption-jackson-jackson-cowecord-gif-23559701"
                ):
                    message_weight = 15
                    print("Condition 3")
                elif "n0thing" in message.content.lower():
                    jackson_imunity = True
                    message_weight = -1
                    print("Condition 4")
                elif "redpill" in message.content.lower():
                    message_weight = 1500
                    print("Condition 5")
                elif message.content.lower() == "what":
                    message_weight = 10
                    print("Condition 6")
                elif message.content.lower() == "wait":
                    message_weight = 5
                    print("Condition 7")
                elif message.content.lower() == "wait what":
                    message_weight = 35
                    print("Condition 8")
                elif space_check(message.content):
                    message_weight = 50
                    print("Condition 9")

                if (
                    message.content.isupper()
                    and (not message.content.isdigit())
                    and not jackson_imunity
                ):
                    message_weight *= 3
                    print("Condition 10")

                if len(lines) == 1 and lines[0] == "curse":
                    message_weight *= 3
                    print("Condition 11")

                    f.seek(0)
                    f.truncate()

                f.close()

            if not jackson_average() and not jackson_imunity:
                message_weight *= 2
                print("Condition 12")

            if (jcksn_msg_num - message_weight) <= 0:
                await message.guild.edit(name="(0 Jackson messages remaining)")
            else:
                await message.guild.edit(
                    name=f"({jcksn_msg_num-message_weight} Jackson messages remaining)"
                )

            if rigby_chance == 1:
                async with message.channel.typing():
                    await asyncio.sleep(1.3)
                    await message.channel.send(file=discord.File(Assets.rigby_speech))

    ############ Ari Message ############

    if message.author.id == ARI_ID:
        num = random.randint(1, 500)

        if num == 1:
            async with message.channel.typing():
                await asyncio.sleep(1.3)
                await message.reply("aristinko 🤢")
        if num == 2:
            async with message.channel.typing():
                await asyncio.sleep(1.3)
                await message.reply(":face_vomiting:")

    ############ Steal Message ############

    chance = random.randint(1, 500)

    if (
        len(message.content) > 0
        and (chance == 1)
        and not jackson_imunity
        and not message.content.startswith(".")
    ):
        new_msg = message.content
        await message.delete()
        await message.channel.send(new_msg)
    elif jackson_imunity:
        jackson_imunity = False


client.run(BOT_TOKEN)
