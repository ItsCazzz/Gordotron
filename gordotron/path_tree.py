from typing import List, Union, Dict, Any, DefaultDict, Optional, TypeVar, overload
from collections import defaultdict

KT = str | int
TreeDict = Dict[KT, Union[Any, "TreeDict"]]
TreeDefaultDict = DefaultDict[KT, Union[Any, "TreeDefaultDict"]]
T = TypeVar("T")


class PathlikeTree(defaultdict[KT, Union[Any, "PathlikeTree"]]):
    def __init__(self, nested_dict: Optional[TreeDict] = None):
        if nested_dict:
            # this is our replacement for the nested dict
            d = PathlikeTree()
            # for each item
            for k, v in nested_dict.items():
                # if its a dict, crate a new PathlikeTree, recursing this
                if isinstance(v, dict):
                    d[k] = PathlikeTree(v)
                else:
                    d[k] = v

            # store our inner tree
            super().__init__(self.__class__, d)
        else:
            super().__init__(self.__class__)

    def __getitem__(self, key: str | int) -> Union[Any, "PathlikeTree"]:
        if isinstance(key, str) and "." in key:
            deep = self
            for part in key.split("."):
                # if digit, try as int first
                if part.isdigit():
                    part_i = int(part)
                    # if neither or the int version exist, use int
                    if part not in deep or part_i in deep:
                        deep = deep[part_i]
                        continue

                # go one level deeper
                deep = deep[part]
            return deep
        return super().__getitem__(key)

    def __setitem__(self, key: str | int, value: Union[Any, "PathlikeTree"]) -> None:
        if isinstance(key, str) and "." in key:
            # split parts
            parts = key.split(".")
            # all keys before the last
            k = ".".join(parts[:-1])

            # self[k] will produce the default value (self) for the access path
            # then we do a normal assignment for the outermost key part
            self[k][parts[-1]] = value
            return
        super().__setitem__(key, value)

    def get(self, key: KT, default: T = None) -> T:
        try:
            v = self[key]
            if isinstance(v, PathlikeTree):
                return default
            return v  # type: ignore
        except KeyError:
            return default


pt_1 = PathlikeTree()
pt_1["a"]["b"][1]["d"] = 5
assert pt_1["a"]["b"][1]["d"] == 5
assert pt_1["a.b.1.d"] == 5

pt_2 = PathlikeTree()
pt_2["a.b.1.d"] = 5
assert pt_2["a"]["b"][1]["d"] == 5
assert pt_2["a.b.1.d"] == 5
