import streamlit as st
import numpy as np
import pandas as pd

WELL_INSULATED = {
    "walls": 0.25,
    "roof": 0.15,
    "windows": 0.8,
    "floor": 0.2,
    "ACH": 0.5
}

POORLY_INSULATED = {
    "walls": 1.5,
    "roof": 1.0,
    "windows": 5.7,
    "floor": 1.0,
    "ACH": 1.3
}
# walls height estimated to be 2.5 m
WALLS_HEIGHT = 2.5
# temperature used as base temperature for degree days
DEGREE_DAYS_BASE_TEMP = 15.5
# heat gain of the building
HEAT_GAIN = 0

def calculate_energy_for_heating_well_insulated(property_info, temp_gap, month, hours_day):

    volume_property = property_info["area_floor"] * property_info["floors"] * WALLS_HEIGHT
    # compute the energy required to maintain the temperature gap for an hour for each component,
    # based on their relative Thermal Transmittance
    energy_floor = property_info["area_floor"] * temp_gap * WELL_INSULATED["floor"]
    energy_roof = property_info["area_roof"]  * temp_gap * WELL_INSULATED["roof"]
    energy_windows = property_info["area_windows"] * temp_gap * WELL_INSULATED["windows"]
    energy_walls = property_info["area_walls"] * temp_gap * WELL_INSULATED["walls"]
    if month in ["06", "07", "08"]:
        # reduce ACH in summer months
        energy_infiltration = 0.005 * WELL_INSULATED["ACH"] * 0.7 * volume_property * temp_gap
    else:
        energy_infiltration = 0.005 * WELL_INSULATED["ACH"] * volume_property * temp_gap

    # add up all components
    total_energy_hour = energy_floor + energy_roof + energy_windows + energy_walls + energy_infiltration
    # compute energy for the full day
    total_energy_day = np.round((total_energy_hour * hours_day) / 1000, 2)

    return total_energy_day
def calculate_energy_for_heating_poorly_insulated(property_info, temp_gap, month, hours_day):

    volume_property = property_info["area_floor"] * property_info["floors"] * WALLS_HEIGHT
    # compute the energy required to maintain the temperature gap for an hour for each component,
    # based on their relative Thermal Transmittance
    energy_floor = property_info["area_floor"] * temp_gap * POORLY_INSULATED["floor"]
    energy_roof = property_info["area_roof"]  * temp_gap * POORLY_INSULATED["roof"]
    energy_windows = property_info["area_windows"] * temp_gap * POORLY_INSULATED["windows"]
    energy_walls = property_info["area_walls"] * temp_gap * POORLY_INSULATED["walls"]
    if month in ["06", "07", "08"]:
        # reduce ACH in summer months
        energy_infiltration = 0.005 * POORLY_INSULATED["ACH"] * 0.7 * volume_property * temp_gap
    else:
        energy_infiltration = 0.005 * POORLY_INSULATED["ACH"] * volume_property * temp_gap

    # add up all components
    total_energy_hour = energy_floor + energy_roof + energy_windows + energy_walls + energy_infiltration
    # compute energy for the full day
    total_energy_day = np.round((total_energy_hour * hours_day) / 1000, 2)

    return total_energy_day

st.title("House insulation - Reading")
st.write("Calculate the energy efficiency of your house")
st.write("Part 1: Describe your house")

area_walls = st.number_input("What is the total area of external walls? (m²)")
area_windows = st.number_input("What is the total area of windows? (m²)")
area_floor = st.number_input("What is the area of floor? (m²) (Leave 0 if there's another property below yours)")
area_roof = st.number_input("What is the area of roof? (m²) (Leave 0 if there's another property above yours)")
floors = st.number_input("How many floors are present in your house?", min_value=1, max_value=5)
hours_heating = st.selectbox("How many hours a day do you heat your home in average?", np.arange(1, 25, 1))
room_temp = st.number_input("What temperature do you keep at home?", min_value=15, max_value=25)

property_info = {
    "area_walls": area_walls,
    "area_windows": area_windows,
    "area_floor": area_floor,
    "area_roof": area_roof,
    "floors": floors
}

heating_settings = {
    "hours": hours_heating,
    "temp": room_temp
}

year_bill_well = 0
year_energy_well = 0

st.write("Part 2: Give us your meter readings (heating only)")
st.write("Start")
reading_start = st.number_input("Insert meter reading (start)")
date_start = st.date_input("Insert meter reading date (start)")

st.write("End")
reading_end = st.number_input("Insert meter reading (end)")
date_end = st.date_input("Insert meter reading date (end)")

meter_readings = {
    "first": {
        "date": str(date_start),
        "reading": reading_start
    },
    "second": {
        "date": str(date_end),
        "reading": reading_end
    }
}

def calculate_efficiency_score(heating_settings, meter_readings, property_info):

    # check that the meter readings are valid
    actual_energy = meter_readings["second"]["reading"] - meter_readings["first"]["reading"]

    if actual_energy < 0:
        st.write("Meter readings not valid")
        return np.nan

    # read file with degree days for Reading
    reading_degree_days_2022 = pd.read_csv("EGUB_HDD_15.5C.csv", parse_dates=["Date"], dayfirst=True)

    st.write(meter_readings["first"]["date"], meter_readings["second"]["date"])
    # select only the dates between the two readings
    df = reading_degree_days_2022[
        (
            (reading_degree_days_2022["Date"].ge(meter_readings["first"]["date"])) &
            (reading_degree_days_2022["Date"].le(meter_readings["second"]["date"]))
        )
    ].copy()

    # check that the selected dates are valid or present in the degree-days
    if df.empty:
        st.write("Dates not available or not valid")
        return np.nan

    total_energy_well = 0
    total_energy_poor = 0

    # here we calculate the bill daily
    for _, row in df.iterrows():
        temp_gap = heating_settings["temp"] - HEAT_GAIN - DEGREE_DAYS_BASE_TEMP + row["HDD 15.5"]
        month = str(row["Date"]).split("-")[1]
        energy_day_well = calculate_energy_for_heating_well_insulated(property_info, temp_gap, month, heating_settings["hours"])
        energy_day_poor = calculate_energy_for_heating_poorly_insulated(property_info, temp_gap, month, heating_settings["hours"])
        total_energy_well += energy_day_well
        total_energy_poor += energy_day_poor

    score = round(100 * (1 - (actual_energy - total_energy_well)/(total_energy_poor - total_energy_well)))

    score = max(min(100, score), 0)

    return score

efficiency = calculate_efficiency_score(property_info=property_info, meter_readings=meter_readings, heating_settings=heating_settings)

st.markdown("Your house efficiency score is **{score}**".format(score=efficiency))
