import os
import time
import requests
import pandas as pd
from io import StringIO

# This script downloads five years of weather data for the Houston airport station, from 2020 through 2024, then cleans it up so it can be used later.
# Since the weather website only lets you pull one year at a time, the script loops through each year, downloads it separately, and then stacks all five 
# years together into one big table. It saves this raw, unprocessed version first.
# Then it cleans the data in a few steps. It keeps only the columns that actually matter (the station, the date, the report type, and the temperature) 
# and drops everything else. Some temperature readings come through as broken or non-numeric text instead of real numbers, so the script forces that column 
# to be strictly numeric and turns anything that fails into a blank value, which then gets removed.
# The weather station sometimes reports multiple readings within the same hour instead of just one clean hourly reading. To fix this, the script rounds 
# every timestamp down to its hour, then averages together any readings that landed in the same hour. This leaves exactly one temperature value per hour.
# Finally, it saves this cleaned, hourly version as its own file, ready to be joined with the electricity data later.

BASE_URL = "https://www.ncei.noaa.gov/access/services/data/v1"
STATION = "72243012960"  # Houston Bush Intercontinental (IAH)

# Step 1: Pull raw data from API one year at a time

years = range(2020, 2025)
all_raw = []

for year in years:
    params = {
        "dataset": "local-climatological-data",
        "stations": STATION,
        "startDate": f"{year}-01-01",
        "endDate": f"{year}-12-31",
        "format": "csv",
    }

    response = requests.get(BASE_URL, params=params, timeout=60)
    response.raise_for_status()

    year_df = pd.read_csv(StringIO(response.text), low_memory=False)
    all_raw.append(year_df)
    time.sleep(0.5)

raw_df = pd.concat(all_raw, ignore_index=True)

os.makedirs("raw data", exist_ok=True)
raw_df.to_csv("raw data/noaa_iah_raw.csv", index=False)

# Step 2: Clean the pulled data

keep_cols = ["STATION", "DATE", "REPORT_TYPE", "HourlyDryBulbTemperature"]
df = raw_df[keep_cols].copy()

df["DATE"] = pd.to_datetime(df["DATE"])

df["HourlyDryBulbTemperature"] = pd.to_numeric(
    df["HourlyDryBulbTemperature"], errors="coerce"
)

df = df.dropna(subset=["HourlyDryBulbTemperature"])

df["hour"] = df["DATE"].dt.floor("h")

hourly = df.groupby("hour").agg(
    temperature=("HourlyDryBulbTemperature", "mean")
).reset_index()

hourly.to_csv("raw data/noaa_iah_cleaned.csv", index=False)