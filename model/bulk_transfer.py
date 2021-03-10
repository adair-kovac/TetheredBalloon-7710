from model.temperature import R_d, c_pd, L_v
from sklearn.linear_model import LinearRegression
import numpy as np
from dataclasses import dataclass
from model.temperature import  add_temp_columns

C_H = C_W = 1.2e-3 # Estimate of bulk transfer coefficients
reference_height = 20 # m
margin_for_regression = 5 # include values within this many meters when smoothing measurements


@dataclass
class Fluxes:
    sensible: float
    latent: float
    evaporative: float


def get_fluxes(data, debug=False):
    add_temp_columns(data)
    rho = get_average_density(data, reference_height)
    wind_speed = get_reference_value(data, "speed", reference_height)
    surface_temp = get_surface_value(data, "temp")
    reference_temp = get_reference_value(data, "temp", reference_height)
    surface_q = get_surface_value(data, "specific_humidity")
    reference_q = get_reference_value(data, "specific_humidity", reference_height)
    sat_reference_q = get_reference_value(data, "sat_specific_humidity", reference_height)
    evaporative = get_evaporative_flux(rho, wind_speed, surface_q, reference_q, sat_reference_q)
    H_L = L_v * evaporative
    H_S = get_sensible_heat_flux(rho, wind_speed, surface_temp, reference_temp)
    if debug:
        print("\tDebug output:")
        print("\t\trho: " + str(rho))
        print("\t\twindspeed: " + str(wind_speed))
        print("\t\tsurface_temp: " + str(surface_temp))
        print("\t\treference_temp: " + str(reference_temp))
        print("\t\tsurface_q: " + str(surface_q))
        print("\t\treference_q: " + str(reference_q))
        print("\t\tsat_reference_q: " + str(sat_reference_q))
    return Fluxes(H_S, H_L, evaporative)


def get_average_density(data, reference_height):
    reference_height = rebase_reference_height(data, reference_height)
    data = data[data["altitude"] <= reference_height]
    average_rho = data["rho"].sum()/len(data.index)
    return average_rho


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
def get_evaporative_flux(rho, wind_speed, surface_q, reference_q, sat_reference_q):
    drying_power = rho * C_W * wind_speed * (sat_reference_q - reference_q)
    print("Drying power: {:.2E}".format(drying_power))
    return rho * C_W * wind_speed * (surface_q - sat_reference_q) + drying_power


# wind_speed should be at reference height
def get_sensible_heat_flux(rho, wind_speed, surface_temp, reference_temp):
    # technically we could be using c_pv, dependent on humidity, instead of c_pd
    return rho * c_pd * C_H * wind_speed * (surface_temp - reference_temp)


def get_density(P, T_v):
    return P*100/(R_d * T_v)


def test(number):
    from data import data_loader
    data = getattr(data_loader, "get_site_" + str(number) + "_data")()
    print(get_fluxes(data))


if __name__=="__main__":
    test(2)