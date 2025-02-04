import numpy as np
import pandas as pd
from scipy.stats import norm
from math import log, sqrt, exp

def delta_garman_kohlhagen_call(spot, strike, domestic_rate, foreign_rate, sigma, time_to_maturity):
    """
    Delta of the FX call option under the Garman-Kohlhagen model.
    """
    d1 = (log(spot/strike) + (domestic_rate - foreign_rate + 0.5 * sigma**2) * time_to_maturity) \
         / (sigma * sqrt(time_to_maturity))
    return exp(-foreign_rate * time_to_maturity) * norm.cdf(d1)

def backtest_delta_hedge(data, strike, domestic_rate, foreign_rate, sigma, maturity_days):
    """
    Backtest daily delta hedging for an FX call option.
    :param data: DataFrame with columns ['date', 'spot']
    :param strike: Strike price
    :param domestic_rate: Domestic interest rate
    :param foreign_rate: Foreign interest rate
    :param sigma: Volatility
    :param maturity_days: Number of days to maturity
    :return: DataFrame with PnL, delta, etc.
    """
    # Copy the DataFrame to avoid modifying the original
    df = data.copy()
    print(f"Size after potential filtering: {df.shape}")
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').reset_index(drop=True)
    
    if df.empty:
        raise ValueError("Error: Empty DataFrame in backtest! Check data loading.")
    
    # Assume each row represents one day
    print(f"DataFrame size before calculating days: {df.shape}")
    print(df.head())
    print(f"Unique index values: {df.index.unique()}")
    df['days_to_maturity'] = maturity_days - pd.Series(df.index, dtype=int)
    print("`days_to_maturity` calculated successfully")
    print(df[['date', 'days_to_maturity']].head())

    # Initialization
    notional = 1.0  # Assume 1 contract
    df['delta'] = 0.0
    df['hedge_position'] = 0.0
    df['pnl_hedge'] = 0.0
    df['option_value'] = 0.0
    
    # Iterate over each day
    for i in range(len(df)):
        ttm = df.loc[i, 'days_to_maturity'] / 365.0
        if ttm <= 0:
            # Option expired, no more PnL after
            df.loc[i:, 'option_value'] = 0.0
            break
        
        # Calculate delta
        spot_i = df.loc[i, 'spot']
        delta_i = delta_garman_kohlhagen_call(spot_i, strike, domestic_rate, foreign_rate, sigma, ttm)
        
        df.loc[i, 'delta'] = delta_i
        
        # Option value (call)
        from .garman_kohlhagen import garman_kohlhagen_call_price
        option_val = garman_kohlhagen_call_price(spot_i, strike, domestic_rate, foreign_rate, sigma, ttm)
        df.loc[i, 'option_value'] = option_val
        
        if i == 0:
            # Initialize hedge position
            df.loc[i, 'hedge_position'] = -delta_i * notional
        else:
            # Adjust hedge position
            prev_delta = df.loc[i-1, 'delta']
            delta_change = delta_i - prev_delta
            df.loc[i, 'hedge_position'] = df.loc[i-1, 'hedge_position'] - delta_change * notional
            
            # Calculate PnL on the hedge (spot difference * position)
            df.loc[i, 'pnl_hedge'] = (df.loc[i, 'spot'] - df.loc[i-1, 'spot']) * df.loc[i-1, 'hedge_position']
    
    # Final option value at expiration
    if len(df) > 0:
        final_index = df.index[-1]
        final_spot = df.loc[final_index, 'spot']
        payoff = max(final_spot - strike, 0.0)  # call payoff
        df.loc[final_index, 'option_value'] = payoff
    
    # Calculate cumulative PnL on the hedge
    df['pnl_hedge_cum'] = df['pnl_hedge'].cumsum()
    
    return df
