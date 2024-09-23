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

    @property
    def replies(self) -> PathlikeTree:
        return self._config["replies"]

    @property
    def brandon_id(self) -> int:
        return self._config["brandon_id"]  # type: ignore

    @property
    def jackson_id(self) -> int:
        return self._config["jackson_id"]  # type: ignore

    @property
    def caz_id(self) -> int:
        return self._config["caz_id"]  # type: ignore

    @property
    def jesse_id(self) -> int:
        return self._config["jesse_id"]  # type: ignore

    @property
    def ari_id(self) -> int:
        return self._config["ari_id"]  # type: ignore

    @property
    def general_chat_id(self) -> int:
        return self._config["general_chat_id"]  # type: ignore

    @property
    def brandon_vc_ids(self) -> List[int]:
        return self._config["brandon_vc_ids"]  # type: ignore

    @property
    def afk_vc_ids(self) -> List[int]:
        return self._config["afk_vc_ids"]  # type: ignore
