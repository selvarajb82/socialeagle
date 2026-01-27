# ☕ Google Maps Coffee Shop Scraper

> An automated Python scraper that extracts coffee shop data from Google Maps and exports it to a beautifully formatted Excel file.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev/python/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output](#output)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgements](#acknowledgements)

---

## 🎯 Overview

Finding and comparing local coffee shops can be time-consuming when you're scrolling through Google Maps manually. This scraper automates the entire process, extracting detailed information about coffee shops in a specific area and organizing it into a professional Excel spreadsheet for easy analysis and comparison.

**Perfect for:**
- 🏢 Market research and competitive analysis
- 📊 Location-based business planning
- ☕ Coffee enthusiasts exploring new spots
- 📝 Content creators building local guides

---

## ✨ Features

- **🤖 Automated Scraping** - Uses Playwright to navigate Google Maps and extract data without manual intervention
- **📊 Rich Data Extraction** - Captures name, rating, reviews, price range, category, address, hours, services, and URLs
- **🎨 Formatted Excel Output** - Professional spreadsheet with styling, hyperlinks, and freeze panes
- **📈 Statistics Summary** - Calculates average ratings and identifies top-rated establishments
- **🔄 Smart Scrolling** - Automatically loads more results for comprehensive data collection
- **💎 Clean Data Structure** - Organized columns with proper formatting for immediate use

---

## 🎬 Demo

The scraper runs in a visible browser window so you can watch the magic happen:

```
🌐 Loading Google Maps...
🔍 Searching for coffee shops...
⏳ Waiting for results...
📜 Scrolling to load more results...
   Scroll 1/5
   Scroll 2/5
   ...
✅ Found 20 results

1. 🏪 Cafe Coffee Day
   ⭐ 4.2 (500 reviews) | 💰 ₹₹
   🪙 Coffee shop
   📍 GST Road, Chrompet
   🕐 Open ⋅ Closes 11 PM
   🍽️ Dine-in, Takeaway, Delivery
   🔗 https://maps.google.com/...
```

---

## 📦 Prerequisites

Before running this scraper, ensure you have:

- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **pip** package manager
- **Internet connection** for accessing Google Maps
- **Basic command line knowledge**

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/coffee-shop-scraper.git
cd coffee-shop-scraper
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install playwright openpyxl
```

### Step 4: Install Playwright Browsers

```bash
playwright install chromium
```

---

## 💻 Usage

### Basic Usage

Simply run the script with default settings:

```bash
python coffee_shop_chrompet.py
```

The scraper will:
1. Open Google Maps in a browser
2. Search for "coffee shops near GST Road Chrompet"
3. Scroll to load multiple results
4. Extract detailed information
5. Save data to `coffee_shops_chrompet.xlsx`
6. Display statistics in the terminal

### Custom Search Location

To search a different location, edit the `SEARCH_TEXT` variable in the script:

```python
SEARCH_TEXT = "coffee shops near [Your Location]"
```

Examples:
```python
SEARCH_TEXT = "coffee shops near Times Square New York"
SEARCH_TEXT = "cafes in downtown Seattle"
SEARCH_TEXT = "coffee near Marina Beach Chennai"
```

### Run in Headless Mode

For faster execution without a visible browser, modify line 12:

```python
browser = p.chromium.launch(headless=True)  # Change False to True
```

---

## ⚙️ Configuration

### Adjustable Parameters

| Parameter | Location | Default | Description |
|-----------|----------|---------|-------------|
| `SEARCH_TEXT` | Line 6 | `"coffee shops near GST Road Chrompet"` | Search query for Google Maps |
| `headless` | Line 11 | `False` | Set to `True` to run without browser UI |
| Scroll count | Line 27 | `5` | Number of scrolls to load more results |
| Wait timeout | Various | `2000-7000ms` | Adjust for slower connections |

### Excel Output Customization

Modify the `create_excel()` function to customize:
- Column widths (line 247-259)
- Header colors (line 216-217)
- Border styles (line 221-226)
- Font sizes and colors

---

## 📤 Output

### Excel File Structure

The generated `coffee_shops_chrompet.xlsx` includes:

| Column | Description | Example |
|--------|-------------|---------|
| S.No | Serial number | 1, 2, 3... |
| Name | Business name | Cafe Coffee Day |
| Rating | Star rating | 4.2 |
| Reviews | Number of reviews | 500 |
| Price | Price range | ₹₹ |
| Category | Business type | Coffee shop |
| Address | Street address | GST Road, Chrompet |
| Hours | Operating hours | Open ⋅ Closes 11 PM |
| Services | Available services | Dine-in, Takeaway |
| URL | Google Maps link | Clickable hyperlink |

### Sample Statistics Output

```
📈 Average Rating: 4.15 ⭐
🏆 Highest Rated: Starbucks Coffee (4.8⭐)
```

---

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Multi-location batch processing** - Scrape multiple areas in one run
- [ ] **Phone number extraction** - Add contact information to output
- [ ] **Price range analysis** - Statistical breakdown by price tier
- [ ] **Map visualization** - Generate location heatmaps
- [ ] **CSV export option** - Alternative to Excel format
- [ ] **Command-line arguments** - Customize search without editing code
- [ ] **Error recovery** - Retry failed extractions automatically
- [ ] **Duplicate detection** - Filter out repeated entries

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

Please ensure your code follows PEP 8 style guidelines and includes appropriate comments.

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Note:** This tool is for educational and research purposes. Please respect Google Maps' Terms of Service and use responsibly. Consider rate limiting and avoid excessive requests.

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgements

- [Playwright](https://playwright.dev/) - Reliable web automation framework
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel file manipulation library
- [Google Maps](https://maps.google.com/) - Data source for local business information
- Coffee shop owners everywhere ☕ - For keeping us caffeinated!

---

## ⚠️ Disclaimer

This tool is provided for educational purposes. Web scraping may violate the Terms of Service of some websites. Always:
- Check the website's `robots.txt` and Terms of Service
- Implement reasonable rate limiting
- Respect server resources
- Use official APIs when available

**Use this tool responsibly and ethically.**

---

<div align="center">

**⭐ If this project helped you, please consider giving it a star! ⭐**

Made with ❤️ and ☕

</div>
