from scrape import fetch_data


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

#Tjek eventuelt
#print(df.head(1000))
#print(df.columns)

#bool = df_weather_forecast.isna().mean()
#print(bool)

df