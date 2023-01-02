from datetime import timedelta

from journal_parse.entry import Entry, get_date_obj, get_date_str
from journal_parse.terms import ACTUAL_WEEKDAYS


def check_entries(entries: list[Entry]):
    """Check if entries/dates increment appropriately.

    Reverse so entries start at entry 1 and upwards instead of input file start at last entry.
    Check dates, indexes, nums, and weekdays, output any errors.
    """
    rev_entries = entries[::-1]
    check_dates(rev_entries)
    check_idxs(rev_entries)
    check_weekdays(rev_entries)
    check_nums(rev_entries)


def check_dates(entries: list[Entry]) -> None:
    """If actual date of next entry does not equal date of first entry plus number of days since, print error."""
    first_dateobj = get_date_obj(entries[0].date)
    for num_entries, entry in enumerate(entries):
        actual_dateobj = entry.dateobj
        expected_dateobj = first_dateobj + timedelta(days=num_entries)
        if actual_dateobj != expected_dateobj:
            print(
                f"Entry date is {get_date_str(actual_dateobj)} but should be {get_date_str(expected_dateobj)}"
            )


def set_dates(entries: list[Entry]) -> list[Entry]:
    """Gets old value. For dates just add number of entries days to it from first day."""
    new_entries = []
    first_dateobj = get_date_obj(entries[0].date)
    for num_entries, entry in enumerate(entries):
        entry.dateobj = first_dateobj + timedelta(days=num_entries)
        entry.date = get_date_str(entry.dateobj)
        entry.modify_entry()
        new_entries.append(entry)
    return new_entries


def check_nums(entries: list[Entry]) -> None:
    """If actual number entry does not equal num of first entry plus number of days since, print error."""
    first_val = entries[0].num
    for num_entries, entry in enumerate(entries):
        actual_num = entry.num
        expected_num = first_val + num_entries
        if actual_num != expected_num:
            print(f"Entry num is {actual_num} but should be {expected_num}")


def set_nums(entries: list[Entry]) -> list[Entry]:
    """Add number of entries past the first entry number."""
    new_entries = []
    first_val = entries[0].num
    for num_entries, entry in enumerate(entries):
        entry.num = first_val + num_entries
        entry.modify_entry()
        new_entries.append(entry)
    return new_entries


def check_idxs(entries: list[Entry]) -> None:
    """If actual index of next entry does not equal index of first entry plus number of days since, print error."""
    first_val = 1
    for num_entries, entry in enumerate(entries):
        actual_idx = entry.idx
        expected_idx = first_val + num_entries
        if actual_idx != expected_idx:
            print(f"Entry idx is {actual_idx} but should be {expected_idx}")


def set_idxs(entries: list[Entry]) -> list[Entry]:
    """Add number of entries past for first index."""
    new_entries = []
    first_val = 1
    for num_entries, entry in enumerate(entries):
        entry.idx = first_val + num_entries
        entry.modify_entry()
        new_entries.append(entry)
    return new_entries


def check_weekdays(entries: list[Entry]) -> None:
    """If actual weekday of next entry does not equal weekday of first entry plus number of days since, print error.

    Exected weekday found by first getting index of ACTUAL_WEEKDAYS then adding number of days since then modulo 7 (number of weekdays)
    e/g first weekday Friday, index actual_weekdays = 4, num_days since = 4 so weekday is ACTUAL_WEEKDAYS[4+4 % 7]= ACTUAL_WEEKDAYS[1] = Tuesday.
    """
    first_weekday = entries[0].weekday
    first_weekday_idx = ACTUAL_WEEKDAYS.index(first_weekday)
    num_weekdays = len(ACTUAL_WEEKDAYS)
    for num_entries, entry in enumerate(entries):
        curr_weekday_idx = (first_weekday_idx + num_entries) % num_weekdays
        expected_weekday = ACTUAL_WEEKDAYS[curr_weekday_idx]
        actual_weekday = entry.weekday
        if actual_weekday != expected_weekday:
            print(f"Entry weekday is {actual_weekday} but should be {expected_weekday}")


def set_weekdays(entries: list[Entry]) -> list[Entry]:
    """Add number of days past first weekday past for next weekday. Next weekday computed by index into actual weekdays."""
    new_entries = []
    first_weekday = entries[0].weekday
    first_weekday_idx = ACTUAL_WEEKDAYS.index(first_weekday)
    num_weekdays = len(ACTUAL_WEEKDAYS)
    for num_entries, entry in enumerate(entries):
        curr_weekday_idx = (first_weekday_idx + num_entries) % num_weekdays
        entry.weekday = ACTUAL_WEEKDAYS[curr_weekday_idx]
        entry.modify_entry()
        new_entries.append(entry)
    return new_entries


def fix_journals(entries: list[Entry]) -> list[Entry]:
    """Wrapper method to fix journals for all types of order errors.

    Reverse entries to start first entry first, then set correct vals for date number and index.
    """
    rev_entries = entries[::-1]
    rev_entries = set_dates(rev_entries)
    rev_entries = set_nums(rev_entries)
    rev_entries = set_idxs(rev_entries)
    rev_entries = set_weekdays(rev_entries)

    return rev_entries


def new_journals(first_entry: Entry) -> list[Entry]:
    """Make new journal template by setting first entry based on actual date,index, number, weekday, then make 365 entries like it.

    Call fix method to update index,number, dates correctly.
    """
    entries = [
        Entry(
            date=first_entry.date,
            idx=first_entry.idx,
            num=first_entry.num,
            weekday=first_entry.weekday,
        )
        for _ in range(365)
    ]
    return fix_journals(entries)
