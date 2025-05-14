import pandas as pd

def clean_religion_data(file_path):

    xls = pd.ExcelFile(file_path)
    

    df_county = pd.read_excel(xls, sheet_name="2020 Group by County")
    df_metro = pd.read_excel(xls, sheet_name="2020 Group by Metro")
    

    for col in ['State Name', 'County Name', 'Metro Name', 'Group Name']:
        if col in df_county.columns:
            df_county[col] = df_county[col].astype(str).str.strip().str.title()
        if col in df_metro.columns:
            df_metro[col] = df_metro[col].astype(str).str.strip().str.title()
    

    df_metro['Metro Name'].fillna('Unknown', inplace=True)
    

    numeric_cols = ['Congregations', 'Adherents', 'Adherents as % of Total Adherents', 'Adherents as % of Total Population']
    for col in numeric_cols:
        if col in df_county.columns:
            df_county[col] = pd.to_numeric(df_county[col], errors='coerce').fillna(0)
        if col in df_metro.columns:
            df_metro[col] = pd.to_numeric(df_metro[col], errors='coerce').fillna(0)
    

    df_county.drop_duplicates(inplace=True)
    df_metro.drop_duplicates(inplace=True)
    

    df_county['Adherents as % of Total Adherents'] /= 100
    df_county['Adherents as % of Total Population'] /= 100
    df_metro['Adherents as % of Total Adherents'] /= 100
    df_metro['Adherents as % of Total Population'] /= 100
    

    df_county.to_csv("cleaned_religion_county.csv", index=False)
    df_metro.to_csv("cleaned_religion_metro.csv", index=False)
    
    print("Data cleaning complete. Cleaned files saved as CSV.")
    return df_county, df_metro

file_path = "William_Duncan_ARISE Asset Map_Religion Census (long).xlsx"
df_county_clean, df_metro_clean = clean_religion_data(file_path)