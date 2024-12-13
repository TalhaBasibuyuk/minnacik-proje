import numpy as np


mean_vector = np.array([20, 0.3, 0.8])
covar_matrix = np.array([
    [4, 0.5, 0.2],
    [0.5, 0.7, 0.2],
    [0.2, 0.2, 0.1]
])


def g(x):
    return 0.1 * x[0]**2 + 12.5 * x[1]**2 - 7.5 * x[2]**2


def population_variance(matrix):
    result = 0
    result += 0.1**2 * matrix[0][0]**2
    result += 12.5**2 * matrix[1][1]**2
    result += 7.5**2 * matrix[2][2]**2
    result += 2.5 * matrix[0][1]**2
    result += 1.5 * matrix[0][2]**2
    result += 187.5 * matrix[1][2]**2
    return result


def monte_carlo_sampling(sample_count, pop_var):
    samples = np.random.multivariate_normal(mean_vector, covar_matrix, sample_count)
    list = []
    for sample in samples:
        list.append(g(sample))
    g_of_samples = np.array(list)
    g_mean = np.mean(g_of_samples)
    half_width = 1.96 * np.sqrt(pop_var/n)
    confidence_interval = (g_mean - half_width, g_mean + half_width)

    return g_mean, confidence_interval


print("Part 2:")

# Experiments with different sample sizes
for n in [50, 100, 1000, 10000]:
    mean, ci = monte_carlo_sampling(n, population_variance(covar_matrix))
    print(f"n = {n} Mean: {mean}  95% CI = {ci}")

print("Part 3:")


def test(std):
    truth_samples = np.random.multivariate_normal(mean_vector, covar_matrix, 10000)
    test_samples = np.random.multivariate_normal(mean_vector, covar_matrix, 50)
    list1 = []
    for sample1 in truth_samples:
        list1.append(g(sample1))
    g_of_samples1 = np.array(list1)
    truth_mean = np.mean(g_of_samples1)
    list2 = []
    for sample2 in test_samples:
        list2.append(g(sample2))
    g_of_samples2 = np.array(list2)
    test_mean = np.mean(g_of_samples2)

    z = (test_mean - truth_mean) / (std - np.sqrt(50))
    print("Truth mean: " + str(truth_mean))
    print("Test mean: " + str(test_mean))
    print("z_value: " + str(z))

    if -1.96 < z < 1.96:
        return "Accept"
    else:
        return "Reject"

print(test(np.sqrt(population_variance(covar_matrix))))