import streamlit as st
import numpy as np
import os
import boto3
import pandas as pd
from io import StringIO

# read AWS credentials from env variables
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
# define AWS methods
CLIENT = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
RESOURCE = boto3.resource("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# South-East (2022) https://www.nimblefins.co.uk/average-cost-electricity-kwh-uk
PRICE_PER_KWH_ELECTRICITY = 0.195
FIXED_RATE_ELECTRICITY = 85.6
# South-East (2019) https://usave.co.uk/energy/average-uk-gas-and-electricity-prices-per-unit/
PRICE_PER_KWH_GAS = 0.0388
FIXED_RATE_GAS = 95.04

WELL_INSULATED = {
    "walls": 0.25,
    "roof": 0.15,
    "windows": 0.8,
    "floor": 0.2
}

POORLY_INSULATED = {
    "walls": 1.5,
    "roof": 1.0,
    "windows": 5.7,
    "floor": 1.0
}

AVG_TEMP = {
    "Jan": 4.8,
    "Feb": 4.8,
    "Mar": 7.1,
    "Apr": 9.1,
    "May": 12.4,
    "Jun": 15.3,
    "Jul": 17.6,
    "Aug": 17.3,
    "Sep": 14.6,
    "Oct": 11.2,
    "Nov": 7.5,
    "Dec": 5.1
}

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

def calculate_energy_for_heating_well_insulated(property_info, temp_gap):

    # compute the energy required to maintain the temperature gap for an hour for each component,
    # based on their relative Thermal Transmittance
    energy_floor = property_info["floor"] * temp_gap * WELL_INSULATED["floor"]
    energy_roof = property_info["roof"] * temp_gap * WELL_INSULATED["roof"]
    energy_windows = property_info["windows"] * temp_gap * WELL_INSULATED["windows"]
    energy_walls = property_info["walls"] * temp_gap * WELL_INSULATED["walls"]
    # add up all components
    total_energy_hour = energy_floor + energy_roof + energy_windows + energy_walls
    # compute energy for the full month
    hours_month = 30 * property_info["hours"]
    total_energy_month = np.round(total_energy_hour * hours_month / 1000, 2)

    return total_energy_month

def calculate_bill(month_consumption, fuel):

    if fuel == "electricity":
        total_bill = round(month_consumption * PRICE_PER_KWH_ELECTRICITY + (FIXED_RATE_ELECTRICITY/12), 2)
    elif fuel == "gas":
        total_bill = round(month_consumption * PRICE_PER_KWH_GAS + (FIXED_RATE_GAS/12), 2)

    return total_bill

st.title("House insulation - Reading")
st.write("Calculate how much you should pay to heat your house")
st.write("Describe your house")

area_walls = st.number_input("What is the total area of external walls?")
area_windows = st.number_input("What is the total area of windows?")
area_floor = st.number_input("What is the area of floor?")
area_roof = st.number_input("What is the area of roof?")
heat_type = st.selectbox("How are you heating your house?", ["electricity", "gas"])
hours_heating = st.selectbox("How many hours a day do you heat your home in average?", np.arange(1, 25, 1))
room_temp = st.number_input("What temperature do you keep at home?")

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
for month, temp in AVG_TEMP.items():
    temp_gap = max(property_info["room_temp"] - temp, 0)
    energy_month_well = calculate_energy_for_heating_well_insulated(property_info, temp_gap)
    year_energy_well += energy_month_well
    month_bill_well = calculate_bill(energy_month_well, property_info["heat_type"])
    year_bill_well += month_bill_well

st.markdown("Your annual energy consumption should be **{energy} kWh**".format(energy=round(year_energy_well, 2)))
st.markdown("Your annual energy bill should be **£ {bill}**".format(bill=round(year_bill_well, 2)))
