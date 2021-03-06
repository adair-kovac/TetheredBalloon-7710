import math
import pandas as pd

L_v = 2.5e6 #J/kg
L_d = 2.83e6 #J/kg
R_v = 461 #J/K/kg
R_d = 287 #J/K/kg
c_pd = 1004 #J/K/kg
kappa = R_d/c_pd #unitless
epsilon = 0.622 #kg/kg


def add_temp_columns(data: pd.DataFrame):
    for idx, row in data.iterrows():
        temp_k = as_kelvin(row["temp"])
        theta = potential_temperature(temp_k, row["pressure"])
        r = mixing_ratio_from_observations(row["RH"], row["pressure"], temp_k)
        simplified_theta = simplified_potential_temp(row["altitude"], temp_k)
        e_s = clausius_clapeyron_e_s(temp_k)
        q_s = .622 * e_s/row["pressure"]
        data.at[idx, "temp_K"] = temp_k
        data.at[idx, "theta"] = theta
        data.at[idx, "mixing_ratio"] = r
        data.at[idx, "theta_v"] = virtual_temperature(theta, r)
        data.at[idx, "theta_simple"] = simplified_theta
        data.at[idx, "theta_difference"] = theta - simplified_theta
        data.at[idx, "specific_humidity"] = r/(1 + r)
        data.at[idx, "sat_specific_humidity"] = q_s
        T_v = virtual_temperature(temp_k, r)
        data.at[idx, "virtual_temp"] = T_v
        data.at[idx, "rho"] = 100*row["pressure"]/(R_d * T_v)


def simplified_potential_temp(height, temp):
    Gamma_d = 9.8 * 1/1000 # K/km * km/m = K/m
    return temp + Gamma_d*height


def as_kelvin(temp_in_C):
    return 273.15 + temp_in_C


def virtual_temperature(temp, mixing_ratio):
    return (1 + 1.609*mixing_ratio)/(1 + mixing_ratio) * temp


def potential_temperature(temp, pressure):
    return temp * math.pow(1000 / pressure, kappa)  # K * hPa/hPa^unitless = K


def mixing_ratio_from_observations(relative_humidity, total_pressure, temp):
    e_s = clausius_clapeyron_e_s(temp)
    e = vapor_pressure(e_s, relative_humidity)
    p_d = dry_pressure(e, total_pressure)
    return mixing_ratio(e, p_d)


def vapor_pressure(e_s, RH):
    return RH/100 * e_s # %/% * hPa = hPa


def dry_pressure(e, P_T):
    return P_T - e


def mixing_ratio(e, P_d):
    return epsilon * e/P_d #kg/kg * hPa/hPa = kg/kg


def clausius_clapeyron_e_s(T):
    T_0 = 273.15  # K
    e_0 = 6.113  # hPa
    return e_0 * math.exp(L_v/R_v*(1/T_0 - 1/T)) #hPa * e^(J/kg/(J/kg/K) * 1/K) = hPa * unitless^unitless = hPa

