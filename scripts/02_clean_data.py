#I will be standardising Year by stripping YR so it becomes integer
#I'll then remove the regional aggregates like 'World' and 'South Asia'
#then ill inspect and handle missing value using 1)dropna , 2)interpolate/fillna

import pandas as pd 
import numpy as np
import wbgapi as wb

def clean_data():
    
    df = pd.read_csv('data/raw/wdi_raw_data.csv')

    print(f"shape is {df.shape}")
    print(f"Info: {df.info()}")

    #Cleaning Year column by removing YR and convertng it into integer
    df['Year'] = df['Year'].str.replace('YR','').astype(int)
    print(f"year column type after converison: {df['Year'].dtype}")
    print(f"Sample years{df['Year'].head(3).tolist()}")

    #Cleaning Regional Aggregates using WBI Meta data(aggregate == TRUE/FALSE)
    economy_meta = wb.economy.DataFrame()
    real_countries = economy_meta[economy_meta['aggregate'] == False].index.tolist() #use aggregate == True for regions
    before_rows = len(df)
    df = df[df['economy'].isin(real_countries)].copy()
    after_rows =len(df)
    print(f"dropped rows from country list count: {before_rows-after_rows}")
    print(f"Remaining real-country records: {after_rows} rows ({len(df['economy'].unique())} countries)")

    #Handling the missing values 
    #Diagnosis
    print("----Missing Values----")
    missing_count = df.isna().sum()
    missing_pct = (df.isna().sum()/len(df)) *100
    missing_table = pd.DataFrame({
        'Missing Values': missing_count,
        'Percentage (%)': missing_pct.round(2)
    })
    print(missing_table)

    numeric_cols = [
        'gdp_per_capita' ,
        'life_expectancy',
        'school_enrollment',
        'co2_per_capita',
        'renewable_energy_pct'
    ]

    country_missing = df.groupby('Country')[numeric_cols].apply(lambda x: x.isna().mean().mean()*100)

    #10 countries with worst missing values
    worst_countries = country_missing.sort_values(ascending=False).head(10)
    print(f"Top 10 countries with most missing data are: {worst_countries.round(2)}")

    valid_countries = country_missing[country_missing <=30].index.tolist()

    before_count = df['Country'].nunique()
    df = df[df['Country'].isin(valid_countries)].copy()

    after_count = df['Country'].nunique()
    print(f"\nFiltered out countries with >30% missing data: dropped {before_count - after_count} countries.")
    print(f"Remaining countries: {after_count} countries ({len(df)} total rows)")

    #Time series interpolation
    #Sort chronologically before interpolation
    df = df.sort_values(by=['Country', 'Year']).reset_index(drop=True)
    #Apply linear interpolation + edge filling within each country
    print("\n Interpolating missing values per country...")
    df[numeric_cols] = df.groupby('Country')[numeric_cols].transform(
        lambda group: group.interpolate(method='linear').bfill().ffill()
    )
    print("\n--- Missing Values Count After Interpolation ---")
    print(df[numeric_cols].isna().sum())



    #final cleaning 
    #Drop any remaining unresolved missing rows
    df_clean = df.dropna().reset_index(drop=True)
    
    print("\n--- Final Clean Dataset Summary ---")
    print(f"Total Rows: {len(df_clean)}")
    print(f"Total Columns: {df_clean.shape[1]}")
    print(f"Total Countries: {df_clean['Country'].nunique()}")
    print(f"Any remaining missing values? {df_clean.isna().sum().sum()}")

    #Save to data/processed/
    import os
    os.makedirs('data/processed', exist_ok=True)
    clean_path = 'data/processed/wdi_clean_data.csv'
    df_clean.to_csv(clean_path, index=False)
    print(f"Cleaned dataset successfully saved to: {clean_path}")



if __name__ == "__main__" :
    clean_data()

