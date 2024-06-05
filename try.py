#%%

import pandas as pd
import matplotlib.pyplot as plt

# Sample data
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [28, 35, 42, 31],
        'City': ['New York', 'Paris', 'London', 'Sydney']}

df = pd.DataFrame(data)

# Plotting
plt.bar(df['Name'], df['Age'])
plt.xlabel('Name')
plt.ylabel('Age')
plt.title('Age Distribution')
plt.show()


# %%
