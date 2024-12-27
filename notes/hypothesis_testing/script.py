import random
import matplotlib.pyplot as plt

class Experiment:
    def __init__(self, p, k, n):
        self.p = p
        self.k = k
        self.n = n

    # One trial can be one coin toss
    def trial(self):
        return 1 if random.random() > self.p else 0

    # We can perform a trial "n" times
    def n_trials(self):
        return sum([self.trial() for _ in range(self.k)])

    def run_experiments(self):
        # Let's say, an experiment is set of trials, and we'll run
        # n experiments, each of which involves k coin tosses.
        # For each experiment, we'll record the number of "heads".
        experiments = []
        for k in range(self.n):
            experiments.append(self.n_trials())

        counts = {e: len([v for v in experiments if e == v])
                  for e in set(experiments)}
                  
        return counts
        

    def __call__(self):
	    counts = self.run_experiments()
        # Get the values, or events, in the X axis,
	    # and the counts, or frequencies, in the Y-axis
	    x = [c for c, h in counts.items()]
	    y = [h for c, h in counts.items()]
	    fig, ax = plt.subplots()
	    ax.bar(x, y)

	    # Remove bounding boxes and save/display image
	    [ax.spines[v].set_visible(False)
	     for v in ('top', 'bottom', 'left', 'right')]
	    plt.savefig(f'trials_n_{self.k}.png', bbox_inches='tight', pad_inches=0)
	    plt.show()
