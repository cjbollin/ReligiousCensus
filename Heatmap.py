import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\bolli\DataSci\Political Data\Temp.csv")

data = df['Correlation']
labels = df['Feature']

data_reshaped = data.values.reshape(1, -1) 

plt.figure(figsize=(10, 1))
sns.heatmap(data_reshaped, cmap=sns.color_palette("flare_r", as_cmap=True), annot=True, cbar=True, linewidths=0.5, xticklabels=labels)

plt.title(f'One-Dimensional Heatmap for {data.name}')
plt.show()