from model.temperature import R_d, c_pd
from sklearn.linear_model import LinearRegression
import numpy as np
from dataclasses import dataclass
from model.temperature import  add_temp_columns

C_H = C_W = 1.2e-3 # Estimate of bulk transfer coefficients
reference_height = 20 # m
margin_for_regression = 5 # include values within this many meters when smoothing measurements


@dataclass
class HeatFluxes:
    sensible: float
    latent: float


def get_heat_fluxes(data):
    add_temp_columns(data)
    rho = get_average_density(data, reference_height)
    wind_speed = get_reference_value(data, "speed", reference_height)
    surface_temp = get_surface_value(data, "temp")
    reference_temp = get_reference_value(data, "temp", reference_height)
    surface_q = get_surface_value(data, "specific_humidity")
    reference_q = get_reference_value(data, "specific_humidity", reference_height)
    H_L = get_latent_heat_flux(rho, wind_speed, surface_q, reference_q)
    H_S = get_sensible_heat_flux(rho, wind_speed, surface_temp, reference_temp)
    return HeatFluxes(H_S, H_L)


def get_average_density(data, reference_height):
    reference_height = rebase_reference_height(data, reference_height)
    data = data[data["altitude"] <= reference_height]
    average_T_v = data["virtual_temp"].sum()/len(data.index)
    average_pressure = data["pressure"].sum()/len(data.index)
    return get_density(average_pressure, average_T_v)


def get_reference_value(data, value_column, reference_height):
    reference_height = rebase_reference_height(data, reference_height)
    data = data[(reference_height + margin_for_regression
                >= data["altitude"]) & (data["altitude"]
                >= reference_height - margin_for_regression)]
    return get_value(data["altitude"], data[value_column], x=reference_height)


def rebase_reference_height(data, reference_height):
    initial_height = data.iloc[0]["altitude"]
    reference_height = initial_height + reference_height
    return reference_height


def get_surface_value(data, value_column):
    initial_height = data.iloc[0]["altitude"]
    data = data[data["altitude"] <= initial_height + margin_for_regression]
    return get_value(data["altitude"], data[value_column], index=0)


def get_value(data_x, data_y, index=None, x=None):
    # Takes an array with just the values you want to do linear regression on to get a
    # "smoothed" value at the given index or x-value
    reshaped_x = np.array(data_x).reshape((-1, 1))
    model = LinearRegression()
    model.fit(reshaped_x, data_y)
    if index or index == 0:
        return model.predict(reshaped_x)[index]
    else:
        prediction_x = np.array([x]).reshape((1, -1))
        return model.predict(prediction_x)[0]


# wind_speed should be at reference height
def get_latent_heat_flux(rho, wind_speed, surface_q, reference_q):
    print("Drying power: {:.2E}".format(surface_q - reference_q))
    return rho * C_W * wind_speed * (surface_q - reference_q)


# wind_speed should be at reference height
def get_sensible_heat_flux(rho, wind_speed, surface_temp, reference_temp):
    # technically we could be using c_pv, dependent on humidity, instead of c_pd
    return rho * c_pd * C_H * wind_speed * (surface_temp - reference_temp)


def get_density(P, T_v):
    return P*100/(R_d * T_v)


def test(number):
    from data import data_loader
    data = getattr(data_loader, "get_site_" + str(number) + "_data")()
    print(get_heat_fluxes(data))


if __name__=="__main__":
    test(2)