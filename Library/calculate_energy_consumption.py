from Library import consts
import numpy as np

# import parameters
PARAMS_PROPERTY = consts.PARAMS["property_info"]
PARAMS_ENVIRONMENT = consts.PARAMS["environment"]


def main(property_info, temp_gap, month, hours_day, insulation):
    """
    This function, given a property characteristics, the temperature gap to overcome,
    the month of the year and the time the heating is ON (expressed in hours), calculates the
    energy required to maintain the desired temperature.

    Inputs
        property_info: dict
            Each key contains values which describe the property
        temp_gap: float
            Difference between external temperature and internal temperature (expressed in degrees)
        month: str
            Defined as a 2-digit string of a number between 1 and 12
        hours_day: float
            Number of hours in which the heating is ON
        insulation: str
            It defines the type of insulation (either "WELL_INSULATED" or "POORLY_INSULATED")

    Outputs
        total_energy_day: float
            Daily energy consumption (expressed in kWh)
    """

    # calculate the property volume
    if property_info["walls_height"] is np.nan:
        # walls height not defined, use default values
        volume_property = (
            property_info["area_floor"]
            * property_info["floors"]
            * PARAMS_PROPERTY["WALLS_HEIGHT"]
        )
    else:
        volume_property = (
            property_info["area_floor"]
            * property_info["floors"]
            * property_info["walls_height"]
        )
    # calculate energy lost through floor
    energy_floor = (
        property_info["area_floor"] * temp_gap * PARAMS_PROPERTY[insulation]["floor"]
    )
    # calculate energy lost through roof
    energy_roof = (
        property_info["area_roof"] * temp_gap * PARAMS_PROPERTY[insulation]["roof"]
    )
    # calculate energy lost through windows
    energy_windows = (
        property_info["area_windows"]
        * temp_gap
        * PARAMS_PROPERTY[insulation]["windows"]
    )
    # calculate energy lost through walls
    energy_walls = (
        property_info["area_walls"] * temp_gap * PARAMS_PROPERTY[insulation]["walls"]
    )
    # calculate energy lost through drafts
    energy_drafts = (
        PARAMS_PROPERTY[insulation]["ACH"]
        * PARAMS_ENVIRONMENT["SEASON_ACH"][month]
        * volume_property
        * temp_gap
    )
    # add up all components
    total_energy_hour = (
        energy_floor + energy_roof + energy_windows + energy_walls + energy_drafts
    )
    # compute energy for the full day
    total_energy_day = np.round((total_energy_hour * hours_day) / 1000, 2)

    return total_energy_day
