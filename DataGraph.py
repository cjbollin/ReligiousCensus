import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

data = pd.DataFrame({
    'Geographic Level': ['County', 'Metro', 'State', 'National'],
    'Entries': [725932, 319040, 60301, 2232]
})

sns.set(style="whitegrid")

plt.figure(figsize=(8, 6))
barplot = sns.barplot(
    x='Geographic Level',
    y='Entries',
    data=data,
    palette='flare'
)

plt.yscale('log')


plt.title('Entries by Geographic Level (Log Scale)')
plt.xlabel('Geographic Level')
plt.ylabel('Number of Entries (log scale)')

for i, value in enumerate(data['Entries']):
    plt.text(i, value, f"{value:,}", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

