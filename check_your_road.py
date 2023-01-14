import streamlit as st
import pandas as pd

# read file with Reading streets
reading_streets_mapping = pd.read_csv("Mapping_Reading_housing_stock.csv")

st.title("Check Your Street - Reading")
st.write("See the average energy efficiency and insulation of houses in Reading streets")

street_list = [""] + list(reading_streets_mapping["road"])
# get street name from user
street_name = st.selectbox("Type your street name", street_list)

# select relevant street
df = reading_streets_mapping[reading_streets_mapping["road"]==street_name].copy()

if df.empty:
    st.write("No street selected")
else:
    num_properties = df["num_properties"].iloc[0]
    perc_insulated_roof = df["insulated_roof"].iloc[0]
    perc_insulated_walls = df["insulated_walls"].iloc[0]
    perc_insulated_windows = df["insulated_windows"].iloc[0]
    perc_insulated_floor = df["insulated_floor"].iloc[0]
    avg_CO2_emissions = df["avg_CO2_emissions"].iloc[0]
    avg_energy_consumption = df["avg_energy_consumption"].iloc[0]
    avg_energy_efficiency = df["avg_energy_efficiency"].iloc[0]
    perc_good_rating = df["good_rating"].iloc[0]
    # print number of properties
    st.markdown(
        "Number of properties on {street_name}: **{num_properties}**".format(
            street_name=street_name,
            num_properties=num_properties
        )
    )
    # print percentage of properties with insulated roof
    st.markdown(
        "Percentage of properties on {street_name} with ROOF insulation: **{perc_insulated_roof}**".format(
            street_name=street_name,
            perc_insulated_roof=perc_insulated_roof
        )
    )
    # print percentage of properties with insulated walls
    st.markdown(
        "Percentage of properties on {street_name} with WALLS insulation: **{perc_insulated_walls}**".format(
            street_name=street_name,
            perc_insulated_walls=perc_insulated_walls
        )
    )
    # print percentage of properties with insulated windows
    st.markdown(
        "Percentage of properties on {street_name} with WINDOWS insulation: **{perc_insulated_windows}**".format(
            street_name=street_name,
            perc_insulated_windows=perc_insulated_windows
        )
    )
    # print percentage of properties with insulated floor
    st.markdown(
        "Percentage of properties on {street_name} with FLOOR insulation: **{perc_insulated_floor}**".format(
            street_name=street_name,
            perc_insulated_floor=perc_insulated_floor
        )
    )
    # print average energy consumption
    st.markdown(
        "Average energy consumption of properties on {street_name}: **{avg_energy_consumption}** (kWh/m²/year)".format(
            street_name=street_name,
            avg_energy_consumption=avg_energy_consumption
        )
    )
    # print average CO2 emissions
    st.markdown(
        "Average CO2 emissions of properties on {street_name}: **{avg_CO2_emissions}** (kWh/m²/year)".format(
            street_name=street_name,
            avg_CO2_emissions=avg_CO2_emissions
        )
    )
    # print average energy efficiency
    st.markdown(
        "Average energy efficiency of properties on {street_name}: **{avg_energy_efficiency}/100**".format(
            street_name=street_name,
            avg_energy_efficiency=avg_energy_efficiency
        )
    )
    # print percentage of properties with good rating
    st.markdown(
        "Percentage of properties on {street_name} with GOOD EPC rating (A-B-C-D): **{perc_good_rating}**".format(
            street_name=street_name,
            perc_good_rating=perc_good_rating
        )
    )
