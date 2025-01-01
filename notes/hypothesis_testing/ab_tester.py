import random
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

class NonParametricTwoTailedTest:
    def __init__(self, n_c, n_t, p_c, effect_size, alpha, n_iter):
        self.n_c = n_c
        self.n_t = n_t
        self.effect_size = effect_size
        self.alpha = alpha
        self.n_iter = n_iter
        self.p_c = p_c
        self.p_t = p_c + effect_size


    def groups_outcomes(self):
        control_negatives = [0 for _ in range(int(self.n_c*(1-self.p_c)))]
        control_positives = [1 for _ in range(int(self.n_c*self.p_c))]
        control = control_negatives + control_positives
    
        treatment_negatives = [0 for _ in range(int(self.n_t*(1-self.p_t)))]
        treatment_positives = [1 for _ in range(int(self.n_t*self.p_t))]
        treatment = treatment_negatives + treatment_positives
    
        control_prop = sum(control)/ len(control)
        treatment_prop = sum(treatment) / len(treatment)
        proportion_difference = treatment_prop - control_prop
    
        return control, treatment, proportion_difference
    
    
    def permutation_test(self, control, treatment):
        pool = control + treatment
        control_size = len(control)
        treatment_size = len(treatment)
        sampling_stats = list()
        extreme_occurrences = 0
        for _ in range(self.n_iter):
            # Randomize!
            pool_ = random.sample(pool, len(pool))#random.shuffle(pool)
            # Select control and treatment groups (with exclusion)
            pseudo_control = pool_[:control_size]
            pseudo_treatment = pool_[control_size:(control_size + treatment_size)]
       
            groups_length = len(pseudo_control) + len(pseudo_treatment)
            if len(pool_) != groups_length:
                raise ValueError('No!! :(')
        
            # Calculate proportions
            pseudo_p_0 = sum(pseudo_control) / len(pseudo_control)
            pseudo_p_a = sum(pseudo_treatment) / len(pseudo_treatment)
            # And save the sampled statistic
            pseudo_stat = pseudo_p_a - pseudo_p_0
            sampling_stats.append(pseudo_stat)
        
            # Is our sampled statistic greater than our experiment observation?
            # NOTE: It is important to convert to absolute values,
            # as this is a two-tailed test
            if abs(pseudo_stat) >= abs(self.effect_size):
                extreme_occurrences += 1
    
        p_value = extreme_occurrences / self.n_iter
        null_rejected = self.alpha >= p_value
        lower_crit = np.quantile(sampling_stats, self.alpha / 2)
        upper_crit = np.quantile(sampling_stats, 1 - (self.alpha / 2))
        results = {'null_rejected': null_rejected,
                   'p_value': p_value,
                   'sampling_stats': sampling_stats,
                   'lower_crit': lower_crit,
                   'upper_crit': upper_crit,
                   'effect_size': self.effect_size}
    
        return results
    
    
    @staticmethod
    def plot_sampling_distribution(bins=20, color='dodgerblue', **kwargs):
        if not len(kwargs.keys()):
            raise ValueError('You need to pass test information')
    
        sampling_stats = kwargs['sampling_stats']
        effect_size = kwargs['effect_size']
        lower_crit = kwargs['lower_crit']
        upper_crit = kwargs['upper_crit']
    
        plt.hist(sampling_stats, bins=20, color='dodgerblue')
        plt.axvline(x=effect_size, color='r')
        plt.axvline(x=lower_crit, ls='--')
        plt.axvline(x=upper_crit, ls='--')
        plt.show()


    def __call__(self, plot=False):
        control, treatment, _ = self.groups_outcomes()
        test_result = self.permutation_test(control, treatment)
        
        if plot:
           self.plot_sampling_distribution(**test_result)

        return test_result['null_rejected']
