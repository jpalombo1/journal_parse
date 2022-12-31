from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Entry:
    """Journal Entry object with number for year, total index, weekday, date, rating and actual content."""

    idx: int
    num: int
    weekday: str
    date: str
    rating: float = 0.0
    entry: str = "Entry (): \nRating: /10\nSummary:\nInfo/Learn:\nFeelings: \nStories: "

    def __post_init__(self) -> None:
        """Re-initialized entry based on filled in parameters."""
        self.entry = (
            f"Entry {self.num} ({self.idx}) {self.weekday} {self.date}\n"
            + "\n".join(self.entry.split("\n")[1:])
        )

    def modify_entry(self, type: str, new_val: Any):
        if type not in self.__dict__.keys():
            return

        new_val = get_date_str(new_val) if type == "date" else new_val
        self.__dict__[type] = new_val
        self.entry = (
            f"Entry {self.num} ({self.idx}) {self.weekday} {self.date}\n"
            + "\n".join(self.entry.split("\n")[1:])
        )


def make_entry(entry_text: str) -> Entry:
    """Make an entry from already made journals / line of text.

    Split text into lines, Then get idx num weekday date by lines that begin with Entry,
    then get rating by lines that begin with Rating.
    Only use first of each field then make entry from it.
    """
    lines = entry_text.split("\n")
    idx = [get_idx(line) for line in lines if "Entry " in line][0]
    num = [get_num(line) for line in lines if "Entry " in line][0]
    weekday = [get_weekday(line) for line in lines if "Entry " in line][0]
    date = [get_date_line_str(line) for line in lines if "Entry " in line][0]
    rating = [get_rating(line) for line in lines if "Rating" in line][0]
    entry = Entry(
        entry=entry_text, idx=idx, num=num, rating=rating, weekday=weekday, date=date
    )
    return entry


def get_idx(line: str) -> int:
    """Get index from line, will be in form of 'words blah blah (index) blah blah'"""
    return int(line.split("(")[-1].split(")")[0])


def get_num(line: str) -> int:
    """Get number from line, will be in form of 'words blah blah Entry: number blah blah'"""
    return int(line.split("Entry ")[-1].split(" ")[0])


def get_rating(line: str) -> float:
    """Get rating from line, will be in form of 'words blah blah Rating: rating/10 blah blah'"""
    val = line.split("Rating: ")[-1].split("/")[0]
    return float(val) if val.replace(".", "", 1).isdigit() else 0.0


def get_weekday(line: str) -> str:
    """Get number from line, will be in form of 'words blah blah: weekday blah blah'"""
    return line.split(": ")[-1].split(" ")[0]


def get_date_line_str(line: str) -> str:
    """Get date string from line, will be in form of 'words blah blah day date_str\n"""
    return line.split("day ")[-1].split("\n")[0]


def get_date_str(date: datetime) -> str:
    """Convert datetime date back to string."""
    return date.strftime("%m/%d/%Y")


def get_date_obj(date: str) -> datetime:
    """Convert string date to datetime object."""
    return datetime.strptime(date, "%m/%d/%Y")


def get_date_line_obj(line: str) -> datetime:
    """Convert string date on line to datetime object."""
    return get_date_obj(get_date_line_str(line))
