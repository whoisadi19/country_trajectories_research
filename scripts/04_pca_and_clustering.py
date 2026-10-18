import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

def run_ml_pipeline():
    df = pd.read_csv('data/processed/wdi_scaled_data.csv')
    
    scaled_cols = [
        'gdp_per_capita_scaled', 
        'life_expectancy_scaled', 
        'school_enrollment_scaled', 
        'co2_per_capita_scaled', 
        'renewable_energy_pct_scaled'
    ]

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(df[scaled_cols])
    
    df['PC1'] = pca_result[:, 0]
    df['PC2'] = pca_result[:, 1]

    var_pc1 = pca.explained_variance_ratio_[0] * 100
    var_pc2 = pca.explained_variance_ratio_[1] * 100
    total_var = var_pc1 + var_pc2

    print(f"   PC1 explains: {var_pc1:.2f}% of total variance")
    print(f"   PC2 explains: {var_pc2:.2f}% of total variance")
    print(f"   Total 2D Variance Explained: {total_var:.2f}%")

    print("\n--- PCA Feature Loadings (Weights of each indicator) ---")
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=['PC1', 'PC2'],
        index=[c.replace('_scaled', '') for c in scaled_cols]
    )
    print(loadings.round(3))

    from sklearn.cluster import KMeans
    k_range = range(2,8)
    inertias = []

    features_for_clustering = ['PC1', 'PC2']
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(df[features_for_clustering])
        inertias.append(kmeans.inertia_)
        print(f"   K = {k}: Inertia = {kmeans.inertia_:.2f}")

    plt.figure(figsize=(8, 5))
    plt.plot(k_range, inertias, marker='o', linewidth=2, color='#2b5c8f')
    plt.title("K-Means Elbow Method for Optimal Clusters", fontsize=14, pad=12)
    plt.xlabel("Number of Clusters (K)", fontsize=12)
    plt.ylabel("Inertia (Within-Cluster Sum of Squares)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('figures/03_kmeans_elbow.png', dpi=300)
    plt.close()
    print("Saved Elbow curve to figures/03_kmeans_elbow.png")


    #Visualising country development trajectories in PCA
    plt.figure(figsize=(11, 7))
    plt.scatter(
        df['PC1'], 
        df['PC2'], 
        c='lightgray', 
        alpha=0.25, 
        s=15, 
        label='Global Country-Years'
    )
    sample_countries = {
        'IND': ('India', '#e67e22'),       # Orange
        'CHN': ('China', '#e74c3c'),       # Red
        'USA': ('United States', '#2980b9'),# Blue
        'DEU': ('Germany', '#27ae60'),     # Green
        'KEN': ('Kenya', '#8e44ad')        # Purple
    }
    for code, (name, color) in sample_countries.items():
        c_data = df[df['economy'] == code].sort_values('Year')

        plt.plot(c_data['PC1'], c_data['PC2'], color=color, linewidth=2.5, label=name)
        
        # Mark the start year (1990) with an open circle
        start = c_data.iloc[0]
        plt.scatter(start['PC1'], start['PC2'], color=color, s=70, edgecolors='black', zorder=5)
        plt.text(start['PC1'] + 0.1, start['PC2'], '1990', fontsize=9, weight='bold', color=color)
        
        # Mark the latest year (2022) with a solid arrow/dot
        end = c_data.iloc[-1]
        plt.scatter(end['PC1'], end['PC2'], color=color, s=110, edgecolors='black', zorder=5)
        plt.text(end['PC1'] + 0.1, end['PC2'], '2022', fontsize=9, weight='bold', color=color)

    # Conceptual Quadrant Labels
    plt.axvline(0, color='gray', linestyle=':', alpha=0.6)
    plt.axhline(0, color='gray', linestyle=':', alpha=0.6)
    plt.title("Trajectories of Sustainable Development in PCA Space (1990–2022)", fontsize=14, pad=14)
    plt.xlabel("PC1: Socio-Economic Development (Wealth, Health, Education) →", fontsize=12)
    plt.ylabel("PC2: Ecological Pressure (High CO2 Emissions) →", fontsize=12)
    plt.legend(loc='upper left', frameon=True)
    plt.tight_layout()
    trajectory_path = 'figures/04_pca_trajectories.png'
    plt.savefig(trajectory_path, dpi=300)
    plt.close()
    print(f"   Saved trajectory map to: {trajectory_path}")

    final_kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster'] = final_kmeans.fit_predict(df[['PC1', 'PC2']])

    original_cols = ['gdp_per_capita', 'life_expectancy', 'school_enrollment', 'co2_per_capita', 'renewable_energy_pct']
    cluster_profile = df.groupby('Cluster')[original_cols].mean()
    print("\n--- Cluster Profiles (Mean of Indicators) ---")
    print(cluster_profile.round(2))

    plt.figure(figsize=(10, 7))
    palette = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6']
    
    sns.scatterplot(
        data=df, 
        x='PC1', 
        y='PC2', 
        hue='Cluster', 
        palette=palette, 
        alpha=0.6, 
        s=30
    )

    centroids = final_kmeans.cluster_centers_
    plt.scatter(
        centroids[:, 0], 
        centroids[:, 1], 
        marker='X', 
        s=200, 
        c='black', 
        edgecolors='white', 
        linewidth=2, 
        label='Centroids'
    )

    plt.title("The 4 Global Development Archetypes in PCA Space", fontsize=14, pad=12)
    plt.xlabel("PC1: Socio-Economic Development →", fontsize=12)
    plt.ylabel("PC2: Ecological / Carbon Pressure →", fontsize=12)
    plt.legend(title="Cluster Archetype", loc='upper left')
    plt.tight_layout()
    
    cluster_plot_path = 'figures/05_kmeans_clusters.png'
    plt.savefig(cluster_plot_path, dpi=300)
    plt.close()
    print(f"Saved Cluster Map to: {cluster_plot_path}")

    final_output_path = 'data/processed/wdi_clustered_data.csv'
    df.to_csv(final_output_path, index=False)
    print(f"Clustered dataset saved to: {final_output_path}")



if __name__ == "__main__":
    run_ml_pipeline()