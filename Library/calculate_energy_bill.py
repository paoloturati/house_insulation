from Library import consts

# import parameters
PARAMS = consts.PARAMS["energy_tarifs"]

def main(daily_consumption, fuel):
    """
    This function, given the daily energy consumption and the heating type,
    calculates the energy bill for this day.

    Inputs
        daily_consumption: float
            Energy consumed daily (expressed in kWh)
        fuel: str
            Type of heating ("electricity" or "gas")

    Outputs
        total_bill: float
            Daily cost for energy consumption (expressed in GBP)
    """

    total_bill = round(daily_consumption * PARAMS[fuel]["kWh"] + (PARAMS[fuel]["fixed_rate"]/365), 2)

    return total_bill
