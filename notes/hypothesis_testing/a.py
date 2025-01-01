def groups_outcomes(n1: 'control group size',
                    n2: 'treatment group size',
                    c: 'fraction of positives in control',
                    t: 'fraction of positives in treatment'):
    control_negatives = [0 for _ in range(int(n1*(1-c)))]
    control_positives = [1 for _ in range(int(n1*c))]
    control = control_negatives + control_positives

    treatment_negatives = [0 for _ in range(int(n2*(1-t)))]
    treatment_positives = [1 for _ in range(int(n2*t))]
    treatment = treatment_negatives + treatment_positives
    
    return control, treatment
    

control, treatment = groups_outcomes(2500, 2500, 0.05, 0.07)

p_0 = sum(control) / len(control)
p_a = sum(treatment) / len(treatment)
observed_stat = p_a - p_0
print(f'p_0: {p_0}\np_a: {p_a}\np_a - p_0: {round(observed_stat, 8)}')


import random
import numpy as np
import matplotlib.pyplot as plt

# A priori settings
pool = control + treatment
control_size = 2500
treatment_size = 2500
alpha = 0.05

# Let's sample N times
sampling_stats = list()
extreme_occurrences = 0
for _ in range(2000):
    # Randomize!
    pool_ = random.sample(pool, len(pool))#random.shuffle(pool)
    # Select control and treatment groups (with exclusion)
    pseudo_control = pool_[:control_size]
    pseudo_treatment = pool_[control_size:(control_size + treatment_size)]

    if len(pool_) != len(pseudo_control) + len(pseudo_treatment):
        raise ValueError('No!')

    # Calculate proportions
    pseudo_p_0 = sum(pseudo_control) / len(pseudo_control)
    pseudo_p_a = sum(pseudo_treatment) / len(pseudo_treatment)
    # And save the sampled statistic
    pseudo_stat = pseudo_p_a - pseudo_p_0
    sampling_stats.append(pseudo_stat)

    # Is our sampled statistic greater than our experiment observation?
    # NOTE: It is important to convert to absolute values,
    # as this is a two-tailed test
    if abs(pseudo_stat) >= abs(observed_stat):
        extreme_occurrences += 1

# What are our significant thresholds?
lower_crit = np.quantile(sampling_stats, alpha / 2)
upper_crit = np.quantile(sampling_stats, 1 - (alpha / 2))

# What is our p-value?
p_value = round(extreme_occurrences / len(sampling_stats), 5)
# Is our p-value as extreme as our significance level?
print(f'{p_value} <= {alpha}:', p_value <= alpha)

# Plot
plt.hist(sampling_stats, bins=20, color='dodgerblue')
plt.axvline(x=observed_stat, color='r')
plt.axvline(x=lower_crit, ls='--')
plt.axvline(x=upper_crit, ls='--')
plt.show()
