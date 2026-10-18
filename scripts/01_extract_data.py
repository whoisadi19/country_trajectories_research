import os
import wbgapi as wb
import pandas as pd 
#Indicators I will be tracking 
#format is 'World bank code' : 'my given labels'
INDICATORS = { 
    'NY.GDP.PCAP.KD' : 'gdp_per_capita',
    'SP.DYN.LE00.IN' : 'life_expectancy',
    'SE.SEC.ENRR' : 'school_enrollment',
    'EN.GHG.CO2.PC.CE.AR5' : 'co2_per_capita',
    'EG.FEC.RNEW.ZS' : 'renewable_energy_pct',
}

#I have chosen a time frame of 1990 till 2022 (33 years)
START_YEAR = 1990
END_YEAR = 2022
YEAR_RANGE = range(START_YEAR, END_YEAR+1)

def extract_wdi_data():
    print("connecting to WB API...")
    indicator_dfs = []
    

    for code,col_name in INDICATORS.items():
        print(f"fetching : '{col_name}' ({code})...")
   

        df = wb.data.DataFrame(code, time=YEAR_RANGE, economy= 'all', labels=True)

        df_long =df.reset_index().melt(
            id_vars = ['economy', 'Country'],
            var_name = 'Year',
            value_name = col_name
        )
    
        indicator_dfs.append(df_long)
    
    #merging table of all the 5 indicators
    final_df = indicator_dfs[0]

    for next_df in indicator_dfs[1:]:
        final_df = pd.merge(
            final_df,
            next_df,
            on=['economy', 'Country', 'Year'],
            how='outer'
        )

    #checks
    os.makedirs('data/raw', exist_ok=True)
    
    output_path = 'data/raw/wdi_raw_data.csv'
    final_df.to_csv(output_path, index=False)
    print(f"Raw data saved to {output_path}")
    print(f"Final shape: {final_df.shape[0]} rows, {final_df.shape[1]} columns")

if __name__ == '__main__':
    extract_wdi_data()




 
