import pandas as pd



file_path = "unclean_county_data.xlsx"  
df = pd.read_excel(file_path)

df["Adherents as % of Total Adherents"] = (
    df["Adherents as % of Total Adherents"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .astype(float)
)
df["Adherents as % of Total Population"] = (
    df["Adherents as % of Total Population"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .astype(float)
)


df["Total Population"] = (df["Adherents"] / df["Adherents as % of Total Population"])
df["Total Adherents"] = (df["Adherents"] / df["Adherents as % of Total Adherents"])


df["Total Population"] = df.groupby("FIPS")["Total Population"].transform("first")
df["Total Adherents"] = df.groupby("FIPS")["Total Adherents"].transform("first")


df.replace("", pd.NA, inplace=True)


output_path = "cleaned_county_data.xlsx"
df.to_excel(output_path, index=False)

print(f"Data cleaning complete. Saved to {output_path}")




nation_file = "group_nation_data.xlsx"
nation_df = pd.read_excel(nation_file)

df = df.merge(nation_df, on="Group Code", how="left")

output_path = "cleaned_county_data.xlsx"
df.to_excel(output_path, index=False)
print(f"Data cleaning complete. Saved to {output_path}")