import os
from pathlib import Path
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EXTENSION_DIR = Path("exts")


def getenv(var: str) -> str:
    val = os.getenv(var)
    if val is None:
        raise Exception(f"Required env-var {var} not found, check .env")
    return val


BOT_TOKEN = getenv("BOT_TOKEN")

JACKSON_SECRET_MESSAGE = getenv("JACKSON_SECRET_MESSAGE")

# declaring constants and global variables
BRANDON_ID = 159981115413626880
JACKSON_ID = 147309825296957440
CAZ_ID = 483750276977917983
JESSE_ID = 128283945203662848
ARI_ID = 1048693844750901359

GENERAL_CHAT_ID = 813512089259474946

BRANDON_VC_IDS = [1116030251617759263]
AFK_VC_IDS = [1116030288322109531]

NUMBER_REGEX = re.compile(r"\d+")
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
TIME_FORMATER = datetime.strptime("0:0:0", TIME_FORMAT)
