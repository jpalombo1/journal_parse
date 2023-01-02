from dataclasses import dataclass
from datetime import datetime


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
        self.dateobj = get_date_obj(self.date)
        self.modify_entry()

    def modify_entry(self) -> None:
        """Change entry string depending on updated class field values, then use rest of the entry after Entry line."""
        self.entry = (
            f"Entry {self.num} ({self.idx}): {self.weekday} {self.date}\n"
            + "\n".join(self.entry.split("\n")[1:])
        )


def make_entry(entry_text: str) -> Entry:
    """Make an entry from already made journals / line of text.

    Split text into lines, Then get idx num weekday date by lines that begin with Entry,
    then get rating by lines that begin with Rating.
    Only use first of each field then make entry from it.

    Each entry with format:
    Entry <entry_num> (<index>): <Weekday> <date MM/dd/yyy>
    Rating <rating>/10:
    <rest of entry text>
    """
    lines = entry_text.split("\n")
    entry_line = [line for line in lines if "Entry " in line][0]
    rating_line = [line for line in lines if "Rating" in line][0]
    entry = Entry(
        entry=entry_text,
        idx=get_idx(entry_line),
        num=get_num(entry_line),
        rating=get_rating(rating_line),
        weekday=get_weekday(entry_line),
        date=get_date_line_str(entry_line),
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
