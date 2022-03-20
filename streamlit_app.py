import streamlit as st
import numpy as np
import os
import boto3
import pandas as pd
from io import StringIO

# read AWS credentials from env variables
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
bucket_name = os.environ["bucket_name"]

# define AWS methods
CLIENT = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
RESOURCE = boto3.resource("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# South-East (2022) https://www.nimblefins.co.uk/average-cost-electricity-kwh-uk
PRICE_PER_KWH_ELECTRICITY = 0.195
FIXED_RATE_ELECTRICITY = 85.6
# South-East (2019) https://usave.co.uk/energy/average-uk-gas-and-electricity-prices-per-unit/
PRICE_PER_KWH_GAS = 0.0388
FIXED_RATE_GAS = 95.04

# read file with degree days for Reading
reading_degree_days_2022 = pd.read_csv("EGUB_HDD_15.5C.csv")

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
HEAT_GAIN = 4

def write_csv_to_s3(df, filename, bucket_name):

    # writing file on S3 Bucket
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    # write pandas to csv
    RESOURCE.Object(bucket_name, filename).put(Body=csv_buffer.getvalue())

def read_csv_from_s3(filename, bucket_name):

    data = CLIENT.get_object(Bucket=bucket_name, Key=filename)["Body"]
    df = pd.read_csv(data)

    return df

def calculate_energy_for_heating_well_insulated(property_info, temp_gap, month):

    # calculate the area of each components of the external surface
    area_floor = property_info["floor"]
    area_roof = area_floor
    area_windows = property_info["windows"]
    area_walls = property_info["walls"]
    volume_property = area_floor * WALLS_HEIGHT
    # compute the energy required to maintain the temperature gap for an hour for each component,
    # based on their relative Thermal Transmittance
    energy_floor = area_floor * temp_gap * WELL_INSULATED["floor"]
    energy_roof = area_roof * temp_gap * WELL_INSULATED["roof"]
    energy_windows = area_windows * temp_gap * WELL_INSULATED["windows"]
    energy_walls = area_walls * temp_gap * WELL_INSULATED["walls"]
    if month in ["06", "07", "08"]:
        # reduce ACH in summer months
        energy_infiltration = 0.005 * WELL_INSULATED["ACH"] * 0.7 * volume_property * temp_gap
    else:
        energy_infiltration = 0.005 * WELL_INSULATED["ACH"] * volume_property * temp_gap

    # add up all components
    total_energy_hour = energy_floor + energy_roof + energy_windows + energy_walls + energy_infiltration
    # compute energy for the full day
    total_energy_day = np.round((total_energy_hour * property_info["hours"]) / 1000, 2)

    return total_energy_day

def calculate_bill(daily_consumption, fuel):

    if fuel == "electricity":
        total_bill = round(daily_consumption * PRICE_PER_KWH_ELECTRICITY + (FIXED_RATE_ELECTRICITY/365), 2)
    elif fuel == "gas":
        total_bill = round(daily_consumption * PRICE_PER_KWH_GAS + (FIXED_RATE_GAS/365), 2)

    return total_bill


st.title("House insulation - Reading")
st.write("Calculate how much you should pay to heat your house")
st.write("Describe your house")

area_walls = st.number_input("What is the total area of external walls? (m²)")
area_windows = st.number_input("What is the total area of windows? (m²)")
area_floor = st.number_input("What is the area of floor? (m²) (Leave 0 if there's another property below yours)")
area_roof = st.number_input("What is the area of roof? (m²) (Leave 0 if there's another property above yours)")
heat_type = st.selectbox("How are you heating your house?", ["electricity", "gas"])
hours_heating = st.selectbox("How many hours a day do you heat your home in average?", np.arange(1, 25, 1))
room_temp = st.number_input("What temperature do you keep at home?", min_value=15, max_value=25)

property_info = {
    "walls": area_walls,
    "windows": area_windows,
    "floor": area_floor,
    "roof": area_roof,
    "heat_type": heat_type,
    "hours": hours_heating,
    "room_temp": room_temp
}

year_bill_well = 0
year_energy_well = 0

# here we calculate the bill daily
for i, row in reading_degree_days_2022.iloc[:365].iterrows():
    temp_gap = room_temp - HEAT_GAIN - DEGREE_DAYS_BASE_TEMP + row["HDD 15.5"]
    month = row["Date"].split("/")[1]
    energy_day_well = calculate_energy_for_heating_well_insulated(property_info, temp_gap, month)
    day_bill_well = calculate_bill(energy_day_well, heat_type)
    year_bill_well += day_bill_well
    year_energy_well += energy_day_well

st.markdown("Your annual energy consumption due to heating should be **{energy} kWh**".format(energy=round(year_energy_well, 2)))
st.markdown("Your annual energy bill (for heating only) should be **£ {bill}**".format(bill=round(year_bill_well, 2)))
