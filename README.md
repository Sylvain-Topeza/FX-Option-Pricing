# FX Option Pricing & Delta Hedging Strategy  

## 📌 Overview  
This project implements an **FX option pricer** using the **Garman-Kohlhagen model**, incorporating **real market data**. It also features an **implied volatility calculator** and a **delta hedging backtest** to analyze hedging efficiency.  

## ⚙️ Features  
- **Garman-Kohlhagen model** for pricing FX call and put options  
- **Implied volatility computation** via numerical root-finding  
- **Delta hedging strategy** to manage risk exposure  
- **Market data integration** (EUR/USD spot price, interest rates, and volatility)  

## 📊 Methodology  
1. **Data Collection**:  
   - **Spot FX rate** (EUR/USD) from Yahoo Finance  
   - **Interest rates** (EUR & USD) from FRED  
   - **Historical volatility estimation** using a rolling 20-day window  

2. **Option Pricing (Garman-Kohlhagen Model)**:  
   - Uses **interest rates & volatility** to compute call/put prices  
   - Formula:  
     \[
     C = S e^{-qT} N(d1) - K e^{-rT} N(d2)
     \]

3. **Implied Volatility Calculation**:  
   - Uses numerical root-finding to extract market expectations  

4. **Delta Hedging Backtest**:  
   - Simulates **daily hedging adjustments**  
   - Computes **PnL over the hedging period**  

## 🖥️ Installation & Setup  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/FX_Option_Pricing_Delta_Hedging.git
   cd FX_Option_Pricing_Delta_Hedging
