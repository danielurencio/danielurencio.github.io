from datetime import datetime
import pandas as pd
from itertools import product
from ab_tester import NonParametricTwoTailedTest as Tester

c_size = [2500]
t_size = list(range(1000, 3600, 100))
p_c = [0.05]
effect_size = [0.005, 0.01, 0.015, 0.02]
alpha = [0.05, 0.01]

options = product(*(c_size, t_size, p_c, effect_size, alpha))

start = datetime.now()
results = list()
for option in options:
    c_size_, t_size_, p_c_, effect_size_, alpha_ = option
    e = [Tester(c_size_, t_size_, p_c_, effect_size_, alpha_, 1000)(plot=0) for _ in range(100)]
    power = len([d for d in e if d == True]) / len(e);
    results.append(option + (power,))
    print(option, power)

df = pd.DataFrame(results, columns=['c_size', 't_size', 'p_c', 'efect_size', 'alpha', 'power'])
df.to_csv('results.csv', index=False)
finish = datetime.now()

secs = (finish - start).seconds
print(secs)
