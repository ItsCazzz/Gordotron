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

NUMBER_REGEX = re.compile(r"\d+")
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"
TIME_FORMAT = "%H:%M:%S"
TIME_FORMATER = datetime.strptime("0:0:0", TIME_FORMAT)
