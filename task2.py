import numpy as np  # for mathematical operations
import pandas as pd  # to manipulate dataset
import matplotlib.pyplot as plt  # to plot out data


def gaussian(x, mean, var):
    return (np.power(np.e, -np.power(x - mean, 2) / (2 * var))) / np.sqrt(2 * np.pi*var)


data = pd.read_csv("res/detection_data.csv")
#print(data)
detected_data = data[data["Detection"] == "Detect"].drop("Detection", axis=1)
nondetected_data = data[data["Detection"] == "No Detect"].drop("Detection", axis=1)
#print(detected_data)

# calculate mean and variance for each feature and category
d_m = dict()
d_v = dict()
for feature in detected_data.columns:  # we exclude the "person" column

    d_m[feature] = detected_data[feature].mean()
    d_v[feature] = detected_data[feature].var()

nd_m = dict()
nd_v = dict()
for feature in detected_data.columns:  # we exclude the "person" column

    nd_m[feature] = nondetected_data[feature].mean()
    nd_v[feature] = nondetected_data[feature].var()

all_m = dict()
all_v = dict()

for feature in data.drop("Detection", axis=1).columns:  # we exclude the "person" column

    all_m[feature] = data[feature].mean()
    all_v[feature] = data[feature].var()
"""
print(d_m["Distance"], d_v["Distance"])
print(nd_m["Distance"], nd_v["Distance"])
print(all_m["Distance"], all_v["Distance"])
print(d_m["Amplitude"], d_v["Amplitude"])
print(nd_m["Amplitude"], nd_v["Amplitude"])
print(all_m["Amplitude"], all_v["Amplitude"])
"""



def prob_for_detected_ad(a, d):

    step_size = 0.000002
    wid = 0.001

    det_a = 0
    for x in np.arange(a-wid, a+wid, step_size):
        det_a += gaussian(x, d_m["Amplitude"], d_v["Amplitude"]) * step_size
    det_d = 0
    for x in np.arange(d-wid, d+wid, step_size):
        det_d += gaussian(x, d_m["Distance"], d_v["Distance"]) * step_size
    det_prob = det_a * det_d

    p_detection = len(detected_data)/len(data)
    ndet_a = 0
    for x in np.arange(a - wid, a + wid, step_size):
        ndet_a += gaussian(x, nd_m["Amplitude"], nd_v["Amplitude"]) * step_size
    ndet_d = 0
    for x in np.arange(d - wid, d + wid, step_size):
        ndet_d += gaussian(x, nd_m["Distance"], nd_v["Distance"]) * step_size
    ndet_prob = ndet_a * ndet_d
    all_prob = det_prob*p_detection + ndet_prob*(1-p_detection)

    return det_prob * p_detection / all_prob


def prob_for_nondetected_ad(a, d):
    step_size = 0.000002
    wid = 0.001

    ndet_a = 0
    for x in np.arange(a-wid, a+wid, step_size):
        ndet_a += gaussian(x, nd_m["Amplitude"], nd_v["Amplitude"]) * step_size
    ndet_d = 0
    for x in np.arange(d-wid, d+wid, step_size):
        ndet_d += gaussian(x, nd_m["Distance"], nd_v["Distance"]) * step_size
    ndet_prob = ndet_a * ndet_d


    p_nondetection = len(nondetected_data)/len(data)

    det_a = 0
    for x in np.arange(a - wid, a + wid, step_size):
        det_a += gaussian(x, d_m["Amplitude"], d_v["Amplitude"]) * step_size
    det_d = 0
    for x in np.arange(d - wid, d + wid, step_size):
        det_d += gaussian(x, d_m["Distance"], d_v["Distance"]) * step_size
    det_prob = det_a * det_d
    all_prob = det_prob * p_nondetection + ndet_prob * (1 - p_nondetection)

    return ndet_prob * p_nondetection / all_prob

extra = pd.read_csv("res/detection_data.csv")


s_c = 0
f_c = 0
for index, dataling in extra.iterrows():

    det = prob_for_detected_ad(dataling[1], dataling[0])
    nondet = prob_for_nondetected_ad(dataling[1], dataling[0])
    if det > nondet:
        if dataling[2] == "Detect": s_c += 1
        else: f_c += 1
    else:
        if dataling[2] == "No Detect":
            s_c += 1
        else:
            f_c += 1
print("Success: ", s_c, " Failure: ", f_c)


"""
def height_density(height):
    return gaussian(height, all_m["Distance"], all_v["Distance"])

step_size = 0.01
width = 50
mean = d_m["Distance"]
x_values = np.arange(mean-width, mean+width, step_size)
y_values = height_density(x_values)*step_size
plt.figure(figsize=(8, 6))
plt.plot(x_values, y_values)
plt.title("Distribution of Height")
plt.xlabel("height")
plt.ylabel("probability density")
#plt.legend()
plt.show()

area = 0
for x in x_values:
    area+=height_density(x)*step_size
print(area)
"""