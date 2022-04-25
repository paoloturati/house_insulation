import streamlit as st
import numpy as np
import pandas as pd
from Library import calculate_energy_consumption
from Library import consts


# import parameters
PARAMS = consts.PARAMS["environment"]

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
    "floors": floors,
    "heat_type": None,
    "walls_height": np.nan
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
        temp_gap = heating_settings["temp"] - PARAMS["HEAT_GAIN"] - PARAMS["DEGREE_DAYS_BASE_TEMP"] + row["HDD 15.5"]
        month = str(row["Date"]).split("-")[1]
        energy_day_well = calculate_energy_consumption.main(property_info, temp_gap, month, heating_settings["hours"],
                                                            "WELL_INSULATED")
        energy_day_poor = calculate_energy_consumption.main(property_info, temp_gap, month, heating_settings["hours"],
                                                            "POORLY_INSULATED")
        total_energy_well += energy_day_well
        total_energy_poor += energy_day_poor

    score = round(100 * (1 - (actual_energy - total_energy_well)/(total_energy_poor - total_energy_well)))

    score = max(min(100, score), 0)

    return score

efficiency = calculate_efficiency_score(property_info=property_info, meter_readings=meter_readings, heating_settings=heating_settings)

# section to show results
submit = st.button("Calculate")
st.write("Click Calculate to see your figures")

if submit:
    st.markdown("Your house efficiency score is **{score}**".format(score=efficiency))
