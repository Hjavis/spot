import pandas as pd

df = pd.read_csv("df.csv")
df_interpolate = pd.read_csv("df_interpolate.csv")

print(df.head(50))
print(df_interpolate.head(50))