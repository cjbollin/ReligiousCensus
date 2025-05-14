import pandas as pd
import os

# Define file paths
input_file = r"D:\countypres_2000-2020.csv"
output_folder = r"D:\Filtered_Data"
os.makedirs(output_folder, exist_ok=True)
output_file = os.path.join(output_folder, "county_data_2020.csv")

# Load the dataset
df = pd.read_csv(input_file, dtype=str)  # Read everything as a string initially

# Filter only for the 2020 election data
if 'year' in df.columns:
    df = df[df['year'] == '2020']
else:
    raise KeyError("The dataset does not contain a 'year' column.")

# Standardize column names
df.columns = df.columns.str.strip().str.lower()

# Identify the correct party column
party_col = None
for col in df.columns:
    if "party" in col.lower():
        party_col = col
        break

if party_col is None:
    raise KeyError("No 'Party' column found in the dataset!")

# Define custom encoding for 'Party'
party_mapping = {
    "REPUBLICAN": 0,
    "DEMOCRAT": 1,
    "LIBERTARIAN": 2
}

# Apply encoding, ensuring all values are strings and stripping spaces
df[party_col] = df[party_col].astype(str).map(lambda x: party_mapping.get(x.strip().upper(), 3))  # OTHER = 3

# Save the filtered and processed dataset
df.to_csv(output_file, index=False)

print(f"Filtered 2020 election data saved to: {output_file}")
