# 🇮🇳 Indian Mutual Funds Analysis Dashboard

A comprehensive, production-ready financial dashboard for analyzing Indian mutual funds with real-time NAV data, returns calculation, risk metrics, and SIP planning tools.

## 📸 Screenshots

Similar to the HDFCBANK.NS analysis dashboard you showed, this application provides:
- Real-time price charts with candlestick visualization
- Interactive sliders for period selection and investment calculations
- Comprehensive technical analysis and returns breakdown
- Wealth growth calculator with visual projections

## ✨ Features

### 📊 Core Analytics
- **Real-Time NAV Tracking** - Live data from MFAPI.in
- **Interactive Charts** - Candlestick-style charts with moving averages
- **Multi-Period Returns** - 1W, 1M, 3M, 6M, 1Y, 3Y, 5Y CAGR
- **Risk Metrics** - Volatility, Sharpe Ratio, Maximum Drawdown
- **Performance Stats** - Win rate, best/worst days, distribution analysis

### 💰 Investment Tools
- **SIP Calculator** - Systematic Investment Plan projections
- **Lumpsum Calculator** - One-time investment returns
- **Wealth Growth Visualization** - Interactive growth charts
- **Historical Returns Analysis** - CAGR calculations

### 🎨 User Interface
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Theme** - Easy on the eyes for long analysis sessions
- **Interactive Sliders** - Adjust parameters in real-time
- **Data Export** - Download analysis results

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for real-time data)

### Installation

1. **Clone or Download the Files**
```bash
# Create a new directory
mkdir indian-mf-dashboard
cd indian-mf-dashboard

# Download the files (or copy them manually)
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the Application**
```bash
streamlit run app.py
```

4. **Open in Browser**
The app will automatically open at `http://localhost:8501`

## 📁 Project Structure

```
indian-mf-dashboard/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 💡 Usage Guide

### 1. Fund Selection

**Step 1:** Use the sidebar to search for funds
```
Search Box → Enter "HDFC" or "SBI" or any AMC name
```

**Step 2:** Select from filtered results
```
Dropdown → Choose specific fund scheme
```

**Step 3:** Select analysis period
```
Period Selector → 1M, 3M, 6M, 1Y, 3Y, 5Y, or All Data
```

### 2. Viewing Analysis

#### Tab 1: 📈 Charts
- View NAV trend line chart
- Toggle moving averages (50-day, 200-day)
- See NAV statistics and fund age

#### Tab 2: 💰 Returns
- Compare returns across all periods
- View absolute returns vs CAGR
- Analyze return patterns

#### Tab 3: ⚠️ Risk
- Check volatility and risk metrics
- Understand maximum drawdown
- View Sharpe ratio for risk-adjusted returns

#### Tab 4: 🧮 SIP Calculator
- Enter monthly SIP amount (₹500 to ₹1,000,000)
- Select investment duration (1-30 years)
- Use historical returns or custom expected returns
- View wealth projection chart
- See year-wise breakdown

#### Tab 5: 📊 Stats
- Performance statistics
- Distribution analysis
- Win rate and daily returns data

### 3. Interactive Features

**Sliders:**
- Monthly SIP Amount: `₹500` to `₹1,000,000`
- Investment Duration: `1` to `30` years
- Expected Return: `0%` to `30%` p.a.

**Toggles:**
- Show Moving Averages: ON/OFF
- Use Custom Return Rate: ON/OFF

**Filters:**
- Search by fund name
- Filter by time period

## 📊 Data Source

**API:** MFAPI.in (https://www.mfapi.in/)
- Free, public API for Indian mutual funds
- Updated daily with NAV data
- No API key required
- Covers 40,000+ mutual fund schemes

**Data Includes:**
- Daily NAV (Net Asset Value)
- Fund metadata (name, category, type)
- Historical data (inception to current)

## 🧮 Calculations Explained

### Returns Calculation

**Absolute Return:**
```python
Return (%) = ((Current NAV - Old NAV) / Old NAV) × 100
```

**CAGR (Compound Annual Growth Rate):**
```python
CAGR = (((Current NAV / Old NAV) ^ (1 / Years)) - 1) × 100
```

### Risk Metrics

**Volatility (Annualized):**
```python
Volatility = Daily Returns Std Dev × √252
```

**Sharpe Ratio:**
```python
Sharpe = (Annual Return - Risk Free Rate) / Volatility
```

**Maximum Drawdown:**
```python
Drawdown = (Current Value - Peak Value) / Peak Value
```

### SIP Calculation

**Future Value of SIP:**
```python
FV = P × [((1 + r)^n - 1) / r] × (1 + r)

Where:
P = Monthly investment
r = Monthly return rate
n = Number of months
```

## 🎯 Popular Fund Categories

### Equity Funds
- **Large Cap** - Invests in top 100 companies by market cap
- **Mid Cap** - Companies ranked 101-250
- **Small Cap** - Companies ranked 251 onwards
- **Flexi/Multi Cap** - Mix of large, mid, small caps

### Debt Funds
- **Liquid Funds** - Very short term (1-91 days)
- **Ultra Short Duration** - 3-6 months
- **Short Duration** - 1-3 years
- **Medium to Long Duration** - 3+ years

### Hybrid Funds
- **Aggressive Hybrid** - 65-80% equity
- **Conservative Hybrid** - 10-25% equity
- **Balanced Advantage** - Dynamic allocation

### Tax Saving
- **ELSS** - Equity Linked Savings Scheme (3-year lock-in)

### Index Funds
- **Nifty 50** - Tracks Nifty index
- **Sensex** - Tracks Sensex index
- **Nifty Next 50** - Next 50 companies

## 🔍 Examples

### Example 1: Analyzing HDFC Flexi Cap Fund

1. Search: "HDFC Flexi"
2. Select: "HDFC Flexi Cap Fund - Direct Plan - Growth"
3. Period: 5 Years
4. View Returns: Check 3Y CAGR and 5Y CAGR
5. Analyze Risk: Check volatility and max drawdown
6. Plan SIP: Enter ₹10,000/month for 10 years

### Example 2: Comparing Returns

1. Open fund A, note returns
2. Use browser's back button or refresh
3. Select fund B, note returns
4. Compare side by side

### Example 3: SIP Planning

**Goal:** ₹1 Crore in 15 years

1. Go to SIP tab
2. Enter expected return: 12% p.a.
3. Adjust monthly SIP until target is reached
4. Check wealth projection chart

**Result:** ~₹20,000/month needed

## ⚙️ Configuration

### Customize Analysis Period
Edit the `period_map` in `app.py`:
```python
period_map = {
    '1M': 30, 
    '3M': 90, 
    '6M': 180, 
    '1Y': 365, 
    '3Y': 1095, 
    '5Y': 1825, 
    'All': None
}
```

### Adjust Risk-Free Rate
Modify in risk calculation:
```python
risk_free_rate = 0.065  # 6.5% for India (can change to current rate)
```

### Change Theme
Modify Plotly template:
```python
template='plotly_dark'  # Options: plotly, plotly_white, ggplot2, seaborn
```

## 🐛 Troubleshooting

### Issue: "Failed to load funds"
**Solution:**
- Check internet connection
- API might be temporarily down
- Try refreshing the page
- Wait a few minutes and retry

### Issue: "No NAV data available"
**Solution:**
- Fund might be newly launched
- Select a different fund
- Check if fund code is correct

### Issue: Charts not displaying
**Solution:**
```bash
pip install --upgrade plotly streamlit
```

### Issue: Slow performance
**Solution:**
- Select shorter time period (1Y instead of All)
- Close other browser tabs
- Clear Streamlit cache (sidebar refresh)

## 📈 Performance Tips

1. **Use shorter periods** for faster loading (1Y vs All)
2. **Cache is enabled** - switching back to analyzed funds is instant
3. **Limit search results** - First 50 funds shown to avoid lag
4. **Close unused tabs** - Better browser performance

## 🎓 Understanding the Metrics

### What is CAGR?
Compound Annual Growth Rate - The annual rate at which an investment grows. Better than simple returns for multi-year comparisons.

**Good CAGR:**
- Debt Funds: 6-8%
- Hybrid Funds: 8-12%
- Equity Funds: 12-18%

### What is Sharpe Ratio?
Measures risk-adjusted returns. Higher is better.

**Interpretation:**
- < 1: Below average
- 1-2: Good
- 2-3: Very good
- \> 3: Excellent

### What is Maximum Drawdown?
Largest peak-to-trough decline. Shows worst-case loss scenario.

**Interpretation:**
- < 10%: Low risk
- 10-20%: Moderate risk
- 20-30%: High risk
- \> 30%: Very high risk

## 💰 Investment Strategies

### SIP Strategy
**When to use:** Regular income, disciplined investing
**Benefit:** Rupee cost averaging
**Best for:** Long-term goals (5+ years)

**Recommended Amount:**
- Beginners: ₹1,000 - ₹5,000/month
- Intermediate: ₹5,000 - ₹25,000/month
- Advanced: ₹25,000+/month

### Lumpsum Strategy
**When to use:** Windfall, market correction
**Benefit:** Higher exposure to growth
**Best for:** Market timing, extra funds

## 🌟 Best Practices

1. **Diversify** - Don't put all money in one fund
2. **Match Goals** - Equity for long-term, debt for short-term
3. **Review Quarterly** - Check performance every 3 months
4. **Stay Invested** - Don't panic sell during market drops
5. **Tax Planning** - Use ELSS for tax saving under 80C

## 📚 Additional Resources

### Learning
- [AMFI Investor Education](https://www.amfiindia.com/investor-corner)
- [SEBI Investor Awareness](https://investor.sebi.gov.in/)
- [Value Research](https://www.valueresearchonline.com/funds/)

### Tools
- [Moneycontrol MF](https://www.moneycontrol.com/mutual-funds/)
- [ET Money](https://www.etmoney.com/)
- [Groww](https://groww.in/mutual-funds)

### Regulations
- [SEBI](https://www.sebi.gov.in/) - Securities and Exchange Board of India
- [AMFI](https://www.amfiindia.com/) - Association of Mutual Funds in India

## ⚠️ Disclaimer

**IMPORTANT NOTICE:**

This application is for **educational and informational purposes only**. It is NOT investment advice.

- Past performance does NOT guarantee future results
- Mutual fund investments are subject to market risks
- Read all scheme-related documents carefully
- Consult with a SEBI-registered financial advisor
- Creator is not responsible for investment decisions
- Data accuracy depends on third-party API

**Investment Tips:**
- Only invest surplus funds
- Understand your risk tolerance
- Have an emergency fund first
- Don't invest borrowed money
- Diversify across asset classes

## 🤝 Contributing

Suggestions for improvements:
- Multiple fund comparison view
- Export to PDF/Excel
- Email alerts for targets
- Advanced technical indicators
- Fund recommendations based on goals
- Integration with broker APIs

## 📄 License

MIT License - Free to use, modify, and distribute

## 📞 Support

For issues or questions:
1. Check Troubleshooting section
2. Review examples
3. Check API status at mfapi.in
4. Verify internet connection

## 🎉 Version History

**v1.0.0** (Current)
- Initial release
- Real-time NAV tracking
- Returns and risk analysis
- SIP calculator
- Interactive charts

---

## 🚀 Quick Command Reference

```bash
# Install
pip install -r requirements.txt

# Run
streamlit run app.py

# Update dependencies
pip install --upgrade -r requirements.txt

# Clear cache
# Use "Clear Cache" button in Streamlit menu (☰)
```

---

**Made with ❤️ for Indian Investors**

Happy Investing! 📈💰🇮🇳