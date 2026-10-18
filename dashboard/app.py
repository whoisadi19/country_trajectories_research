"""
app.py - Global Trajectories of Sustainable Development Dashboard
-----------------------------------------------------------------
A modern, dark-mode-first, minimalist research dashboard investigating 
national pathways of economic growth, human wellbeing, and environmental 
sustainability (1990-2022).
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sustainable Development Trajectories | DEP Research",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- UNIFIED, HIGH-CONTRAST MODERN DARK UI (Single Clean Font, No Neon Gimmicks) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Single Global Font Family */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Clean Container Cards */
    .metric-card {
        background-color: #131b2e;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }

    .metric-val {
        font-size: 1.75rem;
        font-weight: 700;
        color: #f8fafc;
        line-height: 1.2;
    }

    .metric-lbl {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: #94a3b8;
        margin-top: 4px;
    }

    .archetype-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        border-bottom: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 8px;
        font-size: 0.92rem;
        font-weight: 500;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA INGESTION ---
@st.cache_data
def load_data():
    csv_path = 'data/processed/wdi_clustered_data.csv'
    if not os.path.exists(csv_path):
        csv_path = '../data/processed/wdi_clustered_data.csv'
    df = pd.read_csv(csv_path)
    
    # Archetype Labels & High-Contrast Dark-Mode Palette
    cluster_names = {
        1: "Developing & Biomass-Reliant",
        0: "Emerging Transitioners",
        2: "Advanced Decoupled Economies",
        3: "Hyper-Carbon Petrostates"
    }
    cluster_colors = {
        1: "#38bdf8",  # Vibrant Sky Blue
        0: "#fbbf24",  # Amber Gold
        2: "#34d399",  # Emerald Mint
        3: "#f87171"   # Coral Rose
    }
    df['Cluster_Name'] = df['Cluster'].map(cluster_names)
    df['Cluster_Color'] = df['Cluster'].map(cluster_colors)
    return df, cluster_names, cluster_colors

df, cluster_names, cluster_colors = load_data()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown("### 🌍 Research Controls")
    st.caption("Investigating national trajectories of human development, economic growth, and carbon pressure (1990–2022).")
    st.divider()

    all_countries = sorted(df['Country'].unique().tolist())
    default_selected = [c for c in ['India', 'China', 'United States', 'Germany', 'Kenya'] if c in all_countries]

    selected_countries = st.multiselect(
        "Select Trajectory Countries:",
        options=all_countries,
        default=default_selected,
        help="Compare developmental paths over time on the PCA plane."
    )

    year_range = st.slider(
        "Time Range:",
        min_value=int(df['Year'].min()),
        max_value=int(df['Year'].max()),
        value=(1990, 2022),
        step=1
    )

    st.divider()
    st.markdown("#### Cluster Archetypes")
    for cid, name in cluster_names.items():
        color = cluster_colors[cid]
        st.markdown(
            f"<div style='margin-bottom:6px;'><span style='color:{color}; font-size:1.1rem;'>●</span> "
            f"<span style='color:#e2e8f0; font-size:0.86rem; font-weight:500;'>{name}</span></div>",
            unsafe_allow_html=True
        )

    st.divider()
    st.caption("Data: World Bank WDI API | Course: DEP")

filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])].copy()

# --- HEADER SECTION ---
st.markdown("<h2 style='margin-bottom:4px; font-weight:700;'>Trajectories of Sustainable Development</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='color:#94a3b8; font-size:0.95rem; margin-bottom:20px;'>"
    "An empirical investigation into whether nations can achieve economic growth and human flourishing while decoupling from environmental pressure (1990–2022)."
    "</p>",
    unsafe_allow_html=True
)

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-val">193</div>
        <div class="metric-lbl">Sovereign Nations</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-val">33 Years</div>
        <div class="metric-lbl">Longitudinal Scope</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-val">77.95%</div>
        <div class="metric-lbl">PCA Variance Preserved</div>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-val">4 Clusters</div>
        <div class="metric-lbl">Development Archetypes</div>
    </div>
    """, unsafe_allow_html=True)

# --- TABS ---
tab_trajectories, tab_archetypes, tab_indicators, tab_methodology = st.tabs([
    "🗺️ Trajectory Explorer",
    "🏛️ The 4 Development Archetypes",
    "📈 Indicator Time-Series",
    "🔬 Mathematical Foundations"
])

# ==============================================================================
# TAB 1: TRAJECTORY EXPLORER
# ==============================================================================
with tab_trajectories:
    st.markdown("#### 2D PCA Development Landscape (1990–2022)")
    st.caption(
        "Horizontal Axis (PC1) = Socio-Economic Flourishing (Wealth, Education, Longevity). "
        "Vertical Axis (PC2) = Ecological Load (CO2 Emissions per Capita). "
        "Sustainable decoupling corresponds to moving rightward while staying low."
    )

    fig_pca = go.Figure()

    # Background points: subtle, high-contrast dark mode dots
    fig_pca.add_trace(go.Scatter(
        x=filtered_df['PC1'],
        y=filtered_df['PC2'],
        mode='markers',
        marker=dict(
            color=filtered_df['Cluster_Color'],
            size=4,
            opacity=0.3
        ),
        text=filtered_df['Country'] + " (" + filtered_df['Year'].astype(str) + ")",
        hoverinfo='text',
        name='All Countries',
        showlegend=False
    ))

    # Selected country trajectory lines
    line_palette = ['#38bdf8', '#fbbf24', '#34d399', '#f87171', '#c084fc', '#fb923c', '#a3e635']

    for i, country in enumerate(selected_countries):
        c_sub = filtered_df[filtered_df['Country'] == country].sort_values('Year')
        if len(c_sub) == 0:
            continue

        c_color = line_palette[i % len(line_palette)]

        # Trajectory Path Line
        fig_pca.add_trace(go.Scatter(
            x=c_sub['PC1'],
            y=c_sub['PC2'],
            mode='lines',
            line=dict(color=c_color, width=3),
            name=country,
            hoverinfo='skip'
        ))

        # Start Year Marker (1990)
        start_row = c_sub.iloc[0]
        fig_pca.add_trace(go.Scatter(
            x=[start_row['PC1']],
            y=[start_row['PC2']],
            mode='markers+text',
            marker=dict(color=c_color, size=9, symbol='circle', line=dict(color='#0b0f19', width=2)),
            text=[f"{country} '{str(start_row['Year'])[-2:]}"],
            textposition='top center',
            textfont=dict(color='#cbd5e1', size=11, family='Inter'),
            name=f"{country} Start",
            showlegend=False,
            hovertemplate=(
                f"<b>{country} ({start_row['Year']})</b><br>"
                f"GDP/Cap: ${start_row['gdp_per_capita']:,.0f}<br>"
                f"Life Exp: {start_row['life_expectancy']:.1f} yrs<br>"
                f"CO2/Cap: {start_row['co2_per_capita']:.2f} t<br>"
                f"Renewables: {start_row['renewable_energy_pct']:.1f}%<extra></extra>"
            )
        ))

        # End Year Marker (2022)
        end_row = c_sub.iloc[-1]
        fig_pca.add_trace(go.Scatter(
            x=[end_row['PC1']],
            y=[end_row['PC2']],
            mode='markers+text',
            marker=dict(color=c_color, size=13, symbol='diamond', line=dict(color='#ffffff', width=1.5)),
            text=[f"{country} '{str(end_row['Year'])[-2:]}"],
            textposition='bottom center',
            textfont=dict(color='#f8fafc', size=11, family='Inter'),
            name=f"{country} End",
            showlegend=False,
            hovertemplate=(
                f"<b>{country} ({end_row['Year']})</b><br>"
                f"GDP/Cap: ${end_row['gdp_per_capita']:,.0f}<br>"
                f"Life Exp: {end_row['life_expectancy']:.1f} yrs<br>"
                f"CO2/Cap: {end_row['co2_per_capita']:.2f} t<br>"
                f"Renewables: {end_row['renewable_energy_pct']:.1f}%<extra></extra>"
            )
        ))

    # Grid & Reference Crosshairs
    fig_pca.add_vline(x=0, line_dash='dash', line_color='#334155', line_width=1)
    fig_pca.add_hline(y=0, line_dash='dash', line_color='#334155', line_width=1)

    fig_pca.update_layout(
        template="plotly_dark",
        height=580,
        plot_bgcolor='rgba(19, 27, 46, 0.6)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=40, r=40, t=30, b=40),
        xaxis=dict(
            title="<b>PC1: Socio-Economic Development (Wealth, Health, Education) →</b>",
            gridcolor='#1e293b',
            zeroline=False,
            color='#94a3b8'
        ),
        yaxis=dict(
            title="<b>PC2: Ecological Pressure (High Carbon Footprint) →</b>",
            gridcolor='#1e293b',
            zeroline=False,
            color='#94a3b8'
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor='rgba(19, 27, 46, 0.8)',
            bordercolor='#1e293b',
            borderwidth=1,
            font=dict(color='#e2e8f0', size=11)
        )
    )

    st.plotly_chart(fig_pca, use_container_width=True)

    # Key Empirical Insights
    st.markdown("""
    <div class="metric-card">
        <div style="font-weight:600; font-size:0.95rem; color:#f8fafc; margin-bottom:8px;">Key Empirical Observations:</div>
        <div style="font-size:0.87rem; color:#94a3b8; line-height:1.6;">
            • <b>Emerging Giants (India & China):</b> Show massive rightward movement along PC1 (human wellbeing). China ascended higher in PC2 during rapid coal-fired industrialization, whereas India followed a lower-emission trajectory.<br>
            • <b>Decoupled Pioneers (Germany & Western Europe):</b> Demonstrate trajectory curvature downward—expanding economic prosperity while steadily curbing per-capita emissions.<br>
            • <b>Carbon Outliers (Petrostates):</b> Occupy the upper quadrant (PC2 > 7), demonstrating high income through extreme fossil extraction without systemic clean transition.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: THE 4 DEVELOPMENT ARCHETYPES
# ==============================================================================
with tab_archetypes:
    st.markdown("#### Empirical Characteristics of the 4 Archetypes")
    st.caption("Partitioned via K-Means Clustering on the complete 33-year global dataset.")

    summary_cols = ['gdp_per_capita', 'life_expectancy', 'school_enrollment', 'co2_per_capita', 'renewable_energy_pct']
    profile_df = df.groupby('Cluster')[summary_cols].mean()
    profile_df.index = [cluster_names[i] for i in profile_df.index]
    profile_df.columns = [
        "GDP per Capita ($)",
        "Life Expectancy (Yrs)",
        "School Enrollment (%)",
        "CO2 / Capita (Tons)",
        "Renewable Share (%)"
    ]

    col_a, col_b = st.columns([1.3, 1])

    with col_a:
        st.markdown("##### Cluster Indicator Averages")
        st.dataframe(
            profile_df.style.format({
                "GDP per Capita ($)": "${:,.0f}",
                "Life Expectancy (Yrs)": "{:.1f}",
                "School Enrollment (%)": "{:.1f}%",
                "CO2 / Capita (Tons)": "{:.2f}",
                "Renewable Share (%)": "{:.1f}%"
            }),
            use_container_width=True
        )

    with col_b:
        st.markdown("##### Global Distribution (Year: 2022)")
        df_2022 = df[df['Year'] == 2022]
        dist = df_2022['Cluster_Name'].value_counts().reset_index()
        dist.columns = ['Archetype', 'Countries']

        fig_pie = px.pie(
            dist,
            values='Countries',
            names='Archetype',
            color='Archetype',
            color_discrete_map={cluster_names[k]: cluster_colors[k] for k in cluster_names},
            hole=0.6
        )
        fig_pie.update_layout(
            template="plotly_dark",
            margin=dict(l=10, r=10, t=10, b=10),
            height=260,
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            font=dict(color='#cbd5e1')
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    st.divider()

    # 4 Archetype Explanations
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 3px solid {cluster_colors[1]};">
            <div style="color:{cluster_colors[1]}; font-weight:700; font-size:0.95rem;">1. Developing & Biomass-Reliant</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin:4px 0 8px 0;">Income: ~$1,350 | Life Exp: 57.1 yrs | CO2: 0.50 t | Renewables: 72.8%</div>
            <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.5;">
                High apparent "renewable" energy is actually traditional, unimproved biomass (firewood, charcoal) burned for subsistence heating and cooking due to lack of modern power grids.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card" style="border-left: 3px solid {cluster_colors[0]};">
            <div style="color:{cluster_colors[0]}; font-weight:700; font-size:0.95rem;">2. Emerging Transitioners</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin:4px 0 8px 0;">Income: ~$5,440 | Life Exp: 70.4 yrs | CO2: 2.96 t | Renewables: 20.4%</div>
            <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.5;">
                Middle-income economies experiencing accelerating urban industrialization. The core policy imperative is leapfrogging fossil grids to avoid carbon lock-in.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 3px solid {cluster_colors[2]};">
            <div style="color:{cluster_colors[2]}; font-weight:700; font-size:0.95rem;">3. Advanced Decoupled Economies</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin:4px 0 8px 0;">Income: ~$36,600 | Life Exp: 77.9 yrs | CO2: 10.1 t | Renewables: 10.6%</div>
            <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.5;">
                High-income post-industrial societies. Demonstrating relative and absolute decoupling: living standards remain elevated while carbon intensity trends downward.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card" style="border-left: 3px solid {cluster_colors[3]};">
            <div style="color:{cluster_colors[3]}; font-weight:700; font-size:0.95rem;">4. Hyper-Carbon Petrostates</div>
            <div style="font-size:0.8rem; color:#94a3b8; margin:4px 0 8px 0;">Income: ~$35,200 | Life Exp: 71.6 yrs | CO2: 81.1 t | Renewables: 0.13%</div>
            <div style="font-size:0.85rem; color:#cbd5e1; line-height:1.5;">
                Resource-dependent export economies with severe carbon intensity and negligible clean energy deployment (0.13%). Acute embodiment of the resource curse.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 3: INDICATOR TIME-SERIES
# ==============================================================================
with tab_indicators:
    st.markdown("#### Longitudinal Indicator Decomposition")
    
    selected_target = st.selectbox(
        "Choose Country to Inspect:",
        options=all_countries,
        index=all_countries.index("India") if "India" in all_countries else 0
    )

    c_df = df[df['Country'] == selected_target].sort_values('Year')

    col_t1, col_t2 = st.columns(2)

    with col_t1:
        # GDP vs CO2 Dual Axis
        fig_1 = go.Figure()
        fig_1.add_trace(go.Scatter(
            x=c_df['Year'], y=c_df['gdp_per_capita'],
            name="GDP per capita ($)",
            line=dict(color="#38bdf8", width=2.5)
        ))
        fig_1.add_trace(go.Scatter(
            x=c_df['Year'], y=c_df['co2_per_capita'],
            name="CO2 per capita (tons)",
            yaxis="y2",
            line=dict(color="#f87171", width=2.5, dash='dash')
        ))
        fig_1.update_layout(
            template="plotly_dark",
            title=f"Wealth vs. Emissions: {selected_target}",
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(19, 27, 46, 0.5)',
            yaxis=dict(title="GDP / Capita ($)", gridcolor="#1e293b", color="#94a3b8"),
            yaxis2=dict(title="CO2 / Capita (Tons)", overlaying="y", side="right", color="#f87171"),
            legend=dict(orientation="h", y=1.12, x=0.05),
            margin=dict(l=30, r=30, t=40, b=30)
        )
        st.plotly_chart(fig_1, use_container_width=True)

    with col_t2:
        # Life Expectancy vs Renewables
        fig_2 = go.Figure()
        fig_2.add_trace(go.Scatter(
            x=c_df['Year'], y=c_df['life_expectancy'],
            name="Life Expectancy (yrs)",
            line=dict(color="#34d399", width=2.5)
        ))
        fig_2.add_trace(go.Scatter(
            x=c_df['Year'], y=c_df['renewable_energy_pct'],
            name="Renewables (% of total)",
            yaxis="y2",
            line=dict(color="#fbbf24", width=2.5, dash='dot')
        ))
        fig_2.update_layout(
            template="plotly_dark",
            title=f"Health vs. Renewables: {selected_target}",
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(19, 27, 46, 0.5)',
            yaxis=dict(title="Life Expectancy (Years)", gridcolor="#1e293b", color="#94a3b8"),
            yaxis2=dict(title="Renewable Share (%)", overlaying="y", side="right", color="#fbbf24"),
            legend=dict(orientation="h", y=1.12, x=0.05),
            margin=dict(l=30, r=30, t=40, b=30)
        )
        st.plotly_chart(fig_2, use_container_width=True)

    # Decoupling Metric Diagnosis
    start_gdp, end_gdp = c_df.iloc[0]['gdp_per_capita'], c_df.iloc[-1]['gdp_per_capita']
    start_co2, end_co2 = c_df.iloc[0]['co2_per_capita'], c_df.iloc[-1]['co2_per_capita']
    
    pct_gdp = ((end_gdp - start_gdp) / max(1, start_gdp)) * 100
    pct_co2 = ((end_co2 - start_co2) / max(0.01, start_co2)) * 100

    if pct_gdp > 0 and pct_co2 < 0:
        decouple_type = "<span style='color:#34d399; font-weight:700;'>Absolute Decoupling</span> (Economy grew while emissions actively decreased)"
    elif pct_gdp > pct_co2:
        decouple_type = "<span style='color:#fbbf24; font-weight:700;'>Relative Decoupling</span> (Economy grew faster than emissions grew)"
    else:
        decouple_type = "<span style='color:#f87171; font-weight:700;'>Carbon-Coupled Growth</span> (Emissions growth outpaced or matched economic growth)"

    st.markdown(f"""
    <div class="metric-card">
        <div style="font-weight:600; color:#f8fafc; margin-bottom:4px;">Decoupling Assessment for {selected_target} (1990 → 2022):</div>
        <div style="font-size:0.88rem; color:#cbd5e1; line-height:1.6;">
            • GDP per capita change: <b>{pct_gdp:+.1f}%</b> (${start_gdp:,.0f} → ${end_gdp:,.0f})<br>
            • CO2 per capita change: <b>{pct_co2:+.1f}%</b> ({start_co2:.2f} t → {end_co2:.2f} t)<br>
            • Historical Classification: {decouple_type}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: MATHEMATICAL FOUNDATIONS
# ==============================================================================
with tab_methodology:
    st.markdown("#### Mathematical & Algorithmic Foundations")
    
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.markdown("""
        <div class="metric-card">
            <div style="color:#38bdf8; font-weight:700; margin-bottom:8px;">1. Z-Score Feature Standardization</div>
            <p style="font-size:0.85rem; color:#cbd5e1;">Prevents high-magnitude metrics like GDP ($166 to $132,595) from dominating Euclidean distance calculations:</p>
        """, unsafe_allow_html=True)
        st.latex(r"z_i = \frac{x_i - \mu}{\sigma}, \quad \mu = \frac{1}{N}\sum_{i=1}^N x_i, \quad \sigma = \sqrt{\frac{1}{N}\sum_{i=1}^N (x_i - \mu)^2}")
        st.markdown("</div>", unsafe_allow_html=True)

    with m_col2:
        st.markdown("""
        <div class="metric-card">
            <div style="color:#38bdf8; font-weight:700; margin-bottom:8px;">2. Principal Component Analysis (PCA)</div>
            <p style="font-size:0.85rem; color:#cbd5e1;">Eigen-decomposition of the empirical covariance matrix C, preserving 77.95% of total multi-dimensional variance:</p>
        """, unsafe_allow_html=True)
        st.latex(r"\mathbf{C} = \frac{1}{N}\mathbf{X}^T\mathbf{X}, \quad \mathbf{C}\mathbf{v}_k = \lambda_k \mathbf{v}_k")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="metric-card">
        <div style="color:#38bdf8; font-weight:700; margin-bottom:8px;">3. K-Means Cluster Optimization (Lloyd's Algorithm)</div>
        <p style="font-size:0.85rem; color:#cbd5e1;">Minimizing Within-Cluster Sum of Squares (Inertia J) across 6,369 country-year vectors:</p>
    """, unsafe_allow_html=True)
    st.latex(r"J = \sum_{k=1}^{K} \sum_{\mathbf{x}_i \in C_k} \|\mathbf{x}_i - \boldsymbol{\mu}_k\|^2, \quad \boldsymbol{\mu}_k = \frac{1}{|C_k|}\sum_{\mathbf{x}_i \in C_k}\mathbf{x}_i")
    st.markdown("</div>", unsafe_allow_html=True)
