import numpy as np  
import pandas as pd 


# model the gaussian distribution
def gaussian(x, mean, var):
    return (np.power(np.e, -np.power(x - mean, 2) / (2 * var))) / np.sqrt(2 * np.pi*var)

# read the datas from detection_data.csv
data = pd.read_csv("detection_data.csv")

# Classify the data based detection and no detection
detected_data = data[data["Detection"] == "Detect"].drop("Detection", axis=1)
nondetected_data = data[data["Detection"] == "No Detect"].drop("Detection", axis=1)


# Calculate the mean and variance of distance and amplitude for detected cases
detected_means = dict()
detected_vars = dict()
for feature in detected_data.columns:  

    detected_means[feature] = detected_data[feature].mean()
    detected_vars[feature] = detected_data[feature].var()

# Calculate the mean and variance of distance and amplitude for nondetected cases
nondetected_means = dict()
nondetected_vars = dict()
for feature in detected_data.columns: 

    nondetected_means[feature] = nondetected_data[feature].mean()
    nondetected_vars[feature] = nondetected_data[feature].var()

all_means = dict()
all_vars = dict()

for feature in data.drop("Detection", axis=1).columns:  

    all_means[feature] = data[feature].mean()
    all_vars[feature] = data[feature].var()

# Calculates the probability of detection given amplitude,distance
def prob_detect_given_a_d(amplitude, distance):

    step_size = 0.000002
    width = 0.001
    
    # We found the probabilites for amplitude and distance
    # by integrating the prob dist over a very short interval(width) around the given points
    
    # P(a|Detect)
    prob_a_given_detect = 0
    for x in np.arange(amplitude-width, amplitude+width, step_size):
        prob_a_given_detect += gaussian(x, detected_means["Amplitude"], detected_vars["Amplitude"]) * step_size

    # P(d|Detect)
    prob_d_given_detect = 0
    for x in np.arange(distance-width, distance+width, step_size):
        prob_d_given_detect += gaussian(x, detected_means["Distance"], detected_vars["Distance"]) * step_size

    # P(a|Detect)*P(d|Detect)
    prob_a_and_d_given_detect = prob_a_given_detect * prob_d_given_detect
    
    # P(Detect)
    prob_detect = len(detected_data)/len(data)

    # P(a|No Detect)
    prob_a_given_nodetect = 0
    for x in np.arange(amplitude - width, amplitude + width, step_size):
        prob_a_given_nodetect += gaussian(x, nondetected_means["Amplitude"], nondetected_vars["Amplitude"]) * step_size

    # P(d|No Detect)
    prob_d_given_nodetect = 0
    for x in np.arange(distance - width, distance + width, step_size):
        prob_d_given_nodetect += gaussian(x, nondetected_means["Distance"], nondetected_vars["Distance"]) * step_size
        
    prob_a_and_d_given_nodetect = prob_a_given_nodetect * prob_d_given_nodetect
    all_prob = prob_a_and_d_given_detect*prob_detect + prob_a_and_d_given_nodetect*(1-prob_detect)

    return prob_a_and_d_given_detect * prob_detect / all_prob

# Calculates the probability of no detection given amplitude,distance
def prob_nodetect_given_a_d(amplitude, distance):
    step_size = 0.000002
    width = 0.001

    # We found the probabilites for amplitude and distance
    # by integrating the prob dist over a very short interval(width) around the given points

    # P(a|No Detect)
    prob_a_given_nodetect = 0
    for x in np.arange(amplitude-width, amplitude+width, step_size):
        prob_a_given_nodetect += gaussian(x, nondetected_means["Amplitude"], nondetected_vars["Amplitude"]) * step_size
    
    # P(d|No Detect)   
    prob_d_given_nodetect = 0
    for x in np.arange(distance-width, distance+width, step_size):
        prob_d_given_nodetect += gaussian(x, nondetected_means["Distance"], nondetected_vars["Distance"]) * step_size

    # P(a|No Detect)*P(d|No Detect)
    prob_a_and_d_given_nodetect = prob_a_given_nodetect * prob_d_given_nodetect
    
    # P(No Detect)
    prob_nodetect = len(nondetected_data)/len(data)

    # P(a|Detect)
    prob_a_given_detect = 0
    for x in np.arange(amplitude - width, amplitude + width, step_size):
        prob_a_given_detect += gaussian(x, detected_means["Amplitude"], detected_vars["Amplitude"]) * step_size

    # P(d|Detect)
    prob_d_given_detect = 0
    for x in np.arange(distance - width, distance + width, step_size):
        prob_d_given_detect += gaussian(x, detected_means["Distance"], detected_vars["Distance"]) * step_size

    prob_a_and_d_given_detect = prob_a_given_detect * prob_d_given_detect
    all_prob = prob_a_and_d_given_detect * prob_nodetect + prob_a_and_d_given_nodetect * (1 - prob_nodetect)

    return prob_a_and_d_given_nodetect * prob_nodetect / all_prob

# Read the data in extra data file
extra = pd.read_csv("detection_data_extra.csv")

# Print the number of success and failure counts for extra data 
success_count = 0
failure_count = 0
for index, dataling in extra.iterrows():

    det = prob_detect_given_a_d(dataling[1], dataling[0])
    nondet = prob_nodetect_given_a_d(dataling[1], dataling[0])
    if det > nondet:
        if dataling[2] == "Detect": success_count += 1
        else: failure_count += 1
    else:
        if dataling[2] == "No Detect":
            success_count += 1
        else:
            failure_count += 1
print("Success: ", success_count, " Failure: ", failure_count)



