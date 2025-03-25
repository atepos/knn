import sys
import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv(sys.argv[1])
results[results['validation_loss'].notnull()]['validation_loss'].plot()
plt.ylim(0, 0.5)
plt.show()
