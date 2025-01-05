import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Parameters for the binomial distribution
n_values = [10, 50]  # Number of trials (n)
p_values = [0.2, 0.5, 0.8]  # Probabilities of success (p)

# Plot the PMF for different combinations of n and p
plt.figure(figsize=(12, 8))
for n in n_values:
    for p in p_values:
        k = np.arange(0, n + 1)  # Possible number of successes (0 to n)
        pmf = binom.pmf(k, n, p)  # Binomial PMF
        plt.plot(k, pmf, marker='o', label=f'n = {n}, p = {p}')

# Customizing the plot
plt.title('PMF of Binomial Distribution', fontsize=14)
plt.xlabel('Number of Successes (k)', fontsize=12)
plt.ylabel('P(X = k)', fontsize=12)
plt.xticks(range(max(n_values) + 1))
plt.grid(alpha=0.4)
plt.legend(title='Parameters', fontsize=10)
plt.tight_layout()

# Display the plot
plt.show()

