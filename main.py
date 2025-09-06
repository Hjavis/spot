import pandas as pd

df = pd.read_csv("df.csv")
df_interpolate = pd.read_csv("df_interpolate.csv")
df_nordpool = pd.read_csv("df_nordpool.csv")

#Konverter til datetime
df["HourUTC"] = pd.to_datetime(df["HourUTC"])
df_nordpool["HourUTC"] = pd.to_datetime(df_nordpool["HourUTC"])
df_interpolate["HourUTC"] = pd.to_datetime(df_interpolate["HourUTC"])

print(df.tail(50))
print(df_interpolate.tail(50))
print(df_nordpool.head(50))
print(df.columns)

#pris tjek
slice_df = df_interpolate[
    (df_interpolate['HourUTC'] >= "2025-08-22") &
    (df_interpolate['HourUTC'] <= "2025-08-23")
]

slice_df2 = df[
    (df['HourUTC'] >= "2025-08-22") &
    (df['HourUTC'] <= "2025-08-23")
]

slice_dfnord = df_nordpool[
    (df_nordpool['HourUTC'] >= "2025-08-22") &
    (df_nordpool['HourUTC'] <= "2025-08-23")
]

print(slice_df)
print(slice_df2)
print(slice_dfnord)