import streamlit as st
import numpy as np
import pandas as pd
from Library import calculate_energy_consumption
from Library import calculate_energy_bill
from Library import consts

# import parameters
PARAMS = consts.PARAMS["environment"]

# read file with degree days for Reading
reading_degree_days_2022 = pd.read_csv("EGUB_HDD_15.5C.csv")

st.title("House insulation - Reading")
st.write("Calculate how much you should pay to heat your house")
st.write("Describe your house")

area_walls = st.number_input("What is the total area of external walls? (m²)")
area_windows = st.number_input("What is the total area of windows? (m²)")
area_floor = st.number_input(
    "What is the area of floor? (m²) (Leave 0 if there's another property below yours)"
)
area_roof = st.number_input(
    "What is the area of roof? (m²) (Leave 0 if there's another property above yours)"
)
floors = st.number_input(
    "How many floors are present in your house?", min_value=1, max_value=5
)
heat_type = st.selectbox("How are you heating your house?", ["electricity", "gas"])
hours_day = st.selectbox(
    "How many hours a day do you heat your home in average?", np.arange(1, 25, 1)
)
room_temp = st.number_input(
    "What temperature do you keep at home?", min_value=15, max_value=25
)

property_info = {
    "area_walls": area_walls,
    "area_windows": area_windows,
    "area_floor": area_floor,
    "floors": area_floor,
    "area_roof": area_roof,
    "heat_type": heat_type,
    "walls_height": np.nan,
}

heating_settings = {"hours": hours_day, "temp": room_temp}

year_bill_well = 0
year_energy_well = 0

insulation = "WELL_INSULATED"
# here we calculate the bill daily
for i, row in reading_degree_days_2022.iloc[:365].iterrows():
    temp_gap = (
        heating_settings["temp"]
        - PARAMS["HEAT_GAIN"]
        - PARAMS["DEGREE_DAYS_BASE_TEMP"]
        + row["HDD 15.5"]
    )
    month = row["Date"].split("/")[1]
    energy_day_well = calculate_energy_consumption.main(
        property_info, temp_gap, month, heating_settings["hours"], insulation
    )
    day_bill_well = calculate_energy_bill.main(energy_day_well, heat_type)
    year_bill_well += day_bill_well
    year_energy_well += energy_day_well

# section to show results
submit = st.button("Calculate")
st.write("Click Calculate to see your figures")

if submit:
    st.markdown(
        "Your annual energy consumption due to heating should be **{energy} kWh**".format(
            energy=round(year_energy_well, 2)
        )
    )
    st.markdown(
        "Your annual energy bill (for heating only) should be **£ {bill}**".format(
            bill=round(year_bill_well, 2)
        )
    )
