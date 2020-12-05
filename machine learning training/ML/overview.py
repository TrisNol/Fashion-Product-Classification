import pandas as pd 
import matplotlib.pyplot as plt

data = pd.read_csv("./assets/styles.csv", error_bad_lines=False) # multiple lines with errors

# print(data.head)
# for column in data.columns:
#     print("Unique Values for " + column)
#     print(data[column].unique())

names = data['gender'].unique()
values = data.gender.value_counts()
print(values)

plt.figure(figsize=(9, 3))

plt.subplot(131)
plt.bar(names, values)
plt.show()