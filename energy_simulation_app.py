import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# Constants
# -------------------------------
GRAVITY = 9.81  # m/s^2
WATER_DENSITY = 1000  # kg/m^3
HOURS_PER_YEAR = 24 * 365

# -------------------------------
# Functions
# -------------------------------

# Geothermal + Waste Energy
def geothermal_thermal_power(mass_flow, Cp, delta_T):
    """
    Calculate thermal power (kW) from geothermal source.
    Q = m * Cp * ΔT
    """
    return mass_flow * Cp * delta_T

def geothermal_electric_power(Qthermal, efficiency):
    """Convert thermal power to electric power using turbine efficiency"""
    return Qthermal * efficiency

def recovered_waste_power(E_input, wasted_fraction, AI_fraction):
    """
    Calculate electricity recovered from wasted energy.
    E_recovered = AI_fraction * Wasted_fraction * E_input
    """
    return E_input * wasted_fraction * AI_fraction

# Waterfall Turbine
def waterfall_power(flow_rate, height, efficiency):
    """
    Calculate hydropower output (kW)
    P = ρ * g * Q * H * η
    """
    P_watts = WATER_DENSITY * GRAVITY * flow_rate * height * efficiency
    return P_watts / 1000  # convert to kW

# Annual energy & households
def annual_energy(power_kw):
    return power_kw * HOURS_PER_YEAR

def households_powered(Eyear, consumption_per_household=7200):
    return Eyear / consumption_per_household

# -------------------------------
# Streamlit UI
# -------------------------------

st.title("🌿 Sustainable Electricity Generation Simulator")
st.markdown("""
This app simulates electricity generation from two systems:

1. **Dual-Source Geothermal + Wasted Energy Recovery**
2. **Mountain-Attached Waterfall Turbine**

You can adjust parameters or select **predefined scenarios** to see realistic outputs.
""")

# -------------------------------
# Scenario Presets
# -------------------------------
st.header("⚙️ Scenario Presets (Optional)")
scenario = st.selectbox("Choose a scenario:", 
                        ["Custom", "Scenario A - Small Geothermal", "Scenario B - Large Geothermal"])

# Default values
mass_flow = 10
Cp = 4.18
delta_T = 150
geothermal_eff = 0.12
E_input = 100
wasted_fraction = 0.3
AI_fraction = 0.7
flow_rate = 10
waterfall_height = 50
turbine_eff = 0.9

if scenario == "Scenario A - Small Geothermal":
    mass_flow = 10
    delta_T = 150
    geothermal_eff = 0.12
elif scenario == "Scenario B - Large Geothermal":
    mass_flow = 50
    delta_T = 200
    geothermal_eff = 0.12

# -------------------------------
# User Inputs
# -------------------------------

st.header("1️⃣ Geothermal + Wasted Energy Recovery System")

mass_flow = st.slider("Geothermal Mass Flow (kg/s)", 1, 100, mass_flow, help="Mass of water/steam per second")
Cp = st.slider("Specific Heat Capacity Cp (kJ/kg·K)", 1.0, 5.0, Cp, 0.01, help="Heat capacity of geothermal fluid")
delta_T = st.slider("Temperature Rise ΔT (K)", 50, 300, delta_T, help="Temperature difference between geothermal source and steam generator")
geothermal_eff = st.slider("Geothermal Conversion Efficiency (0-1)", 0.01, 1.0, geothermal_eff)
E_input = st.number_input("Input Electricity for Waste Recovery (kW)", min_value=1, value=E_input)
wasted_fraction = st.slider("Fraction of Energy Wasted (0-1)", 0.0, 1.0, wasted_fraction)
AI_fraction = st.slider("AI-Recovered Fraction of Waste (0-1)", 0.0, 1.0, AI_fraction)

# -------------------------------
# Calculations
# -------------------------------

# Geothermal Calculations
Qthermal = geothermal_thermal_power(mass_flow, Cp, delta_T)
Pgeothermal = geothermal_electric_power(Qthermal, geothermal_eff)
Pwaste = recovered_waste_power(E_input, wasted_fraction, AI_fraction)
Ptotal_geothermal = Pgeothermal + Pwaste
Eyear_geo = annual_energy(Ptotal_geothermal)
households_geo = households_powered(Eyear_geo)

# Waterfall Turbine Inputs
st.header("2️⃣ Mountain-Attached Waterfall Turbine System")
flow_rate = st.slider("Water Flow Rate (m³/s)", 0.1, 50.0, flow_rate)
waterfall_height = st.slider("Waterfall Height (m)", 5, 200, waterfall_height)
turbine_eff = st.slider("Turbine Efficiency (0-1)", 0.1, 1.0, turbine_eff)

# Waterfall Calculations
Pwaterfall = waterfall_power(flow_rate, waterfall_height, turbine_eff)
Eyear_waterfall = annual_energy(Pwaterfall)
households_waterfall = households_powered(Eyear_waterfall)

# -------------------------------
# Combined Output
# -------------------------------
st.header("3️⃣ Combined Total Electricity Generation")
total_power = Ptotal_geothermal + Pwaterfall
total_energy = Eyear_geo + Eyear_waterfall
total_households = households_geo + households_waterfall

st.markdown(f"""
**Total Power Output:** {total_power:,.2f} kW  
**Total Annual Energy:** {total_energy:,.0f} kWh/year  
**Total Households Powered:** {total_households:,.0f} families
""")

# -------------------------------
# Visualization
# -------------------------------
st.header("📊 Electricity Generation by Source")
sources = ['Geothermal + Waste', 'Waterfall Turbine']
values = [Ptotal_geothermal, Pwaterfall]

fig, ax = plt.subplots()
bars = ax.bar(sources, values, color=['#FF8C00', '#1E90FF'])
ax.set_ylabel('Electricity Output (kW)')
ax.set_title('Electricity Generation by Source')
ax.bar_label(bars, fmt='%.0f kW')
st.pyplot(fig)

# -------------------------------
# Detailed Explanation
# -------------------------------
st.header("📝 How This Works")
st.markdown("""
1. **Geothermal + Wasted Energy Recovery**:
   - Computes **thermal energy** from mass flow, heat capacity, and temperature rise.
   - Converts it to **electricity** with turbine efficiency.
   - Adds **AI-recovered electricity** from wasted energy.
2. **Mountain-Attached Waterfall Turbine**:
   - Uses **hydropower formula** P = ρ * g * Q * H * η.
   - Calculates electricity and annual energy.
3. **Combined System**:
   - Total electricity = geothermal + waterfall.
   - Computes **annual energy** and **households powered**.
4. **Visualization**:
   - Shows contribution of each source with a bar chart for easy comparison.
""")
