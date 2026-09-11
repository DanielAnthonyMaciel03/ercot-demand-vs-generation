import pandas as pd

# This script combines the two cleaned datasets into one single table. It loads both the electricity data and the weather data, then makes 
# sure the timestamp column in each one is treated as a real date and time rather than plain text, so they can be matched up correctly.
# It then joins the two tables together by matching each electricity hour to the weather reading from that same hour. Only hours that exist in both 
# datasets are kept, so if either dataset is missing a particular hour, that hour gets dropped from the final result rather than left blank.
# The combined table, now containing both electricity numbers and temperature for every matching hour, is saved as one final file. This is the dataset 
# that everything else, like the cushion calculation and the analysis, will be built on top of.

EIA_PATH = "raw data/eia_ercot_wide.csv"
NOAA_PATH = "raw data/noaa_iah_cleaned.csv"
OUTPUT_PATH = "raw data/merged_final.csv"

eia = pd.read_csv(EIA_PATH)
noaa = pd.read_csv(NOAA_PATH)

eia["period"] = pd.to_datetime(eia["period"])
noaa["hour"] = pd.to_datetime(noaa["hour"])

merged = pd.merge(
    eia, noaa,
    left_on="period", right_on="hour",
    how="inner"
)

merged.to_csv(OUTPUT_PATH, index=False)