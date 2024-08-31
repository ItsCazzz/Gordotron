from datetime import datetime
import json
from pathlib import Path
from typing import List, Tuple, Union

from discord.abc import User
from discord.member import Member
from path_tree import PathlikeTree

IntoUserId = Union[Member, User, int]


class JsonStore:
    _path = Path(__file__).parent / "db.json"

    def __init__(self) -> None:
        if not self._path.exists():
            self._path.write_text("{}")

        with self._path.open() as f:
            self._config = PathlikeTree(json.load(f))

    def commit(self):
        with self._path.open("w+") as f:
            json.dump(self._config, f)

    def usr(self, u: IntoUserId):
        if not isinstance(u, int):
            u = u.id
        return self._config["users"][u]

    def vc_join(self, u: IntoUserId):
        self.usr(u)["vc_join"] = datetime.now().timestamp()
        self.commit()

    def vc_left(self, u: IntoUserId):
        usr = self.usr(u)
        join = usr.get("vc_join")
        if isinstance(join, float):
            diff = abs(datetime.now() - datetime.fromtimestamp(join))
            usr["vc_join"] = None
            vc_time = usr.get("vc_time", 0.0)
            if isinstance(vc_time, float):
                vc_time += diff.total_seconds()
                usr["vc_time"] = vc_time
                self.commit()

    def subscribers(self, u: IntoUserId) -> List[int]:
        usr = self.usr(u)
        subs = usr.get("subscribers", [])
        if isinstance(subs, list):
            return subs
        return []

    def vc_alert_mutes(self, u: IntoUserId) -> List[Tuple[datetime, datetime]]:
        usr = self.usr(u)
        mutes = usr.get("vc_alert_mutes", [])
        if isinstance(mutes, list):
            mutes = [
                (datetime.fromtimestamp(start), datetime.fromtimestamp(end))
                for start, end in mutes
            ]
            return mutes
        return []
