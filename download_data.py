from fetch_data import fetch_data, fetch_nordpool_data

df_spot_prices = fetch_data(
    dataset_name="Elspotprices",
    start="2023-08-01T00:00",
    end="2025-08-02T00:00",
    columns=["HourUTC", "PriceArea", "SpotPriceEUR"],
    filter_json={"PriceArea":["DK1", "DK2"]},
    sort="HourUTC asc",
    limit=0,
    timezone="UTC"
)

df_weather_forecast = fetch_data(
    dataset_name="Forecasts_hour",
    start="2023-08-01T00:00",
    end="2025-08-02T00:00",
    columns=["HourUTC", "PriceArea", "ForecastType", "ForecastDayAhead", "ForecastIntraday", "Forecast5Hour", "Forecast1Hour"],
    filter_json={"PriceArea":["DK1", "DK2"]},
    sort="HourUTC asc",
    limit=0,
    timezone="UTC"
)

df_weather_pivot = df_weather_forecast.pivot_table(
    index=['HourUTC','PriceArea'],
    columns='ForecastType',
    values=['ForecastDayAhead','ForecastIntraday','Forecast5Hour','Forecast1Hour']
)

df_weather_pivot.columns = ['_'.join(col).strip() for col in df_weather_pivot.columns.values]
df_weather_forecast = df_weather_pivot.reset_index()

df = df_spot_prices.merge(df_weather_forecast, on=['HourUTC','PriceArea'], how='left')

df.to_csv("df.csv", index=False)


#Håndter Missing Values
df = df.infer_objects()

# Interpolate kun numeriske cols, og ikke intraday_forecast fordi der er rigtig mange NaN. 
cols_to_interpolate = [
    'Forecast1Hour_Offshore Wind',
    'Forecast1Hour_Onshore Wind',
    'Forecast1Hour_Solar',
    'Forecast5Hour_Offshore Wind',
    'Forecast5Hour_Onshore Wind',
    'Forecast5Hour_Solar',
    'ForecastDayAhead_Offshore Wind',
    'ForecastDayAhead_Onshore Wind',
    'ForecastDayAhead_Solar'
]
df[cols_to_interpolate] = df[cols_to_interpolate].interpolate(method='linear', limit_direction='both')

#Intraday forecasts har alt for mange NaN, derfor ffill
intraday_cols = [
    'ForecastIntraday_Offshore Wind',
    'ForecastIntraday_Onshore Wind',
    'ForecastIntraday_Solar'
]
df[intraday_cols] = df[intraday_cols].ffill().bfill() #backfiller kun hvis starten af datasættet har NaN

df.to_csv("df_interpolate.csv", index=False)

#######      NORDPOOL DATA     #############
df_nordpool = fetch_nordpool_data(days_back=14)
df_nordpool.to_csv("df_nordpool.csv", index=False)