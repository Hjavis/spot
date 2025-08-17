import pandas as pd

df = pd.read_csv("df.csv")
df_interpolate = pd.read_csv("df_interpolate.csv")
df_nordpool = pd.read_csv("df_nordpool.csv")

print(df.tail(50))
print(df_interpolate.tail(50))
print(df_nordpool.head(50))
print(df.columns)