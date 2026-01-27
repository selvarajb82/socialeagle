# 💳 Payment XML to Excel Converter

> A Streamlit web app that parses ISO 20022 payment XML files and converts them into beautifully formatted Excel reports with transaction details and summaries.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-FF4B4B.svg)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Latest-150458.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Features](#features)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [XML Structure](#xml-structure)
- [Output Format](#output-format)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgements](#acknowledgements)

---

## 🎯 Overview

This Streamlit application provides a simple, user-friendly interface for converting ISO 20022 payment XML files into structured Excel spreadsheets. Perfect for finance teams, auditors, and developers who need to analyze payment data without manual processing.

**What it does:**
- 📤 Upload payment XML files (`.xml` or `.txt`)
- 🔍 Parse transaction data and group headers
- 📊 Generate summary statistics by Payment Information ID (PPR)
- 💾 Download formatted Excel files with multiple sheets
- 🎨 Apply professional styling with color-coded totals

---

## 💡 Motivation

### The Problem

Working with ISO 20022 payment XML files is challenging:
- ❌ XML is not human-readable for quick analysis
- ❌ Finance teams need Excel for reporting and auditing
- ❌ Manual extraction is time-consuming and error-prone
- ❌ No easy way to get PPR-wise summaries

### The Solution

This tool bridges the gap by:
- ✅ Automatically parsing complex XML structures
- ✅ Extracting all relevant payment fields
- ✅ Calculating summaries and control totals
- ✅ Generating professional Excel reports instantly
- ✅ Providing a web interface - no coding required!

---

## ✨ Features

### Core Functionality
- **🚀 Drag-and-Drop Upload** - Simple file upload interface
- **🔄 Real-time Processing** - Instant parsing and preview
- **📊 Multi-Sheet Excel Export** - Separate sheets for transactions and summaries
- **🎨 Professional Formatting** - Color-coded headers and totals with borders

### Data Extraction
- **💰 Transaction Details** - PPR ID, creditor name, amount, and currency
- **📈 PPR-wise Summaries** - Transaction counts and control sums per payment info
- **📋 Group Header Info** - Total number of transactions and control sum from XML header
- **🧮 Automatic Totals** - Calculated totals for all numeric columns

### Excel Features
- **🎨 Color Coding** - Green headers, yellow totals
- **📐 Auto-sizing** - Columns adjusted to 24-character width
- **🔲 Borders** - Thick borders for all cells
- **📑 Multiple Sheets** - Transactions and Summary in separate tabs
- **🔗 Smart Naming** - Output file named based on input file

---

## 🎬 Demo

### Screenshot Preview

**Upload Interface:**
```
💳 Payment XML to Excel Converter
┌─────────────────────────────────────┐
│  Upload payment XML file            │
│  (.xml or .txt)                     │
│  [Drag and drop file here]          │
└─────────────────────────────────────┘
```

**Output Preview:**

| PPR (PmtInfId) | Creditor Name | Amount | Currency |
|----------------|---------------|--------|----------|
| PPR001         | ABC Corp      | 1000.00| USD      |
| PPR001         | XYZ Ltd       | 2500.00| USD      |
| **TOTAL**      |               | **3500.00** | |

**Summary Table:**

| PPR (PmtInfId) | Number of Transactions | Control Sum |
|----------------|------------------------|-------------|
| PPR001         | 2                      | 3500.00     |
| **TOTAL**      | **2**                  | **3500.00** |

---

## 📦 Prerequisites

Before running this application, ensure you have:

- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **pip** package manager
- **ISO 20022 compliant XML files** (pain.001 format)

### System Requirements:
- **OS**: Windows, macOS, or Linux
- **RAM**: 2GB minimum (4GB+ recommended for large files)
- **Disk Space**: 50MB for dependencies

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/payment-xml-converter.git
cd payment-xml-converter
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
pip install -r requirements.txt
```

**Or install manually:**

```bash
pip install streamlit pandas openpyxl
```

### Step 4: Verify Installation

```bash
streamlit --version
python -c "import pandas; import openpyxl; print('All dependencies installed!')"
```

---

## 💻 Usage

### Running the Application

1. **Start the Streamlit server:**

```bash
streamlit run payment_xml_parsing_excel.py
```

2. **Open your browser** - The app should automatically open at `http://localhost:8501`

3. **Upload your XML file** - Drag and drop or click to browse

4. **Review the data** - Check transactions and summaries in the web interface

5. **Download Excel** - Click the download button to get your formatted report

### Command Line Options

```bash
# Run on a specific port
streamlit run payment_xml_parsing_excel.py --server.port 8080

# Run without auto-opening browser
streamlit run payment_xml_parsing_excel.py --server.headless true

# Enable file watching for development
streamlit run payment_xml_parsing_excel.py --server.fileWatcherType watchdog
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY payment_xml_parsing_excel.py .

EXPOSE 8501

CMD ["streamlit", "run", "payment_xml_parsing_excel.py", "--server.address", "0.0.0.0"]
```

Run with:
```bash
docker build -t payment-xml-converter .
docker run -p 8501:8501 payment-xml-converter
```

---

## 🔍 XML Structure

### Supported XML Format

This tool parses **ISO 20022 pain.001** (Customer Credit Transfer Initiation) XML files.

**Expected structure:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03">
  <CstmrCdtTrfInitn>
    <GrpHdr>
      <NbOfTxs>10</NbOfTxs>
      <CtrlSum>50000.00</CtrlSum>
    </GrpHdr>
    <PmtInf>
      <PmtInfId>PPR001</PmtInfId>
      <CdtTrfTxInf>
        <Amt>
          <InstdAmt Ccy="USD">1000.00</InstdAmt>
        </Amt>
        <Cdtr>
          <Nm>ABC Corporation</Nm>
        </Cdtr>
      </CdtTrfTxInf>
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>
```

### Extracted Fields

| XML Path | Excel Column | Description |
|----------|--------------|-------------|
| `PmtInf/PmtInfId` | PPR (PmtInfId) | Payment Information ID |
| `CdtTrfTxInf/Cdtr/Nm` | Creditor Name | Beneficiary name |
| `CdtTrfTxInf/Amt/InstdAmt` | Amount | Transaction amount |
| `CdtTrfTxInf/Amt/InstdAmt/@Ccy` | Currency | Currency code |
| `GrpHdr/NbOfTxs` | Group Header NbOfTxs | Total transactions |
| `GrpHdr/CtrlSum` | Group Header CtrlSum | Total control sum |

---

## 📤 Output Format

### Excel Structure

The generated Excel file contains **2 sheets**:

#### 1. **Transactions Sheet**
- All individual credit transfer transactions
- Columns: PPR, Creditor Name, Amount, Currency
- TOTAL row at the bottom with sum of amounts

#### 2. **Summary Sheet**
- PPR-wise aggregation
- Columns: PPR, Number of Transactions, Control Sum
- Group Header info below the summary table
- TOTAL rows for both sections

### Styling Applied

```python
# Headers: Green background, bold, thick borders
header_fill = PatternFill("solid", fgColor="C6E0B4")
header_font = Font(bold=True, size=13)

# Totals: Yellow background, bold
total_fill = PatternFill("solid", fgColor="FFF2CC")
total_font = Font(bold=True)

# All cells: Thick borders
border = Border(left/right/top/bottom=Side(style="thick"))

# Columns: 24-character width
```

---

## ⚙️ Configuration

### Customizing the Application

#### Change Page Layout

```python
# In payment_xml_parsing_excel.py, line 9
st.set_page_config(
    page_title="Your Custom Title",
    layout="wide",  # or "centered"
    initial_sidebar_state="expanded"
)
```

#### Adjust Column Widths

```python
# Line 137 - modify this value
sheet.column_dimensions[col[0].column_letter].width = 30  # Change from 24
```

#### Modify Color Scheme

```python
# Lines 120-121 - change hex colors
header_fill = PatternFill("solid", fgColor="4472C4")  # Blue headers
total_fill = PatternFill("solid", fgColor="FFD966")   # Orange totals
```

#### Add More XML Fields

```python
# In the parsing loop (around line 40), add:
debtor = tx.find(".//ns:Dbtr/ns:Nm", ns)
debtor_name = debtor.text if debtor is not None else ""

# Then add to transactions dict:
"Debtor Name": debtor_name,
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 🔴 "Error processing file: no element found"

**Cause:** Invalid XML format or empty file

**Solutions:**
1. Verify XML is well-formed
2. Check file encoding (should be UTF-8)
3. Ensure namespace is correct
4. Try opening in a text editor to validate structure

#### 🔴 "KeyError: 'ns'"

**Cause:** XML namespace not detected properly

**Solution:** Check if your XML has a default namespace:
```python
# The script auto-detects, but you can hardcode:
ns = {"ns": "urn:iso:std:iso:20022:tech:xsd:pain.001.001.03"}
```

#### 🔴 "Module not found: streamlit"

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install streamlit pandas openpyxl
```

#### 🔴 Excel file won't download

**Cause:** Browser blocking download or file size issue

**Solutions:**
1. Check browser's download settings
2. Try a different browser
3. Check available disk space
4. Clear browser cache

#### 🔴 Columns are too narrow/wide

**Solution:** Adjust column width in line 137:
```python
sheet.column_dimensions[col[0].column_letter].width = 20  # Adjust this
```

---

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Multi-file processing** - Batch upload and merge multiple XMLs
- [ ] **CSV export option** - Alternative to Excel for larger files
- [ ] **Advanced filtering** - Filter by date, amount range, or PPR
- [ ] **Data validation** - Check control sums match actual totals
- [ ] **Chart generation** - Visual summaries and graphs
- [ ] **pain.008 support** - Direct debit XML parsing
- [ ] **API endpoint** - REST API for programmatic access
- [ ] **Authentication** - User login and session management
- [ ] **Database storage** - Save parsed data for historical analysis
- [ ] **Email reports** - Automated delivery of Excel files

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** thoroughly with sample XML files
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Contribution Ideas

- Add support for other ISO 20022 message types (pain.002, pain.008, etc.)
- Improve error handling and user feedback
- Add unit tests
- Create sample XML files for testing
- Improve documentation
- Add internationalization (i18n)

### Code Style

Please follow:
- PEP 8 for Python code
- Clear variable names
- Comments for complex logic
- Type hints where appropriate

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com
- Website: [yourwebsite.com](https://yourwebsite.com)

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) - Amazing framework for building data apps
- [Pandas](https://pandas.pydata.org/) - Powerful data manipulation library
- [OpenPyXL](https://openpyxl.readthedocs.io/) - Excel file handling made easy
- [ISO 20022](https://www.iso20022.org/) - International financial messaging standard
- All contributors and users who provide feedback and suggestions

### Helpful Resources

- [ISO 20022 Documentation](https://www.iso20022.org/iso-20022-message-definitions)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)
- [OpenPyXL Styling Guide](https://openpyxl.readthedocs.io/en/stable/styles.html)

---

## 📊 Sample Data

Want to test the application? Here's a minimal valid XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pain.001.001.03">
  <CstmrCdtTrfInitn>
    <GrpHdr>
      <NbOfTxs>2</NbOfTxs>
      <CtrlSum>1500.00</CtrlSum>
    </GrpHdr>
    <PmtInf>
      <PmtInfId>TEST001</PmtInfId>
      <CdtTrfTxInf>
        <Amt><InstdAmt Ccy="USD">1000.00</InstdAmt></Amt>
        <Cdtr><Nm>Test Company A</Nm></Cdtr>
      </CdtTrfTxInf>
      <CdtTrfTxInf>
        <Amt><InstdAmt Ccy="USD">500.00</InstdAmt></Amt>
        <Cdtr><Nm>Test Company B</Nm></Cdtr>
      </CdtTrfTxInf>
    </PmtInf>
  </CstmrCdtTrfInitn>
</Document>
```

Save as `test_payment.xml` and upload to try the application!

---

## 🔒 Security Notes

- **No data stored** - All processing happens in-memory
- **No external requests** - Works completely offline (except Streamlit server)
- **Local deployment** - Runs on your machine, no cloud dependencies
- **File validation** - Only processes .xml and .txt files

**For production use:**
- Consider adding authentication
- Implement rate limiting
- Add audit logging
- Validate XML against XSD schemas
- Scan uploads for malicious content

---

<div align="center">

**⭐ If this tool saved you time, please consider giving it a star! ⭐**

**💼 Finance • 🔄 Automation • 🐍 Python • 📊 Data**

Made with 💙 for the finance community

[Report Bug](https://github.com/yourusername/payment-xml-converter/issues) • [Request Feature](https://github.com/yourusername/payment-xml-converter/issues) • [Documentation](https://github.com/yourusername/payment-xml-converter/wiki)

</div>
