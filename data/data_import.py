import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
from pandas_datareader import data as pdr

# Parameters
start_date = "2022-01-01"
end_date = "2023-01-01"

# Fetch EUR/USD Spot data from Yahoo Finance
df_spot = yf.download("EURUSD=X", start=start_date, end=end_date, interval="1d")

# Keep the 'Close' column as spot
df_spot = df_spot.rename(columns={"Close": "spot"}).reset_index()
df_spot.rename(columns={"Date": "date"}, inplace=True)
df_spot = df_spot[["date", "spot"]]

# Fetch interest rates from FRED
fred_api_key = "YOUR_OWN_FRED_API_KEY" # Replace with your own API key !

# Fetch USD rate (1Y Treasury Yield "GS1")
try:
    df_us_rate = pdr.DataReader("GS1", "fred", start_date, end_date, api_key=fred_api_key)
    df_us_rate = df_us_rate.rename(columns={"GS1": "domestic_rate"}).reset_index()
    df_us_rate.rename(columns={"DATE": "date"}, inplace=True)
    df_us_rate["domestic_rate"] = df_us_rate["domestic_rate"] / 100.0  # Convert to decimal
except Exception as e:
    print("Error fetching USD rate, fallback to 2%")
    df_us_rate = pd.DataFrame({"date": df_spot["date"], "domestic_rate": 0.02})  # Fixed fallback

# Fetch EUR rate (approximate long-term rate "IRLTLT01EZM156N")
try:
    df_eur_rate = pdr.DataReader("IRLTLT01EZM156N", "fred", start_date, end_date, api_key=fred_api_key)
    df_eur_rate = df_eur_rate.rename(columns={"IRLTLT01EZM156N": "foreign_rate"}).reset_index()
    df_eur_rate.rename(columns={"DATE": "date"}, inplace=True)
    df_eur_rate["foreign_rate"] = df_eur_rate["foreign_rate"] / 100.0  # Convert to decimal
except Exception as e:
    print("Error fetching EUR rate, fallback to 1%")
    df_eur_rate = pd.DataFrame({"date": df_spot["date"], "foreign_rate": 0.01})  # Fixed fallback

# Merge data (Spot + USD Rate + EUR Rate)
df = df_spot.merge(df_us_rate, on="date", how="left")
df = df.merge(df_eur_rate, on="date", how="left")

# Fill NaN values with forward fill for missing days
df["domestic_rate"].fillna(method="ffill", inplace=True)
df["foreign_rate"].fillna(method="ffill", inplace=True)
df["domestic_rate"].interpolate(method="linear", inplace=True)
df["foreign_rate"].interpolate(method="linear", inplace=True)

# Approximate volatility (20-day rolling historical volatility)
df["log_return"] = np.log(df["spot"] / df["spot"].shift(1))
df["volatility"] = df["log_return"].rolling(window=20).std() * np.sqrt(252)

# Drop initial NaN rows (caused by rolling volatility)
df.dropna(inplace=True)

# Remove log_return column before writing to CSV
df = df[["date", "spot", "domestic_rate", "foreign_rate", "volatility"]]

# Save to CSV file
df.to_csv("fx_data.csv", index=False)

# Preview the first few rows
print(df.head(10))
print(f"Average observed volatility: {df['volatility'].mean():.2%}")