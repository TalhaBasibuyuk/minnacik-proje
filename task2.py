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
detected_means = dict()
detected_vars = dict()
for feature in detected_data.columns:  # we exclude the "person" column

    detected_means[feature] = detected_data[feature].mean()
    detected_vars[feature] = detected_data[feature].var()

nondetected_means = dict()
nondetected_vars = dict()
for feature in detected_data.columns:  # we exclude the "person" column

    nondetected_means[feature] = nondetected_data[feature].mean()
    nondetected_vars[feature] = nondetected_data[feature].var()

all_means = dict()
all_vars = dict()

for feature in data.drop("Detection", axis=1).columns:  # we exclude the "person" column

    all_means[feature] = data[feature].mean()
    all_vars[feature] = data[feature].var()
"""
print(detected_means["Distance"], detected_vars["Distance"])
print(nondetected_means["Distance"], nondetected_vars["Distance"])
print(all_means["Distance"], all_vars["Distance"])
print(detected_means["Amplitude"], detected_vars["Amplitude"])
print(nondetected_means["Amplitude"], nondetected_vars["Amplitude"])
print(all_means["Amplitude"], all_vars["Amplitude"])
"""



def prob_for_detected_ad(a, d):

    step_size = 0.000002
    wid = 0.001

    detected_amp = 0
    for x in np.arange(a-wid, a+wid, step_size):
        detected_amp += gaussian(x, detected_means["Amplitude"], detected_vars["Amplitude"]) * step_size
    detected_dist = 0
    for x in np.arange(d-wid, d+wid, step_size):
        detected_dist += gaussian(x, detected_means["Distance"], detected_vars["Distance"]) * step_size
    detected_prob = detected_amp * detected_dist

    prob_detection = len(detected_data)/len(data)
    nondetected_amp = 0
    for x in np.arange(a - wid, a + wid, step_size):
        nondetected_amp += gaussian(x, nondetected_means["Amplitude"], nondetected_vars["Amplitude"]) * step_size
    nondetected_dist = 0
    for x in np.arange(d - wid, d + wid, step_size):
        nondetected_dist += gaussian(x, nondetected_means["Distance"], nondetected_vars["Distance"]) * step_size
    nondetected_prob = nondetected_amp * nondetected_dist
    all_prob = detected_prob*prob_detection + nondetected_prob*(1-prob_detection)

    return detected_prob * prob_detection / all_prob


def prob_for_nondetected_ad(a, d):
    step_size = 0.000002
    wid = 0.001

    nondetected_amp = 0
    for x in np.arange(a-wid, a+wid, step_size):
        nondetected_amp += gaussian(x, nondetected_means["Amplitude"], nondetected_vars["Amplitude"]) * step_size
    nondetected_dist = 0
    for x in np.arange(d-wid, d+wid, step_size):
        nondetected_dist += gaussian(x, nondetected_means["Distance"], nondetected_vars["Distance"]) * step_size
    nondetected_prob = nondetected_amp * nondetected_dist


    p_nondetection = len(nondetected_data)/len(data)

    detected_amp = 0
    for x in np.arange(a - wid, a + wid, step_size):
        detected_amp += gaussian(x, detected_means["Amplitude"], detected_vars["Amplitude"]) * step_size
    detected_dist = 0
    for x in np.arange(d - wid, d + wid, step_size):
        detected_dist += gaussian(x, detected_means["Distance"], detected_vars["Distance"]) * step_size
    detected_prob = detected_amp * detected_dist
    all_prob = detected_prob * p_nondetection + nondetected_prob * (1 - p_nondetection)

    return nondetected_prob * p_nondetection / all_prob

extra = pd.read_csv("res/detection_data.csv")


success_count = 0
failure_count = 0
for index, dataling in extra.iterrows():

    det = prob_for_detected_ad(dataling[1], dataling[0])
    nondet = prob_for_nondetected_ad(dataling[1], dataling[0])
    if det > nondet:
        if dataling[2] == "Detect": success_count += 1
        else: failure_count += 1
    else:
        if dataling[2] == "No Detect":
            success_count += 1
        else:
            failure_count += 1
print("Success: ", success_count, " Failure: ", failure_count)


"""
def height_density(height):
    return gaussian(height, all_means["Distance"], all_vars["Distance"])

step_size = 0.01
width = 50
mean = detected_means["Distance"]
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
