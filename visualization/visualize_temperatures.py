import pandas as pd
import matplotlib.pyplot as plt
from collections import namedtuple
from data import data_loader

Line = namedtuple("Line", ["x", "label", "color_arg"])


def plot_temperatures(data_with_temperatures, dataset_name):
    temps = [Line("temp_K", "Temperature", "b"),
             Line("theta", "Potential Temperature", "g"),
             Line("theta_v", "Virtual Potential Temperature", "r")]

    base_temp_plot(data_with_temperatures, temps, dataset_name, "temp_", "Temperatures - ")


def compare_potential_temp_methods(data_with_temperatures, dataset_name):
    temps = [Line("theta", "Potential Temperature", "g"),
             Line("theta_simple", "Simplified Potential Temperature", "y"),
             Line("temp_K", "Temperature", "b")]

    base_temp_plot(data_with_temperatures, temps, dataset_name, "pottemp_", "Potential Temp Method - ")


def plot_potential_temp_diff(data_with_temperatures, dataset_name):
    temps = [Line("theta_difference", "Difference in Potential Temperature", 'b')]

    base_temp_plot(data_with_temperatures, temps, dataset_name, "pottempdiff_", "Difference in Potential Temp - ")


def base_temp_plot(data_with_temperatures, lines, dataset_name, file_prefix, title_prefix):
    fig, ax = plt.subplots()
    y = data_with_temperatures["altitude"]

    for temp in lines:
        ax.plot(data_with_temperatures[temp.x], y, temp.color_arg, label=temp.label)

    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Altitude (m)")
    ax.legend()
    plt.title(title_prefix + dataset_name)
    fig.savefig(data_loader.get_project_root() / "figures" / (file_prefix + dataset_name))
    plt.show()
    plt.close()


def test(number):
    from model import temperature
    data = getattr(data_loader, "get_site_" + str(number) + "_data")()
    temperature.add_temp_columns(data)
    compare_potential_temp_methods(data, "Site " + str(number))


if __name__ == "__main__":
    test(2)