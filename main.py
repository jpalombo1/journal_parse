from pathlib import Path

import matplotlib.pyplot as plt  # type: ignore
import numpy as np

from journal_parse.entry import Entry, make_entry
from journal_parse.io import get_all_content, output_journals
from journal_parse.metrics import get_ratings, get_vocabulary, get_work, word_counts
from journal_parse.plotting import plot_histogram
from journal_parse.terms import ACTIVTIES, FEELINGS, NAMES
from journal_parse.validate import check_entries, fix_journals, new_journals

JOURNAL_PATH = Path(__file__).parent / "data" / "journals_2022.txt"
OUTPUT_PATH = Path(__file__).parent / "data" / "journals_2022_new.txt"
NEW_PATH = Path(__file__).parent / "data" / "journal_template.txt"


def main():

    all_content = get_all_content(JOURNAL_PATH)
    entries = [make_entry(entry_text) for entry_text in all_content.split("\n\n")]

    check_entries(entries)
    # Modify journal values as needed
    entries = fix_journals(entries)
    output_journals(entries, OUTPUT_PATH)
    first_entry = Entry(
        idx=1, num=entries[0].num + 1, weekday="Sunday", date="01/01/2023"
    )
    blank_journals = new_journals(first_entry)
    output_journals(blank_journals, NEW_PATH)

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
