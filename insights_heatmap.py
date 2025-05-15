import arff
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from matplotlib.colors import ListedColormap


# 1. LOAD & DECODE THE RAW DATA

arff_path = r'C:\Users\caleb\OneDrive - Kansas State University\Data Science Project\County\new_grouped_data.arff'
with open(arff_path) as f:
    raw = arff.load(f)

# turn it into a DataFrame, pulling column names from the ARFF header
df = pd.DataFrame(raw['data'], columns=[attr[0] for attr in raw['attributes']])

# fix any byte-strings in State/County/Faith columns
for col in ['State_Name', 'County_Name', 'Faith_Category']:
    if df[col].dtype == object and isinstance(df[col].iloc[0], bytes):
        df[col] = df[col].str.decode('utf-8')

# make sure our key numeric fields are actually numbers
df['Adherents']       = pd.to_numeric(df['Adherents'], errors='coerce')
df['Total_Population']= pd.to_numeric(df['Total_Population'], errors='coerce')


# 2. BUILD THE “PRESENCE” TABLE

# sum adherents by (FIPS, County, Faith)
grouped = (
    df
    .groupby(['FIPS','State_Name','County_Name','Faith_Category'])['Adherents']
    .sum()
    .reset_index()
)

# grab one copy of total population per county
pop = (
    df
    .groupby(['FIPS','State_Name','County_Name'])['Total_Population']
    .first()
    .reset_index()
)

# merge and compute Presence = adherents / total population
merged = pd.merge(grouped, pop, on=['FIPS','State_Name','County_Name'], how='left')
merged['Presence'] = merged['Adherents'] / merged['Total_Population']

# pivot so each county is a row, each faith is a column of presence
presence = (
    merged
    .pivot_table(
        index=['FIPS','State_Name','County_Name'],
        columns='Faith_Category',
        values='Presence',
        fill_value=0
    )
    .reset_index()
)

# 3. PULL IN OTHER COUNTY FEATURES

# list out whatever county-level metrics you care about
features = [
    'Total_Population',
    'Congregations',
    'voter_percentage',
    'winning_percentage',
    'computed_religiosity'
]

# convert them to numeric
for feat in features:
    df[feat] = pd.to_numeric(df[feat], errors='coerce')

# take first/only value per county
county_feats = (
    df
    .groupby(['FIPS','State_Name','County_Name'])[features]
    .first()
    .reset_index()
)

# merge with our presence table
full = pd.merge(presence, county_feats, on=['FIPS','State_Name','County_Name'], how='left')


# 4. COMPUTE R & P-VALUES

faith_cols = [c for c in presence.columns if c not in ['FIPS','State_Name','County_Name']]

# prepare empty tables
corrs = pd.DataFrame(index=features, columns=faith_cols, dtype=float)
pvals = pd.DataFrame(index=features, columns=faith_cols, dtype=float)

# loop through every feature–faith combo
for feat in features:
    for faith in faith_cols:
        # drop NaNs for this pair
        x = full[feat]
        y = full[faith]
        valid = x.notna() & y.notna()
        if valid.sum() < 2:
            corrs.at[feat, faith] = np.nan
            pvals.at[feat, faith] = np.nan
        else:
            r, p = pearsonr(x[valid], y[valid])
            corrs.at[feat, faith] = r
            pvals.at[feat, faith] = p

# 5. PLOT THE ANNOTATED HEATMAP

# mask where p >= 0.05
mask_nonsig = pvals > 0.05

plt.figure(figsize=(12, 6))

# base heatmap of r-values
ax = sns.heatmap(
    corrs,
    annot=False,
    cmap="coolwarm",
    center=0,
    vmin=-0.4,
    vmax=0.6,
    cbar_kws={'label': 'Pearson r'}
)

# overlay black squares for non-significant
sns.heatmap(
    mask_nonsig,
    mask=~mask_nonsig,
    cmap=ListedColormap(['black']),
    cbar=False,
    ax=ax
)

# write r & p into each cell
for i, feat in enumerate(corrs.index):
    for j, faith in enumerate(corrs.columns):
        r = corrs.at[feat, faith]
        p = pvals.at[feat, faith]
        if pd.isna(r) or pd.isna(p):
            continue
        p_text = "<0.01" if p < 0.01 else f"{p:.2f}"
        txt = f"{r:.2f}\n{p_text}"
        color = "white" if mask_nonsig.at[feat, faith] else "black"
        ax.text(j+0.5, i+0.5, txt, ha='center', va='center', color=color, fontsize=8)

# polish labels
ax.set_xticklabels([c.replace('_',' ').title() for c in corrs.columns], rotation=45, ha='right')
ax.set_yticklabels([f.replace('_',' ').title() for f in corrs.index], rotation=0)

plt.title("County Feature vs. Faith Presence Correlations (r over p)")
plt.tight_layout()
plt.show()
