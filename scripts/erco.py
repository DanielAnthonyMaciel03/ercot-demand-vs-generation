import time
import requests
import pandas as pd

# This script connects to the EIA government website and downloads five years of electricity data for Texas, from January 2020 through January 2025.
# The data it pulls covers four things for every single hour in that time range: how much electricity was used (demand), how much EIA predicted would be 
# used the day before (forecast), how much electricity was actually produced (generation), and how much power moved in or out of Texas from other states (interchange).
# Because the website only allows 5,000 rows to be downloaded at a time, the script asks for the data in chunks. It keeps asking for the next chunk, adding each 
# one to a growing list, until it has collected everything. This is why there is a loop in the middle of the script. Between each request, it pauses for a third of a 
# second so it does not overload the website's server. Once every row has been collected, the script turns the whole list into a table and saves it as a CSV file so 
# it can be used in later steps without needing to download everything again.

API_KEY = "ghjqdHcy9ysBQgz3cxzGKBL7wyXL00rRNDRq1a1G"  

BASE_URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

START_DATE = "2020-01-01T00"
END_DATE = "2025-01-01T00"  
RESPONDENT = "ERCO"
PAGE_SIZE = 5000

all_rows = []
offset = 0

while True:
    params = {
        "api_key": API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "facets[respondent][]": RESPONDENT,
        "start": START_DATE,
        "end": END_DATE,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": offset,
        "length": PAGE_SIZE,
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    rows = payload["response"]["data"]
    total = int(payload["response"]["total"])

    if not rows:
        break

    all_rows.extend(rows)
    print(f"Retrieved {len(all_rows)} / {total} rows...")

    offset += PAGE_SIZE

    if len(all_rows) >= total:
        break

    time.sleep(0.3)  

df = pd.DataFrame(all_rows)
df.to_csv("raw data/eia_ercot_2020-2025.csv", index=False)
