import pandas as pd

# Create a pandas Series
data = {'A': [1, 2, 3, 4, 5]}
series = pd.DataFrame(data['A'])

# Calculate the mean
mean_value = series.mean()
print(mean_value)
print("Mean value of the Series:", mean_value)
if mean_value > 1:
    print('AMONGUS')