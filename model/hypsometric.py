from dataclasses import dataclass
from model.temperature import  R_d, virtual_temperature
import math
import pandas as pd
from typing import List

g = 9.8 # m/s^2


@dataclass
class LayerBoundary:
    pressure: float # hPa
    virtual_temp: float # K


@dataclass
class Layer:
    bottom: LayerBoundary
    top: LayerBoundary


HeightMeters = float


def add_estimated_height(data: pd.DataFrame):
    layers = to_layers(data)
    layer_heights = [get_layer_height(layer) for layer in layers]
    i = 0
    initial_height = data.iloc[0]["altitude"]
    cumulative_height = initial_height
    while i < len(data.index):
        data.at[i, "estimated_height"] = cumulative_height
        if i == len(layer_heights):  # We have to set the last index of data but we won't have another layer to add
            break
        cumulative_height = cumulative_height + layer_heights[i]
        i = i + 1


def get_layer_height(layer: Layer) -> HeightMeters:
    T_v_avg = (layer.bottom.virtual_temp + layer.top.virtual_temp)/2
    z = R_d/g * T_v_avg * math.log(layer.bottom.pressure/layer.top.pressure)
    return z


def to_layers(data: pd.DataFrame) -> List[Layer]:
    layered_data = layer_dataframe(data, ["pressure", "temp_K", "mixing_ratio"])
    layers: List[Layer] = []
    for idx, row in layered_data.iterrows():
        bottom = get_layer_boundary(row, "_b")
        top = get_layer_boundary(row, "_t")
        layers.append(Layer(bottom, top))
    return layers


def get_layer_boundary(row: pd.Series, suffix: str) -> LayerBoundary:
    pressure = row[("pressure" + suffix)]
    temp = row[("temp_K" + suffix)]
    r = row[("mixing_ratio" + suffix)]
    virtual_temp = virtual_temperature(temp, r)
    return LayerBoundary(pressure, virtual_temp)


def layer_dataframe(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    bottoms = data[columns][:-1].reset_index(drop=True)
    tops = data[columns][1:].reset_index(drop=True)
    combined = bottoms.merge(tops, suffixes=["_b", "_t"], left_index=True, right_index=True)
    return combined


def test(number):
    from data import data_loader
    data = getattr(data_loader, "get_site_" + str(number) + "_data")()
    from model.temperature import  add_temp_columns
    add_temp_columns(data)
    add_estimated_height(data)
    print(data)


if __name__ == "__main__":
    test(2)