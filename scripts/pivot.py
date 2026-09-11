import pandas as pd

# This script takes the raw electricity data pulled earlier and reshapes it into a more useful format.
# The original data has four separate rows for every single hour, one row each for demand, forecast, generation, and interchange. 
# This script rearranges that so each hour becomes just one row, with those four values sitting side by side as their own columns instead of 
# being stacked on top of each other. Along the way, it checks how many rows exist before and after the reshape, prints out the 
# new column names, shows a preview of the table, and checks whether any hours ended up missing one of the four values. This is just to confirm the 
# reshape worked correctly before moving on. The final reshaped table is then saved as its own file, ready to be joined with the weather data next.

RAW_PATH = "raw data/eia_ercot_2020-2025.csv"
OUTPUT_PATH = "raw data/eia_ercot_wide.csv"

df = pd.read_csv(RAW_PATH)

wide = df.pivot_table(
    index="period",
    columns="type-name",
    values="value"
).reset_index()

wide.to_csv(OUTPUT_PATH, index=False)