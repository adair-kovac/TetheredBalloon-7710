from scipy.stats import linregress
from model.temperature import c_pd, L_v, epsilon, add_temp_columns
from model.bulk_transfer import  rebase_reference_height
import matplotlib.pyplot as plt


def estimate_bowen_ratio(data, height=20):
    height = rebase_reference_height(data, height)
    add_temp_columns(data)
    data = data[data["altitude"] <= height]

   # data.plot("altitude", "specific_humidity")
   # plt.savefig("test")
    data.reset_index(drop=True, inplace=True)
    # print(data["specific_humidity"])
    gamma = .0004
    potential_temp_slope = linregress(data["altitude"], data["theta"]).slope
    model_q = linregress(data["altitude"], data["specific_humidity"])
    q_slope = model_q.slope
    potential_temp_slope = potential_temp_slope
    # print("r " + str(model_q.rvalue**2))
    # print(potential_temp_slope)
    # print(q_slope)
    # print("gamma " + str(gamma))
    return gamma * potential_temp_slope/q_slope


def get_psychrometric_constant(pressure): # This is off by orders of magnitude, maybe wrong units?
    return c_pd/L_v * pressure / epsilon


def test(number):
    from data import data_loader
    data = getattr(data_loader, "get_site_" + str(number) + "_data")()
    print(estimate_bowen_ratio(data))


if __name__ == "__main__":
    test(1)