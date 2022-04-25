from Library import consts


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
