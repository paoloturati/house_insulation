# House Insulation

The code included in this repo produces two Streamlit Web Apps: one to compute the ideal Energy Bill for a given house (https://paoloturati-house-insulation-calculate-energy-bills-n2lzvy.streamlit.app/), one to compute the actual Energy Efficiency of the house (https://paoloturati-house-insulation-calculate-house-efficiency-g7ikc3.streamlit.app/).

## Background

The motivation for this work lie in the measurement of the necessary energy required to heat (or cool) a home, based on its characteristics, such as geometry and materials. A home, or a building, can be seen as a "box", surrounded by external air: the heating system is what regulates the temperature inside the "box". Depending on how the "box" is build and on the external temperature, more or less energy will be required to maintain a constant internal temperature.

The external temperature can be monitored in several ways, but, for this work, I used the **Degree Days** (https://www.degreedays.net/) data for a station near Reading, UK. The full explanation for computing the energy consumption to maintain a given internal temperature is provided in the Degree Days page. They also provide a very useful API to retrieve data on external temperature through a paid subscription: for this work I used a file I downloaded manually (one year of data) which is provided in this repo, so that the App can be executed. In case a dynamic set of data is required, the App should be linked through their API (installing their required library and paying to access their data).

## Energy Bills App

This Web App requires you to enter the characteristics of the external surfaces of your home (windows area, walls area, etc), how you heat your home (gas or electricity) and how much you heat it for (ex: 20C for 4 hours a day). Based on this generic information, it estimates the required energy needed to heat this home for a year (using the Degree Days data for Reading, UK) **as if** your home had optimal insulation. The energy tarifs are updated to October 2022 and the U-values used for walls, windows, roof and floor are available in the repo.

**Disclaimer**

Obviously the real energy bills take into account **all** the energy consumed across a period of time, not only the one used to heat your home: here we're estimating the cost for home heating only, therefore these figures cannot be used for direct comparison with real energy bills.

## House Efficiency App

This Web App, like the previous one, requires you to enter the characteristics of the external surfaces and the desired heating habits (we don't need to know whether the home is heated by gas or electricity). On top of this information, the App requires you to enter two meter readings taken in different dates, so that, we know the actual energy that was consumed in that period. The App then calculates how much energy is required to heat the same home, with the same settings, in two different scenarios:
- scenario 1: the home has optimal insulation (best case scenario)
- scenario 2: the home has very poor insulation (worst case scenario)
The House Efficiency coefficient is based on this scale, giving a 0 in case your home performs like (or worse than) a poorly insulated home, 100 in case your home requires the same (or less) energy than a optimally insulated home, or a value in between otherwise.

**Disclaimer**

Obviously the real energy bills take into account **all** the energy consumed across a period of time, not only the one used to heat your home: here we're estimating the cost for home heating only, therefore these figures cannot be used for direct comparison with real energy bills.

**Disclaimer 2**

Since the Degree Days data is a static file, please only select periods of time between February 2021 and February 2022.

### Streamlit deployment

Streamlit is an excellent tool for building quick POCs, it provides a simple but effective UI and it's ideal to develop new projects in local. They've recently enabled deployment on remote servers and all the instructions can be found here (https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app).