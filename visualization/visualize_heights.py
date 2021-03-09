from data import data_loader
from model.temperature import add_temp_columns
from model.hypsometric import add_estimated_height
import pandas as pd
from typing import List
from collections import namedtuple
from matplotlib import pyplot as plt

Line = namedtuple("Line", ["x", "label", "color_arg"])


def plot_estimated_vs_actual_height(site_number: int):
    data = getattr(data_loader, "get_site_" + str(site_number) + "_data")()
    add_temp_columns(data)
    add_estimated_height(data)
    columns = [
        Line("altitude", "From data", "b"),
        Line("estimated_height", "From hypsometric equation", "r"),
    ]
    plot_columns_vs_pressure(data, columns, "Height (m)", "Height Comparison - Site " + str(site_number))
    plot_columns_vs_pressure(data, [Line("height_diff", "Altitude - Estimate", "b")], "Height Diff (m)",
                             "Height Diff - Site " + str(site_number))


def plot_columns_vs_pressure(data: pd.DataFrame, columns: List[Line], x_label, title):
    fig, ax = plt.subplots()
    y = data["pressure"]

    for line in columns:
        ax.plot(data[line.x], y, line.color_arg, label=line.label)

    ax.set_xlabel(x_label)
    ax.set_ylabel("Pressure (hPa)")
    ax.invert_yaxis()
    ax.legend()
    plt.title(title)
    fig.savefig(data_loader.get_project_root() / "figures" / title)
    plt.show()
    plt.close()


if __name__ == "__main__":
    plot_estimated_vs_actual_height(2)