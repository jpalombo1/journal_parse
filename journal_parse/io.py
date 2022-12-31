from pathlib import Path
from typing import List

from journal_parse.entry import Entry


def get_all_content(input_path: Path) -> str:
    """From journal file, get all content."""
    with open(input_path) as journal_file:
        lines = [str(line) for line in journal_file]
    return "".join(lines)


def output_journals(entries: List[Entry], output: Path) -> None:
    """Reverse entreis so last entry at top, then get all content and write to file."""
    entries.reverse()
    all_content = "\n\n".join([entry.entry for entry in entries])
    with open(output, "w") as new_journal:
        new_journal.write(all_content)
