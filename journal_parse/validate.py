from datetime import timedelta

from journal_parse.entry import Entry, get_date_obj, get_date_str
from journal_parse.terms import ACTUAL_WEEKDAYS


def check_entries(entries: list[Entry]):
    """Check if entries/dates increment appropriately.

    For each feature, index entry for it. Make sure each dates 1 day apart and less than previous.
    Make sure weekdays follow cycle calculated by DAY # % 7 starting at Friday since 1st day of year was Friday.
    Also make sure each entry/ index increments by 1.
    """

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
    """Function to automatically fix values that were set wrong.

    Gets old value. For dates just add number of entries days to it from first day.
    For other just add number of entires past. Then modify the entry.

    Args:
        type (str): Type of val in entry to be set (date, num, idx)
        entries (list[Entry]): List of entries

    Returns:
        list[Entry]: Modified list of entries fixed for index/date inaccuracies.
    """
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
    """Wrapper method to fix journals for all types of order errors.

    Set correct vals for date number and index.
    """
    entries = set_vals(type="date", entries=entries)
    entries = set_vals(type="num", entries=entries)
    entries = set_vals(type="idx", entries=entries)

    return entries


def new_journals(first_entry: Entry) -> list[Entry]:
    """Make new journal template by setting first entry based on actual date,index, number, weekday, then make 365 entries like it.

    Call fix method to update index,number, dates correctly.
    """
    entries = [Entry(**first_entry.__dict__) for _ in range(365)]
    return fix_journals(entries)
