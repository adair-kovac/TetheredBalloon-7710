import pandas as pd
import matplotlib.pyplot as plt
from collections import namedtuple
from data import data_loader


def plot_temperatures(data_with_temperatures, dataset_name):
    fig, ax = plt.subplots()
    y = data_with_temperatures["altitude"]

    Line = namedtuple("Line", ["x", "label", "color_arg"])
    temps = [Line("temp_K", "Temperature", "b"),
             Line("theta", "Potential Temperature", "g"),
             Line("theta_v", "Virtual Potential Temperature", "r")]

    for temp in temps:
        ax.plot(data_with_temperatures[temp.x], y, temp.color_arg, label=temp.label)

    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Altitude (m)")
    ax.legend()
    plt.title("Temperatures - " + dataset_name)
    fig.savefig(data_loader.get_project_root() / "figures" / ("temp_" + dataset_name))
    plt.show()
    plt.close()


def test():
    from model import temperature
    data = data_loader.get_site_2_data()
    temperature.add_temp_columns(data)
    print(data[["RH", "temp", "mixing_ratio"]])
    plot_temperatures(data, "Site 2")


# test()