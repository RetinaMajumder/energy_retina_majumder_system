import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Constants
# -------------------------------
GRAVITY = 9.81
WATER_DENSITY = 1000
HOURS_PER_YEAR = 24*365

# -------------------------------
# Functions
# -------------------------------
def geothermal_thermal_power(m, Cp, delta_T):
    return m * Cp * delta_T

def geothermal_electric_power(Qthermal, eff):
    return Qthermal * eff

def recovered_waste_power(E_input, wasted_fraction, AI_fraction):
    return E_input * wasted_fraction * AI_fraction

def waterfall_power(flow_rate, height, efficiency):
    return WATER_DENSITY * GRAVITY * flow_rate * height * efficiency / 1000  # kW

def annual_energy(power_kw):
    return power_kw * HOURS_PER_YEAR

def households_powered(Eyear, per_house=7200):
    return Eyear / per_house

# Optimization functions
def optimize_waste_fraction(E_input, wasted_fraction, Qthermal, geo_eff):
    """Maximize total electricity by varying AI fraction from 0 to 1."""
    fractions = np.linspace(0, 1, 101)
    best_fraction = 0
    best_total = 0
    for f in fractions:
        Ptotal = geothermal_electric_power(Qthermal, geo_eff) + recovered_waste_power(E_input, wasted_fraction, f)
        if Ptotal > best_total:
            best_total = Ptotal
            best_fraction = f
    return best_fraction, best_total

def optimize_turbine(flow_rate, height):
    """Find optimal turbine efficiency in realistic range 0.6–0.95."""
    efficiencies = np.linspace(0.6, 0.95, 36)
    best_eff = 0.6
    best_power = 0
    for eff in efficiencies:
        P = waterfall_power(flow_rate, height, eff)
        if P > best_power:
            best_power = P
            best_eff = eff
    return best_eff, best_power

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("🌱 Sustainable Electricity Simulator with AI Optimization")

st.header("1️⃣ Geothermal + Waste Recovery")
mass_flow = st.slider("Geothermal Mass Flow (kg/s)", 1, 150, 10)
Cp = st.slider("Specific Heat Cp (kJ/kg·K)", 1.0, 5.0, 4.18)
delta_T = st.slider("Temperature Rise ΔT (K)", 50, 300, 150)
geo_eff = st.slider("Geothermal Efficiency", 0.01, 1.0, 0.12)
E_input = st.number_input("Input Electricity for Waste Recovery (kW)", 1, 1000, 100)
wasted_fraction = st.slider("Fraction of Energy Wasted", 0.0, 1.0, 0.3)
AI_fraction = st.slider("AI Fraction of Waste Intercepted", 0.0, 1.0, 0.7)

Qthermal = geothermal_thermal_power(mass_flow, Cp, delta_T)
Pgeo = geothermal_electric_power(Qthermal, geo_eff)
Pwaste = recovered_waste_power(E_input, wasted_fraction, AI_fraction)
Ptotal_geo = Pgeo + Pwaste
Eyear_geo = annual_energy(Ptotal_geo)
households_geo = households_powered(Eyear_geo)

st.write(f"Current Total Geothermal + Waste Electricity: **{Ptotal_geo:,.2f} kW**")
st.write(f"Annual Energy: **{Eyear_geo:,.0f} kWh**")
st.write(f"Households Powered: **{households_geo:,.0f}**")

# -------------------------------
# 2️⃣ Waterfall Turbine
# -------------------------------
st.header("2️⃣ Mountain-Attached Waterfall Turbine")
flow_rate = st.slider("Water Flow Rate (m³/s)", 0.1, 50.0, 10.0)
height = st.slider("Waterfall Height (m)", 5, 200, 50)
turbine_eff = st.slider("Current Turbine Efficiency", 0.6, 0.95, 0.9)

Pwaterfall = waterfall_power(flow_rate, height, turbine_eff)
Eyear_waterfall = annual_energy(Pwaterfall)
households_waterfall = households_powered(Eyear_waterfall)

st.write(f"Current Waterfall Turbine Power: **{Pwaterfall:,.2f} kW**")
st.write(f"Annual Energy: **{Eyear_waterfall:,.0f} kWh**")
st.write(f"Households Powered: **{households_waterfall:,.0f}**")

# -------------------------------
# AI Optimization
# -------------------------------
st.header("🤖 AI Optimization Suggestions")
if st.button("Run Optimization"):
    opt_AI_fraction, Ptotal_opt_geo = optimize_waste_fraction(E_input, wasted_fraction, Qthermal, geo_eff)
    opt_turb_eff, Pwaterfall_opt = optimize_turbine(flow_rate, height)
    
    Eyear_opt_geo = annual_energy(Ptotal_opt_geo)
    households_opt_geo = households_powered(Eyear_opt_geo)
    
    Eyear_opt_water = annual_energy(Pwaterfall_opt)
    households_opt_water = households_powered(Eyear_opt_water)
    
    st.subheader("Geothermal + Waste Optimization")
    st.write(f"Optimal AI Fraction: **{opt_AI_fraction:.2f}**")
    st.write(f"Optimized Total Geothermal + Waste Power: **{Ptotal_opt_geo:,.2f} kW**")
    st.write(f"Annual Energy: **{Eyear_opt_geo:,.0f} kWh**")
    st.write(f"Households Powered: **{households_opt_geo:,.0f}**")
    
    st.subheader("Waterfall Turbine Optimization")
    st.write(f"Optimal Turbine Efficiency: **{opt_turb_eff:.2f}**")
    st.write(f"Optimized Waterfall Turbine Power: **{Pwaterfall_opt:,.2f} kW**")
    st.write(f"Annual Energy: **{Eyear_opt_water:,.0f} kWh**")
    st.write(f"Households Powered: **{households_opt_water:,.0f}**")
    
    total_current = Ptotal_geo + Pwaterfall
    total_optimized = Ptotal_opt_geo + Pwaterfall_opt
    st.subheader("✅ Combined Summary")
    st.write(f"Current Total Power: {total_current:,.2f} kW")
    st.write(f"Optimized Total Power: {total_optimized:,.2f} kW")
