import streamlit as st
import pandas as pd

# read file with Reading streets
reading_streets_mapping = pd.read_csv("Mapping_Reading_housing_stock_v2.csv")

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
    # extract street metrics
    num_properties = df["num_properties"].iloc[0]
    # insulation absolute numbers
    properties_roof_insulation = df["properties_roof_insulation"].iloc[0]
    properties_walls_insulation = df["properties_walls_insulation"].iloc[0]
    properties_windows_insulation = df["properties_windows_insulation"].iloc[0]
    properties_floor_insulation = df["properties_floor_insulation"].iloc[0]
    # insulation percentages
    perc_roof_insulation = df["perc_properties_roof_insulation"].iloc[0]
    perc_walls_insulation = df["perc_properties_walls_insulation"].iloc[0]
    perc_windows_insulation = df["perc_properties_windows_insulation"].iloc[0]
    perc_floor_insulation = df["perc_properties_floor_insulation"].iloc[0]
    # emission and consumption metrics
    avg_CO2_emissions = df["avg_CO2_emissions"].iloc[0]
    avg_energy_consumption = df["avg_energy_consumption"].iloc[0]
    avg_energy_efficiency = df["avg_energy_efficiency"].iloc[0]
    # breakdown of properties
    properties_A = df["properties_A_rating"].iloc[0]
    properties_B = df["properties_B_rating"].iloc[0]
    properties_C = df["properties_C_rating"].iloc[0]
    properties_D = df["properties_D_rating"].iloc[0]
    properties_E = df["properties_E_rating"].iloc[0]
    properties_F = df["properties_F_rating"].iloc[0]
    properties_G = df["properties_G_rating"].iloc[0]
    perc_A = df["perc_properties_A_rating"].iloc[0]
    perc_B = df["perc_properties_B_rating"].iloc[0]
    perc_C = df["perc_properties_C_rating"].iloc[0]
    perc_D = df["perc_properties_D_rating"].iloc[0]
    perc_E = df["perc_properties_E_rating"].iloc[0]
    perc_F = df["perc_properties_F_rating"].iloc[0]
    perc_G = df["perc_properties_G_rating"].iloc[0]
    # print number of properties
    st.markdown(
        "Number of properties on {street_name}: **{num_properties}**".format(
            street_name=street_name,
            num_properties=num_properties
        )
    )
    # print properties with insulated roof
    st.markdown(
        "Properties on {street_name} with ROOF insulation: **{insulated_properties}** ({perc_insulated_properties}%)".format(
            street_name=street_name,
            insulated_properties=properties_roof_insulation,
            perc_insulated_properties=perc_roof_insulation
        )
    )
    # print properties with insulated walls
    st.markdown(
        "Properties on {street_name} with WALLS insulation: **{insulated_properties}** ({perc_insulated_properties}%)".format(
            street_name=street_name,
            insulated_properties=properties_walls_insulation,
            perc_insulated_properties=perc_walls_insulation
        )
    )
    # print properties with insulated windows
    st.markdown(
        "Properties on {street_name} with WINDOWS insulation: **{insulated_properties}** ({perc_insulated_properties}%)".format(
            street_name=street_name,
            insulated_properties=properties_windows_insulation,
            perc_insulated_properties=perc_windows_insulation
        )
    )
    # print properties with insulated floor
    st.markdown(
        "Properties on {street_name} with FLOOR insulation: **{insulated_properties}** ({perc_insulated_properties}%)".format(
            street_name=street_name,
            insulated_properties=properties_floor_insulation,
            perc_insulated_properties=perc_floor_insulation
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
    # print properties' ratings
    st.markdown(
        "Properties on {street_name} with EPC A: **{properties_rating}** ({perc_rating}%)".format(
            street_name=street_name,
            properties_rating=properties_A,
            perc_rating=perc_A
        )
    )
    st.markdown(
        "Properties on {street_name} with EPC B: **{properties_rating}** ({perc_rating}%)".format(
            street_name=street_name,
            properties_rating=properties_B,
            perc_rating=perc_B
        )
    )
    st.markdown(
        "Properties on {street_name} with EPC C: **{properties_rating}** ({perc_rating}%)".format(
            street_name=street_name,
            properties_rating=properties_C,
            perc_rating=perc_C
        )
    )
    st.markdown(
        "Properties on {street_name} with EPC D: **{properties_rating}** ({perc_rating}%)".format(
            street_name=street_name,
            properties_rating=properties_D,
            perc_rating=perc_D
        )
    )
    st.markdown(
        "Properties on {street_name} with EPC E: **{properties_rating}** ({perc_rating}%)".format(
            street_name=street_name,
            properties_rating=properties_E,
            perc_rating=perc_E
        )
    )
    st.markdown(
        "Properties on {street_name} with EPC F: **{properties_rating}** ({perc_rating}%)".format(
            street_name=street_name,
            properties_rating=properties_F,
            perc_rating=perc_F
        )
    )
    st.markdown(
        "Properties on {street_name} with EPC G: **{properties_rating}** ({perc_rating}%)".format(
            street_name=street_name,
            properties_rating=properties_G,
            perc_rating=perc_G
        )
    )
