import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------
# Constants
# -------------------------------
GRAVITY = 9.81  # m/s^2
WATER_DENSITY = 1000  # kg/m^3
HOURS_PER_YEAR = 24 * 365

# -------------------------------
# Functions
# -------------------------------
def geothermal_thermal_power(mass_flow, Cp, delta_T):
    """Compute thermal power from geothermal source (kW)."""
    return mass_flow * Cp * delta_T

def geothermal_electric_power(Qthermal, efficiency):
    """Convert thermal power to electric power using turbine efficiency."""
    return Qthermal * efficiency

def recovered_waste_power(E_input, wasted_fraction, AI_fraction):
    """Compute electricity recovered from wasted energy."""
    return E_input * wasted_fraction * AI_fraction

def waterfall_power(flow_rate, height, efficiency):
    """Compute hydropower output (kW)."""
    P_watts = WATER_DENSITY * GRAVITY * flow_rate * height * efficiency
    return P_watts / 1000  # kW

def annual_energy(power_kw):
    return power_kw * HOURS_PER_YEAR

def households_powered(Eyear, consumption_per_household=7200):
    return Eyear / consumption_per_household

def generate_report_df(Pgeo, Pwaste, Pwaterfall):
    data = {
        "Source": ["Geothermal + Waste", "Waterfall Turbine"],
        "Power Output (kW)": [Pgeo + Pwaste, Pwaterfall]
    }
    df = pd.DataFrame(data)
    df["Annual Energy (kWh)"] = df["Power Output (kW)"] * HOURS_PER_YEAR
    df["Households Powered"] = df["Annual Energy (kWh)"] / 7200
    return df

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Sustainable Electricity Simulator", layout="wide")
st.title("🌱 Sustainable Electricity Generation Simulator")

st.markdown("""
This app simulates electricity generation from **dual-source geothermal + wasted energy recovery** 
and **mountain-attached waterfall turbines**.  
Adjust parameters or use scenario presets to explore different outcomes.
""")

# -------------------------------
# Tabs for better UX
# -------------------------------
tab1, tab2, tab3 = st.tabs(["Geothermal + Waste", "Waterfall Turbine", "Summary & Charts"])

# -------------------------------
# Tab 1: Geothermal + Waste
# -------------------------------
with tab1:
    st.header("1️⃣ Geothermal + Wasted Energy Recovery System")
    
    scenario = st.selectbox("Select Scenario:", 
                            ["Custom", "Small Well", "Large Well", "Extreme High Output"])
    
    # Default values
    mass_flow, Cp, delta_T, geothermal_eff, E_input, wasted_fraction, AI_fraction = 10, 4.18, 150, 0.12, 100, 0.3, 0.7
    
    if scenario == "Small Well":
        mass_flow, delta_T, geothermal_eff = 10, 150, 0.12
    elif scenario == "Large Well":
        mass_flow, delta_T, geothermal_eff = 50, 200, 0.12
    elif scenario == "Extreme High Output":
        mass_flow, delta_T, geothermal_eff = 100, 250, 0.15

    # Inputs
    mass_flow = st.slider("Geothermal Mass Flow (kg/s)", 1, 150, mass_flow)
    Cp = st.slider("Specific Heat Capacity Cp (kJ/kg·K)", 1.0, 5.0, Cp, 0.01)
    delta_T = st.slider("Temperature Rise ΔT (K)", 50, 300, delta_T)
    geothermal_eff = st.slider("Geothermal Conversion Efficiency (0-1)", 0.01, 1.0, geothermal_eff)
    E_input = st.number_input("Input Electricity for Waste Recovery (kW)", 1, 1000, E_input)
    wasted_fraction = st.slider("Fraction of Energy Wasted (0-1)", 0.0, 1.0, wasted_fraction)
    AI_fraction = st.slider("AI Recovered Fraction of Waste (0-1)", 0.0, 1.0, AI_fraction)

    # Calculations
    Qthermal = geothermal_thermal_power(mass_flow, Cp, delta_T)
    Pgeothermal = geothermal_electric_power(Qthermal, geothermal_eff)
    Pwaste = recovered_waste_power(E_input, wasted_fraction, AI_fraction)
    Ptotal_geothermal = Pgeothermal + Pwaste
    Eyear_geo = annual_energy(Ptotal_geothermal)
    households_geo = households_powered(Eyear_geo)

    st.markdown(f"**Thermal Power:** {Qthermal:,.2f} kW")
    st.markdown(f"**Electricity from Geothermal:** {Pgeothermal:,.2f} kW")
    st.markdown(f"**Recovered Waste Electricity:** {Pwaste:,.2f} kW")
    st.markdown(f"**Total Geothermal + Waste Electricity:** {Ptotal_geothermal:,.2f} kW")
    st.markdown(f"**Annual Energy:** {Eyear_geo:,.0f} kWh/year")
    st.markdown(f"**Households Powered:** {households_geo:,.0f} families")

# -------------------------------
# Tab 2: Waterfall Turbine
# -------------------------------
with tab2:
    st.header("2️⃣ Mountain-Attached Waterfall Turbine System")
    
    flow_rate = st.slider("Water Flow Rate (m³/s)", 0.1, 50.0, 10.0)
    waterfall_height = st.slider("Waterfall Height (m)", 5, 200, 50)
    turbine_eff = st.slider("Turbine Efficiency (0-1)", 0.1, 1.0, 0.9)

    Pwaterfall = waterfall_power(flow_rate, waterfall_height, turbine_eff)
    Eyear_waterfall = annual_energy(Pwaterfall)
    households_waterfall = households_powered(Eyear_waterfall)

    st.markdown(f"**Electricity Generated:** {Pwaterfall:,.2f} kW")
    st.markdown(f"**Annual Energy:** {Eyear_waterfall:,.0f} kWh/year")
    st.markdown(f"**Households Powered:** {households_waterfall:,.0f} families")

# -------------------------------
# Tab 3: Summary & Charts
# -------------------------------
with tab3:
    st.header("3️⃣ Combined Output & Visualization")

    total_power = Ptotal_geothermal + Pwaterfall
    total_energy = Eyear_geo + Eyear_waterfall
    total_households = households_geo + households_waterfall

    st.markdown(f"**Total Power Output:** {total_power:,.2f} kW")
    st.markdown(f"**Total Annual Energy:** {total_energy:,.0f} kWh/year")
    st.markdown(f"**Total Households Powered:** {total_households:,.0f} families")

    # Bar Chart
    df = generate_report_df(Pgeothermal, Pwaste, Pwaterfall)
    st.bar_chart(df.set_index("Source")["Power Output (kW)"])

    # Download CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Report as CSV", csv, "energy_report.csv", "text/csv")

    # Optional: Add Prototype/Diagram link
    prototype_url = st.text_input("Add link to virtual prototype / diagrams (Google Drive or GitHub)", "")
    if prototype_url:
        st.markdown(f"[Click here to view prototype/diagrams]({prototype_url})", unsafe_allow_html=True)

st.success("💡 Simulation complete! Adjust parameters to explore different scenarios.")
