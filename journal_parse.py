from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


@dataclass
class Entry:
    idx: int
    num: int
    weekday: str
    date: str
    rating: float = 0.0
    entry: str = "Entry (): \nRating: /10\nSummary:\nInfo/Learn:\nFeelings: \nStories: "

    def __post_init__(self):
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


def get_idx(line: str) -> int:
    return int(line.split("(")[-1].split(")")[0])


def get_num(line: str) -> int:
    return int(line.split("Entry ")[-1].split(" ")[0])


def get_rating(line: str) -> float:
    val = line.split("Rating: ")[-1].split("/")[0]
    return float(val) if val.replace(".", "", 1).isdigit() else 0.0


def get_weekday(line: str) -> str:
    return line.split(": ")[-1].split(" ")[0]


def get_date_line_str(line: str) -> str:
    return line.split("day ")[-1].split("\n")[0]


def get_date_str(date: datetime) -> str:
    return date.strftime("%m/%d/%Y")


def get_date_obj(date: str) -> datetime:
    return datetime.strptime(date, "%m/%d/%Y")


def get_date_line_obj(line: str) -> datetime:
    return datetime.strptime(get_date_line_str(line), "%m/%d/%Y")


def make_entry(entry_text: str) -> Entry:
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


def check_entries(entries: list[Entry]):
    """Check if entries/dates increment appropriately."""
    ACTUAL_WEEKDAYS = [
        "Friday",
        "Saturday",
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
    ]

    entries.reverse()
    feature_names = ["num", "idx", "date", "weekday"]
    features = [[entry.__dict__[key] for entry in entries] for key in feature_names]

    # Check for ordered entries and indices and dates
    for name, arr in zip(feature_names, features):
        badVal = False
        for idx, (prev, next) in enumerate(zip(arr[:-1], arr[1:])):
            if name == "date" and get_date_obj(prev) != get_date_obj(next) - timedelta(
                days=1
            ):
                print(
                    f"Previous entry num {prev} Next entry num is {next} but should be {get_date_str((get_date_obj(prev) + timedelta(days=1)))}"
                )
                badVal = True
            elif name == "weekday" and ACTUAL_WEEKDAYS[idx % 7] != prev:
                print(
                    f"Actual weekday should be {ACTUAL_WEEKDAYS[idx % 7]} but weekday is {prev} on entry {idx}"
                )
                badVal = True
            elif name not in ["weekday", "date"] and prev != next - 1:
                print(
                    f"Previous entry num {prev} Next {name} num is {next} but should be {prev + 1}"
                )
                badVal = True
        if not badVal:
            print(f"No missing {name}.")


def set_vals(type: str, entries: list[Entry]) -> list[Entry]:
    new_entries = []
    for num_entries, entry in enumerate(entries):
        old_val = entry.__dict__[type]
        if num_entries == 0:
            first_val = old_val

        val = (
            get_date_obj(first_val) + timedelta(days=num_entries)
            if type == "date"
            else first_val + num_entries
        )
        entry.modify_entry(type, val)
        new_entries.append(entry)
    return new_entries


def fix_journals(entries: list[Entry]) -> list[Entry]:
    """Wrapper method to fix journals for all types of order errors."""
    entries = set_vals(type="date", entries=entries)
    entries = set_vals(type="num", entries=entries)
    entries = set_vals(type="idx", entries=entries)

    entries.reverse()
    all_content = "\n\n".join([entry.entry for entry in entries])
    with open("data/journal_new.txt", "w") as new_journal:
        new_journal.write(all_content)

    entries.reverse()
    return entries


def new_journals():
    entry = Entry(idx=1, num=2074, weekday="Wednesday", date="01/01/2022")
    entries = [Entry(**entry.__dict__) for _ in range(365)]
    fix_journals(entries)


def get_ratings(entries: list[Entry]) -> list[float]:
    """Gather ratings throughout year."""
    return [entry.rating for entry in entries]


def get_work(entries: list[Entry]) -> list[str]:
    """Get lines involving work"""
    return [
        f"{idx}.{line.split('work ')[-1].split(',')[0]}"
        for idx, entry in enumerate(entries)
        for line in entry.entry.split("\n")
        if "Summary" in line and "work " in line
    ]


def get_vocabulary(all_content: str, count: int) -> dict[str, int]:
    """Get top used words from all content."""

    def strip_chars(word: str) -> str:
        """Strip content of punctuation, special chars."""
        rm_chars = ' ,()-""\n/\'[]_.0123456789:#$%+=-*;<>@^`~“”’‘⅔'
        for char in rm_chars:
            word = word.replace(char, " ")
        return word

    edited_content = strip_chars(all_content).lower()
    words = edited_content.split(" ")
    words = [word for word in words if word != ""]
    unique_words, counts = np.unique(words, return_counts=True)
    uwc = {uq: cnt for uq, cnt in zip(unique_words, counts)}
    uwc = dict(sorted(uwc.items(), key=lambda x: x[1], reverse=True))
    top_uwc = {k: v for idx, (k, v) in enumerate(uwc.items()) if idx < count}
    return top_uwc


def word_counts(words: list[str], all_content: str):
    """Given list of strings give count of number of mentions."""
    return [all_content.count(word) for word in words]


def plot_histogram(
    labels: list[Any], counts: list[int], ax: Any, title="Histogram"
) -> Any:
    """Plot histogram of ratings."""
    bars = ax.bar(labels, counts)
    # access the bar attributes to place the text in the appropriate location
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + 0.01, yval + 0.01, yval)

    ax.set_title(title)
    return ax


def main():
    journalPath = "data/journals_2021.txt"
    with open(journalPath) as journalFile:
        lines = [str(line) for line in journalFile]
    all_content = "".join(lines)

    entries = [make_entry(entry_text) for entry_text in all_content.split("\n\n")]

    # Check entries
    check_entries(entries)
    # Modify journal values as needed
    entries = fix_journals(entries)
    new_journals()

    # Plots
    fig, ax = plt.subplots(6, figsize=(16, 8))
    ax = ax.reshape(6)
    fig.tight_layout()

    # Day rating
    ratings = get_ratings(entries)
    ratings_labels, ratings_dist = np.unique(ratings, return_counts=True)
    plot_histogram(ratings_labels, ratings_dist, ax=ax[0], title="Days with Rating")

    # Project counts
    projects = ["esce", "c3ewd", "wicked crow", "dragnet"]
    work_tasks = get_work(entries)
    work_content = "\n".join(work_tasks)
    proj_counts = word_counts(projects, work_content)
    plot_histogram(projects, proj_counts, ax=ax[1], title="Projects Worked on")

    # Person mentions
    NAMES = [
        "Katie",
        "Cooper",
        "Mom",
        "Dad",
        "Ali",
        "Chris",
        "Jay",
        "Harry",
        "Vinny",
        "Zach",
        "Julie",
        "Fisler",
        "Liam",
        "Nick",
        "Sue",
        "George",
        "James",
        "Jenna",
        "Makindree",
        "Alex",
    ]

    # Feelings counts
    FEELINGS = [
        "happy",
        "sad",
        "awful",
        "angry",
        "frustrated",
        "annoyed",
        "amazing",
        "excited",
        "worried",
        "awesome",
        "stressed",
        "funny",
        "hilarious",
        "bored",
        "boring",
        " fun ",
    ]

    # Activities Counts
    ACTIVTIES = [
        "drink",
        "bjj",
        "chess",
        "watch",
        "workout",
        "videos",
        "sex",
        "weights",
        "workout",
        "ate",
        "run",
        "switch",
        "spreadsheet",
    ]
    titles = ["Times People Mentioned", "Feelings Mentioned", "Activities Done"]

    for idx, (title, arr) in enumerate(zip(titles, [NAMES, FEELINGS, ACTIVTIES])):
        counts = word_counts(arr, all_content)
        plot_histogram(arr, counts, ax=ax[2 + idx], title=title)

    # Check vocab
    top_vocab = get_vocabulary(all_content, 50)
    plot_histogram(
        top_vocab.keys(), top_vocab.values(), ax=ax[-1], title="Days with Rating"
    )

    plt.show()


if __name__ == "__main__":
    main()
