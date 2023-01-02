import numpy as np

from journal_parse.entry import Entry


def get_ratings(entries: list[Entry]) -> list[float]:
    """Gather ratings throughout year."""
    return [entry.rating for entry in entries]


def get_work(entries: list[Entry]) -> list[str]:
    """Get lines involving work and parse for word after word to get idea of which work done."""
    return [
        f"{idx}.{line.split('work ')[-1].split(',')[0]}"
        for idx, entry in enumerate(entries)
        for line in entry.entry.split("\n")
        if "Summary" in line and "work " in line
    ]


def get_vocabulary(all_content: str, count: int) -> dict[str, int]:
    """Get top used words from all content. Strip non char letters for spaces, then get words by split by spaces, get counts of unique words."""

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


def word_counts(words: list[str], all_content: str) -> list[int]:
    """Given list of strings give count of number of mentions."""
    return [all_content.count(word) for word in words]
