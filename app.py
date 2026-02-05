import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------
# BASIC CONFIG & STYLE
# ---------------------------
st.set_page_config(
    page_title="Climate Change Dashboard",
    page_icon="🌍",
    layout="wide",
)

plt.style.use("seaborn-v0_8")
sns.set_palette("viridis")


# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("climate_change_dataset.csv")
    return df

df = load_data()

# Precompute some simple stats
years = sorted(df["Year"].unique())
countries = sorted(df["Country"].unique())

min_year = int(min(years))
max_year = int(max(years))


# ---------------------------
# PAGE HEADER
# ---------------------------
st.markdown(
    """
    <h1 style="text-align:center; color:#1f4e79; margin-bottom:0;">
        🌍 Climate Change Insights Dashboard
    </h1>
    <p style="text-align:center; color:#555; font-size:16px; margin-top:4px;">
        Explore temperature, emissions, sea level rise, renewable energy, forests and extreme weather events across countries and years.
    </p>
    <hr style="margin-top:0.5rem; margin-bottom:1rem;">
    """,
    unsafe_allow_html=True,
)


# ---------------------------
# SIDEBAR
# ---------------------------
with st.sidebar:
    st.header("⚙️ Controls")

    selected_year = st.slider(
        "Year (for some charts)",
        min_year,
        max_year,
        value=max_year,
        step=1,
    )

    default_countries = [c for c in ["USA", "China", "India", "Germany", "Brazil"] if c in countries]
    selected_countries = st.multiselect(
        "Countries (multi‑country views)",
        options=countries,
        default=default_countries if default_countries else countries[:4],
    )

    country_single = st.selectbox(
        "Country (detailed view)",
        options=countries,
        index=0,
    )

    st.markdown("---")
    st.markdown(
        """
        **Tips**  
        - Use the year slider to focus on a specific year.  
        - Change the country set to compare different regions.  
        - Use the detailed view to follow one country over time.
        """
    )


# ---------------------------
# TOP METRICS (CARDS)
# ---------------------------
st.markdown("### 🌡️ Key Climate Metrics Snapshot")

df_latest = df[df["Year"] == selected_year]

avg_temp = df_latest["Avg Temperature (°C)"].mean()
avg_sea = df_latest["Sea Level Rise (mm)"].mean()
avg_co2 = df_latest["CO2 Emissions (Tons/Capita)"].mean()
avg_renew = df_latest["Renewable Energy (%)"].mean()

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

col_m1.metric(
    label=f"Avg Temperature (°C) — {selected_year}",
    value=f"{avg_temp:.2f}" if pd.notna(avg_temp) else "N/A",
)

col_m2.metric(
    label=f"Avg Sea Level Rise (mm) — {selected_year}",
    value=f"{avg_sea:.2f}" if pd.notna(avg_sea) else "N/A",
)

col_m3.metric(
    label=f"Avg CO₂ per Capita — {selected_year}",
    value=f"{avg_co2:.2f}" if pd.notna(avg_co2) else "N/A",
)

col_m4.metric(
    label=f"Avg Renewable Energy (%) — {selected_year}",
    value=f"{avg_renew:.1f}%" if pd.notna(avg_renew) else "N/A",
)


# ---------------------------
# SECTION 1: GLOBAL TRENDS
# ---------------------------
st.markdown("---")
st.markdown("## 📈 Global Trends Over Time")

col_g1, col_g2 = st.columns(2)

# Global average temperature over time
q_temp = df.groupby("Year", as_index=False)["Avg Temperature (°C)"].mean()

with col_g1:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=q_temp, x="Year", y="Avg Temperature (°C)", ax=ax1)
    ax1.set_title("Global Average Temperature Over Time")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Avg Temperature (°C)")
    st.pyplot(fig1)

# Global average sea level rise over time
q_sea = df.groupby("Year", as_index=False)["Sea Level Rise (mm)"].mean()

with col_g2:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.lineplot(data=q_sea, x="Year", y="Sea Level Rise (mm)", ax=ax2)
    ax2.set_title("Average Sea Level Rise Over Time")
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Sea Level Rise (mm)")
    st.pyplot(fig2)

st.markdown(
    """
    The global trends suggest increasing **temperature** and **sea level rise** over time, 
    consistent with the expected impacts of ongoing climate change.
    """
)


# ---------------------------
# SECTION 2: COUNTRY COMPARISON
# ---------------------------
st.markdown("---")
st.markdown("## 🌍 Country Comparison: CO₂ and Rainfall")

col_c1, col_c2 = st.columns(2)

# CO2 per capita over time for selected countries
q_co2 = df[df["Country"].isin(selected_countries)].sort_values(["Country", "Year"])

with col_c1:
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.lineplot(
        data=q_co2,
        x="Year",
        y="CO2 Emissions (Tons/Capita)",
        hue="Country",
        ax=ax3,
    )
    ax3.set_title("CO₂ Emissions per Capita Over Time")
    ax3.set_xlabel("Year")
    ax3.set_ylabel("CO₂ Emissions (Tons/Capita)")
    ax3.legend(loc="best")
    st.pyplot(fig3)

# Rainfall distribution by country (boxplot)
with col_c2:
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.boxplot(
        data=df[df["Country"].isin(selected_countries)],
        x="Country",
        y="Rainfall (mm)",
        ax=ax4,
    )
    ax4.set_title("Rainfall Distribution (Selected Countries)")
    ax4.set_xlabel("Country")
    ax4.set_ylabel("Rainfall (mm)")
    ax4.tick_params(axis="x", rotation=45)
    st.pyplot(fig4)

st.markdown(
    """
    Different countries show distinct **CO₂ emission trajectories** and **rainfall patterns**, 
    highlighting how climate and emissions vary across regions.
    """
)


# ---------------------------
# SECTION 3: RELATIONSHIPS
# ---------------------------
st.markdown("---")
st.markdown("## 🔗 Relationships Between Indicators")

col_r1, col_r2 = st.columns(2)

# Renewable Energy vs CO2 (selected year)
df_year = df[df["Year"] == selected_year]

with col_r1:
    fig5, ax5 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=df_year,
        x="Renewable Energy (%)",
        y="CO2 Emissions (Tons/Capita)",
        hue="Country",
        s=80,
        ax=ax5,
    )
    ax5.set_title(f"Renewable Energy vs CO₂ per Capita ({selected_year})")
    ax5.set_xlabel("Renewable Energy (%)")
    ax5.set_ylabel("CO₂ Emissions (Tons/Capita)")
    ax5.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig5)

# CO2 vs Extreme Weather Events (all years)
with col_r2:
    fig6, ax6 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=df,
        x="CO2 Emissions (Tons/Capita)",
        y="Extreme Weather Events",
        hue="Country",
        alpha=0.7,
        ax=ax6,
    )
    ax6.set_title("CO₂ Emissions vs Extreme Weather Events")
    ax6.set_xlabel("CO₂ Emissions (Tons/Capita)")
    ax6.set_ylabel("Extreme Weather Events (count)")
    ax6.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    st.pyplot(fig6)

st.markdown(
    """
    Higher **renewable energy shares** tend to align with lower CO₂ per capita in many cases, 
    while higher CO₂ emissions often coincide with more **extreme weather events** in this dataset.
    """
)


# ---------------------------
# SECTION 4: COUNTRY DETAIL VIEW
# ---------------------------
st.markdown("---")
st.markdown(f"## 🔍 Detailed View: {country_single}")

q_country = df[df["Country"] == country_single].sort_values("Year")

col_d1, col_d2 = st.columns(2)

# Left column: CO2 and Temperature
with col_d1:
    fig7, ax7 = plt.subplots(figsize=(6, 4))
    sns.lineplot(
        data=q_country,
        x="Year",
        y="CO2 Emissions (Tons/Capita)",
        marker="o",
        ax=ax7,
    )
    ax7.set_title(f"{country_single}: CO₂ Emissions per Capita")
    ax7.set_xlabel("Year")
    ax7.set_ylabel("CO₂ Emissions (Tons/Capita)")
    st.pyplot(fig7)

    fig8, ax8 = plt.subplots(figsize=(6, 4))
    sns.lineplot(
        data=q_country,
        x="Year",
        y="Avg Temperature (°C)",
        marker="o",
        color="tomato",
        ax=ax8,
    )
    ax8.set_title(f"{country_single}: Average Temperature")
    ax8.set_xlabel("Year")
    ax8.set_ylabel("Avg Temperature (°C)")
    st.pyplot(fig8)

# Right column: Renewables and Forests
with col_d2:
    fig9, ax9 = plt.subplots(figsize=(6, 4))
    sns.lineplot(
        data=q_country,
        x="Year",
        y="Renewable Energy (%)",
        marker="o",
        color="seagreen",
        ax=ax9,
    )
    ax9.set_title(f"{country_single}: Renewable Energy Share")
    ax9.set_xlabel("Year")
    ax9.set_ylabel("Renewable Energy (%)")
    st.pyplot(fig9)

    fig10, ax10 = plt.subplots(figsize=(6, 4))
    sns.lineplot(
        data=q_country,
        x="Year",
        y="Forest Area (%)",
        marker="o",
        color="saddlebrown",
        ax=ax10,
    )
    ax10.set_title(f"{country_single}: Forest Area Percentage")
    ax10.set_xlabel("Year")
    ax10.set_ylabel("Forest Area (%)")
    st.pyplot(fig10)

st.markdown(
    f"""
    This detailed profile for **{country_single}** shows how emissions, temperature, 
    renewable energy use and forest area have evolved together, giving a compact
    view of its climate and energy trajectory.
    """
)


# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.markdown(
    """
    <p style="text-align:center; color:#777; font-size:13px;">
        Climate Change Dashboard • Built for educational purposes.
    </p>
    """,
    unsafe_allow_html=True,
)
 
