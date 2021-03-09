import matplotlib.pyplot as plt
import pandas as pd
from data import data_loader


def plot_dataframe(data: pd.DataFrame, dataset_name=None):
    dataset_name = str(dataset_name or "")

    subplot_rows = 2
    subplot_columns = 3
    fig, axes = plt.subplots(subplot_rows, subplot_columns, sharey=True, figsize=[10, 9])
    title = "Observations " + dataset_name
    fig.suptitle(title)

    initialize_subplots(axes, data, subplot_columns, subplot_rows)

    save_figure(dataset_name, fig)
    plt.show()


def save_figure(dataset_name, fig):
    filename = "plot" + dataset_name
    fig.savefig(data_loader.get_project_root() / "figures" / filename)


def initialize_subplots(axes, data, subplot_columns, subplot_rows):
    vertical_column = data["altitude"]
    vertical_label = "Altitude (m)"
    variables = ["pressure", "temp", "RH", "speed", "direction"]
    var_labels = ["Pressure (mb)", "Temperature (C)", "Relative Humidity (%)", "Wind Speed (m/s)",
                  "Wind Direction (deg)"]

    var_idx = 0
    def out_of_variables(): return var_idx == len(variables)
    for row in range(0, subplot_rows):
        for column in range(0, subplot_columns):
            if out_of_variables():
                break
            kwargs = get_axis_kwargs(var_labels[var_idx], vertical_label, is_first_column=(column == 0))
            add_subplot(axes[row, column], vertical_column, data[variables[var_idx]], **kwargs)
            var_idx = var_idx + 1


def get_axis_kwargs(horizontal_label, vertical_label, is_first_column):
    kwargs = {"horizontal_label": horizontal_label}
    if is_first_column:
        kwargs["vertical_label"] = vertical_label
    return kwargs


def add_subplot(axis, vertical, var, vertical_label=None, horizontal_label=None):
    axis.plot(var, vertical)
    axis.set_xlabel(horizontal_label)
    axis.set_ylabel(vertical_label)


def test_plot():
    plot_dataframe(data_loader.get_site_2_data(), "Site 2")

test_plot()