import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from src.fx_option_pricer.garman_kohlhagen import garman_kohlhagen_call_price, garman_kohlhagen_put_price
from src.fx_option_pricer.implied_vol import implied_vol_bissection
from src.fx_option_pricer.backtest import backtest_delta_hedge

def main(spot, strike, sigma, T, maturity_days):
    # Load data
    data = pd.read_csv('data/fx_data.csv')
    
    # Get the first row's interest rates
    domestic_rate = data.loc[0, 'domestic_rate']
    foreign_rate = data.loc[0, 'foreign_rate']

    # Calculate call and put prices
    call_price = garman_kohlhagen_call_price(spot, strike, domestic_rate, foreign_rate, sigma, T)
    put_price = garman_kohlhagen_put_price(spot, strike, domestic_rate, foreign_rate, sigma, T)
    
    # Implied volatility
    market_call_price = call_price + 0.005  # market prices a slight spread
    iv = implied_vol_bissection(market_call_price, spot, strike, domestic_rate, foreign_rate, T)
    
    # Backtest delta hedging
    result_df = backtest_delta_hedge(data, strike, domestic_rate, foreign_rate, sigma, maturity_days)
    
    # Display results in a message box
    results_message = (
        f"Call price (Garman-Kohlhagen): {call_price:.4f}\n"
        f"Put price (Garman-Kohlhagen): {put_price:.4f}\n"
        f"Implied volatility: {iv:.2%}\n"
    )
    messagebox.showinfo("Option Pricing Results", results_message)
    
    # Visualize PnL
    plt.figure(figsize=(10,5))
    plt.plot(result_df['date'], result_df['pnl_hedge_cum'], label='Cumulative Hedge PnL')
    plt.title('Delta-Hedging PnL')
    plt.xlabel('Date')
    plt.ylabel('PNL')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def get_user_input():
    def submit():
        try:
            spot = float(spot_entry.get())
            strike = float(strike_entry.get())
            sigma = float(sigma_entry.get())
            T = float(T_entry.get())
            maturity_days = int(maturity_days_entry.get())
            root.destroy()
            main(spot, strike, sigma, T, maturity_days)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid input. Please enter valid numbers.")

    root = tk.Tk()
    root.title("FX Option Pricer")
    root.geometry("400x300")
    root.configure(bg="#2c3e50")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#2c3e50", foreground="#ecf0f1", font=("Helvetica", 12))
    style.configure("TEntry", font=("Helvetica", 12))
    style.configure("TButton", background="#3498db", foreground="#ecf0f1", font=("Helvetica", 12, "bold"))

    ttk.Label(root, text="Enter spot price:").grid(column=0, row=0, padx=10, pady=10, sticky="W")
    spot_entry = ttk.Entry(root)
    spot_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(root, text="Enter strike price:").grid(column=0, row=1, padx=10, pady=10, sticky="W")
    strike_entry = ttk.Entry(root)
    strike_entry.grid(column=1, row=1, padx=10, pady=10)

    ttk.Label(root, text="Enter initial volatility:").grid(column=0, row=2, padx=10, pady=10, sticky="W")
    sigma_entry = ttk.Entry(root)
    sigma_entry.grid(column=1, row=2, padx=10, pady=10)

    ttk.Label(root, text="Enter time to maturity (in years):").grid(column=0, row=3, padx=10, pady=10, sticky="W")
    T_entry = ttk.Entry(root)
    T_entry.grid(column=1, row=3, padx=10, pady=10)

    ttk.Label(root, text="Enter number of hedging days:").grid(column=0, row=4, padx=10, pady=10, sticky="W")
    maturity_days_entry = ttk.Entry(root)
    maturity_days_entry.grid(column=1, row=4, padx=10, pady=10)

    submit_button = ttk.Button(root, text="Submit", command=submit)
    submit_button.grid(column=0, row=5, columnspan=2, pady=20)

    root.mainloop()

if __name__ == "__main__":
    get_user_input()