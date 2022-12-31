from typing import Any


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
