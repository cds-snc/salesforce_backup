from typing import Any
from pprint import PrettyPrinter


def write_to_file(things: list[dict[str, Any]]):
    pp = PrettyPrinter(indent=2)
    with open("fields.txt", "w") as f:
        for thing in things:
            f.write(pp.pformat(thing))