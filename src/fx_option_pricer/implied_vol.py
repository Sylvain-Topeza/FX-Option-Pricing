import math
from scipy.stats import norm
from .garman_kohlhagen import garman_kohlhagen_call_price

def implied_vol_bissection(
    market_price, 
    spot, 
    strike, 
    domestic_rate, 
    foreign_rate, 
    time_to_maturity,
    is_call=True,
    lower_bound=0.0001, 
    upper_bound=5.0, 
    tolerance=1e-6
):
    """
    Calculate implied volatility using the bisection method.
    :param market_price: Market price of the option
    :param spot: Spot FX rate
    :param strike: Strike price
    :param domestic_rate: Domestic interest rate
    :param foreign_rate: Foreign interest rate
    :param time_to_maturity: Time to maturity (in years)
    :param is_call: Boolean, True if call option
    :param lower_bound: Lower bound for the search
    :param upper_bound: Upper bound for the search
    :param tolerance: Convergence tolerance
    :return: Implied volatility
    """
    
    def option_price(vol):
        # Here, we only handle the call option for simplicity
        return garman_kohlhagen_call_price(spot, strike, domestic_rate, foreign_rate, vol, time_to_maturity)
    
    for _ in range(100):
        mid = 0.5 * (lower_bound + upper_bound)
        price_mid = option_price(mid)
        
        if abs(price_mid - market_price) < tolerance:
            return mid
        
        # If the price at midpoint is too high, reduce the volatility
        if price_mid > market_price:
            upper_bound = mid
        else:
            lower_bound = mid
    
    # If we exit the loop, we have not converged
    return mid
