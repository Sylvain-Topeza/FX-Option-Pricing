
# FX Option Pricing & Delta Hedging Strategy  

## 📌 Overview  
This project implements an **FX option pricer** using the **Garman-Kohlhagen model**, incorporating **real market data**.  
It also includes an **implied volatility calculator** and a **delta hedging backtest**, allowing an in-depth analysis of risk management efficiency in FX options trading.  

---

## ⚙️ Features  
### **1️⃣ FX Option Pricing (Garman-Kohlhagen Model)**  
- Computes **Call and Put prices** for FX options using market inputs (spot price, interest rates, and volatility).  
- Uses the **Garman-Kohlhagen formula**, which extends Black-Scholes for foreign exchange options:  

### **2️⃣ Implied Volatility Calculation**  
- Uses **numerical root-finding (Newton-Raphson method)** to estimate the implied volatility from market option prices.  
- Extracts **market expectations** on future price movements.

### **3️⃣ Delta Hedging Strategy Backtest**  
- Simulates a **delta hedging strategy** over a given time period.  
- Adjusts the hedge **daily** to remain delta-neutral.  
- Computes and visualizes **PnL evolution** throughout the hedging period.

### **4️⃣ Real Market Data Integration**  
- Fetches **FX spot rates** (EUR/USD) using Yahoo Finance.  
- Retrieves **interest rates** (EUR & USD) from FRED.  
- Calculates **historical volatility** from real price fluctuations.

---

## 📊 Methodology  
### **Step 1: Data Collection**  
The project collects the following market data:  
✅ **Spot FX Rate** (EUR/USD) from Yahoo Finance  
✅ **Risk-free interest rates** (EUR & USD) from FRED  
✅ **Volatility estimation** (using a 20-day rolling window)  

---

### **Step 2: FX Option Pricing (Garman-Kohlhagen Model)**  
- The model computes **Call and Put prices** using real interest rates and market volatility.  
- Pricing results depend on key parameters:  
  - **Spot price (S)**  
  - **Strike price (K)**  
  - **Time to maturity (T)**  
  - **Domestic interest rate (r)**  
  - **Foreign interest rate (q)**  
  - **Volatility (σ)**  

---

### **Step 3: Implied Volatility Calculation**  
- The script finds the volatility **σ** that matches the market price using a root-finding algorithm.  
- This allows for **extracting market expectations** regarding future volatility.  

---

### **Step 4: Delta Hedging Backtest**  
- We **simulate** a trader dynamically adjusting their hedge **each day**.  
- The trader buys/sells the underlying to maintain a **delta-neutral position**.  
- The **final PnL** measures the efficiency of the hedge.

---

## **🔍 Example Results**
### **1️⃣ Sample Option Pricing Output**


### **2️⃣ Delta Hedging Performance (PnL)**


### **3️⃣ PnL Chart**
![PNL Evolution](example_pnl_chart.png)

---

## 🖥️ Installation & Setup   
1️⃣ **Clone the repository**  
```bash
git clone https://github.com/Sylvain-Topeza/FX_Option_Pricing.git
cd FX-Option-Pricing

2️⃣ **Install dependencies**  
```bash
pip install -r requirements.txt

3️⃣ **Run the project**  
```bash
python main.py


---

### **📌 Requirements**
```md
## **🔧 Requirements**  
- Python 3.8+  
- Required libraries:  
```bash
pip install numpy pandas scipy matplotlib yfinance pandas_datareader


