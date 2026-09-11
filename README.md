# ERCOT Demand vs. Generation Analysis

## Project Overview

This project examines how temperature affects electricity demand on the Texas power grid (ERCOT), and identifies the point at which rising demand shrinks the grid's generation cushion, the safety margin between how much power is being produced and how much is being used.

Using five years of hourly grid data from the U.S. Energy Information Administration (EIA) and hourly temperature data from NOAA (Houston station), this analysis connects weather conditions to grid reliability risk, with a specific focus on identifying when that safety margin becomes dangerously thin.

## Main Analysis Question

How does temperature affect electricity demand in Texas, and at what point does that increased demand shrink the generation cushion enough to represent a real reliability risk?

## Why This Matters

Texas operates its own largely self-contained power grid, meaning it has limited ability to import power from neighboring states during periods of extreme demand. Understanding when and why the grid's safety margin gets thin, and whether that pattern is predictable based on temperature, is directly useful for reserve capacity planning, maintenance scheduling, and reliability risk management.

# Technology Workflow

![Tech Workflow](screenshots/tech_workflow.png)

* REST API: [EIA](https://www.eia.gov/opendata/) was used to source hourly electricity demand and generation data for ERCOT, and [NOAA](https://www.ncei.noaa.gov/access/services/data/v1) was used to source hourly temperature data for Houston.
* Extract/Transform: Python, using `requests` and `pandas`, handled pulling data from both APIs, reshaping the electricity data into a usable format, and merging both sources together on their shared hourly timestamp.
* Storage: PostgreSQL was used for data storage, structured as a single flat table rather than a star schema, since this dataset is a single time series with no natural dimensions to separate out.
* Analysis: SQL was used to check data quality and calculate the generation cushion (net generation minus demand), the core metric used to measure grid reliability risk.
* Visualization: Power BI was used to build an interactive dashboard displaying the relationship between temperature, demand, and grid cushion.

# Data Schema

![Database Schema](screenshots/database_schema.png)

The diagram above shows the database's schema design, which uses a single flat table rather than a star schema. This approach was chosen because the underlying data is fundamentally a single hourly time series (electricity demand, generation, and temperature) with no repeating categorical fields like organization, location, or job category that would benefit from being broken out into separate dimension tables. Splitting this data into multiple tables would add unnecessary complexity without any real analytical benefit, so a single table was used instead.

# Data dictionary

## Data Dictionary

| Column Name | Data Type | Description |
|---|---|---|
| `period` | timestamp | The hour the reading corresponds to (UTC). Serves as the primary key. |
| `demand` | numeric | Actual electricity demand for ERCOT during that hour, in megawatthours. |
| `day_ahead_forecast` | numeric | EIA's day-ahead forecasted demand for that hour, in megawatthours. |
| `net_generation` | numeric | Actual electricity generated for ERCOT during that hour, in megawatthours. |
| `total_interchange` | numeric | Net power exchanged with neighboring grids during that hour, in megawatthours. Negative values indicate net import, positive values indicate net export. |
| `temperature` | numeric | Hourly temperature reading from the Houston Bush Intercontinental Airport (IAH) station, in degrees Fahrenheit. |
| `cushion` | numeric | Calculated as `net_generation` minus `demand`. Represents the grid's reserve margin for that hour; lower or negative values indicate elevated reliability risk. |







