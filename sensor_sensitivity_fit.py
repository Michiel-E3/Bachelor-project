import matplotlib.pyplot as plt
import numpy as np
from lmfit import models

ethanol_x = [50, 100, 300, 700, 950, 2000, 5000]  # ppm
ethanol_y = [3.6, 2, 1.0, 0.6, 0.5, 0.31, 0.18]   # Rs/R0

x = np.linspace(np.min(ethanol_x), np.max(ethanol_x), 100)

def fit_function(x, a, n):
    return a * x**n

model = models.Model(fit_function)

result = model.fit(ethanol_y, x=ethanol_x, weights=10, a=50,n=-1)

a = result.params["a"].value
n = result.params["n"].value

print(result.fit_report())

# plt.plot(ethanol_x, result.init_fit, 'k--', label='initial fit')
plt.plot(x, fit_function(x, a, n), 'r-', label='signaalmodel fit')
plt.scatter(ethanol_x, ethanol_y)

plt.xlabel("Concentration (ppm)")
plt.ylabel("Rs/R0")
plt.title("Ethanol Fit Using lmfit")

plt.legend(loc='best')

plt.show()