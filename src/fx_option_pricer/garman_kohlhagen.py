import math
from math import log, sqrt, exp
from scipy.stats import norm

def garman_kohlhagen_call_price(spot, strike, domestic_rate, foreign_rate, sigma, time_to_maturity):
    """
    Price of an FX call option using the Garman-Kohlhagen model.
    :param spot: Spot FX rate
    :param strike: Strike price
    :param domestic_rate: Domestic interest rate (e.g., USD)
    :param foreign_rate: Foreign interest rate (e.g., EUR)
    :param sigma: Volatility
    :param time_to_maturity: Time to maturity (in years)
    :return: Call option price
    """
    # d1 & d2
    d1 = (log(spot/strike) + (domestic_rate - foreign_rate + 0.5 * sigma**2) * time_to_maturity) \
         / (sigma * sqrt(time_to_maturity))
    d2 = d1 - sigma * sqrt(time_to_maturity)
    
    # Call price
    call_price = spot * exp(-foreign_rate * time_to_maturity) * norm.cdf(d1) \
                 - strike * exp(-domestic_rate * time_to_maturity) * norm.cdf(d2)
    return call_price

def garman_kohlhagen_put_price(spot, strike, domestic_rate, foreign_rate, sigma, time_to_maturity):
    """
    Price of an FX put option using the Garman-Kohlhagen model.
    :param spot: Spot FX rate
    :param strike: Strike price
    :param domestic_rate: Domestic interest rate (e.g., USD)
    :param foreign_rate: Foreign interest rate (e.g., EUR)
    :param sigma: Volatility
    :param time_to_maturity: Time to maturity (in years)
    :return: Put option price
    """
    # d1 & d2
    d1 = (log(spot/strike) + (domestic_rate - foreign_rate + 0.5 * sigma**2) * time_to_maturity) \
         / (sigma * sqrt(time_to_maturity))
    d2 = d1 - sigma * sqrt(time_to_maturity)
    
    # Put price
    put_price = strike * exp(-domestic_rate * time_to_maturity) * norm.cdf(-d2) \
                - spot * exp(-foreign_rate * time_to_maturity) * norm.cdf(-d1)
    return put_price
