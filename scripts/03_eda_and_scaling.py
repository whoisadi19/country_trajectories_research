import pandas as pd
import numpy as np
import os 
import matplotlib.pyplot as plt 
import seaborn as sns  


def run_eda_and_scaling():
    df = pd.read_csv('data/processed/wdi_clean_data.csv')

    numeric_cols = [
        'gdp_per_capita', 
        'life_expectancy', 
        'school_enrollment', 
        'co2_per_capita', 
        'renewable_energy_pct'
    ]
    print("\n---Summary Statistics---")
    print(df[numeric_cols].describe().round(2))

    print("\n--- Correlation Matrix ---")
    corr_matrix = df[numeric_cols].corr()
    print(corr_matrix.round(2))


    #figure generation 
    os.makedirs('figures', exist_ok =True)
    sns.set_theme(style='whitegrid')

    #correlation heatmap 
    plt.figure(figsize=(8,6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title("Indicator Correlation Heatmap (1990-2022)", fontsize=14, pad=12)
    plt.tight_layout()
    plt.savefig('figures/01_correlation_heatmap.png', dpi=300)
    plt.close()
    print("   Saved to figures/01_correlation_heatmap.png")

    #scatter plot
    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        data=df,
        x='gdp_per_capita',
        y='co2_per_capita',
        hue='life_expectancy',
        palette='viridis',
        alpha=0.6
    )
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("GDP per Capita (USD, Log Scale)", fontsize=12)
    plt.ylabel("CO2 Emissions per Capita (Metric Tons, Log Scale)", fontsize=12)
    plt.title("Economic Wealth vs. Environmental Pressure (1990-2022)", fontsize=14, pad=12)
    plt.tight_layout()
    plt.savefig('figures/02_gdp_vs_co2_scatter.png', dpi=300)
    plt.close()
    print("   Saved to figures/02_gdp_vs_co2_scatter.png")



    #Standardisation 
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(df[numeric_cols])

    # Create a new DataFrame for the scaled data
    scaled_cols = [f"{col}_scaled" for col in numeric_cols]
    df_scaled = df[['economy', 'Country', 'Year']].copy()
    df_scaled[scaled_cols] = scaled_array

    for col in numeric_cols:
        df_scaled[col] = df[col]
    print("--- Verification of Scaled Features ---")
    print("Means (should be ~0):")
    print(df_scaled[scaled_cols].mean().round(4))
    print("Standard Deviations (should be exactly 1):")
    print(df_scaled[scaled_cols].std().round(4))

    scaled_path = 'data/processed/wdi_scaled_data.csv'
    df_scaled.to_csv(scaled_path, index=False)
    print(f"\nScaled dataset successfully saved to: {scaled_path}")
    print(f"Shape: {df_scaled.shape}")


if __name__ == "__main__":
    run_eda_and_scaling()


