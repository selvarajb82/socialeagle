# 🤖 YouTube Auto-Subscribe Bot

> Automate YouTube channel subscriptions using Python and PyAutoGUI - because clicking Subscribe manually is so 2010.

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-Latest-green.svg)](https://pyautogui.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Motivation](#motivation)
- [Features](#features)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Disclaimer](#disclaimer)

---

## 🎯 Overview

This Python automation script uses PyAutoGUI to automatically navigate to YouTube, search for a specific channel, and click the Subscribe button - all without you lifting a finger (after running the script, of course).

**Perfect for:**
- 🧪 Learning GUI automation with Python
- 🎓 Educational demonstrations of PyAutoGUI
- 🤖 Understanding image recognition in automation
- 🛠️ Building more complex browser automation workflows

---

## 💡 Motivation

Ever wanted to learn how GUI automation works? This project demonstrates:
- **Real-world automation** - Automating repetitive web tasks
- **Image recognition** - Using screenshots to locate elements on screen
- **Keyboard shortcuts** - Leveraging browser hotkeys for reliability
- **Error handling** - Gracefully managing when elements aren't found

While YouTube's official API is the recommended way for production applications, this project showcases the power and limitations of GUI automation for educational purposes.

---

## ✨ Features

- **🔍 Smart Search** - Automatically navigates to YouTube and searches for channels
- **🖼️ Image Recognition** - Uses screenshot matching to find channel logos and buttons
- **⌨️ Keyboard Shortcuts** - Leverages YouTube hotkeys for reliable navigation
- **🎯 Fallback Methods** - Multiple strategies to locate the Subscribe button
- **💬 Interactive Prompt** - Enter channel name through a GUI dialog
- **🔄 Browser Focus Management** - Automatically handles window focus for smooth operation

---

## 🎬 Demo

### What the Script Does:

1. Prompts you for a channel name
2. Opens a new browser tab
3. Navigates to YouTube
4. Searches for the channel
5. Clicks on the channel (using image recognition)
6. Locates and clicks the Subscribe button

```
📝 Enter channel name: "Thiru_with_AI"
🌐 Opening YouTube...
🔍 Searching for channel...
🎯 Channel found! Clicking...
✅ Subscribe button clicked!
```

---

## 📦 Prerequisites

Before running this script, ensure you have:

- **Python 3.7+** installed ([Download here](https://www.python.org/downloads/))
- **pip** package manager
- **A web browser** (Chrome, Firefox, Edge, etc.)
- **Screenshot images** of:
  - Target channel logo (`Thiru_with_AI.png`)
  - Subscribe button (`Subscribe2.png`)
- **Basic Python knowledge**

### System Requirements:

- **Windows**: Fully supported
- **macOS**: Supported (may need accessibility permissions)
- **Linux**: Supported (requires `scrot` or `gnome-screenshot`)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/youtube-auto-subscribe.git
cd youtube-auto-subscribe
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
pip install pyautogui
```

**Additional requirements for screenshots:**

```bash
# For better image recognition (optional but recommended)
pip install opencv-python pillow
```

---

## 🔧 Setup

### 1. Take Screenshot Images

You need to capture screenshots of specific UI elements:

#### **Channel Logo** (`Thiru_with_AI.png`)
1. Open YouTube and search for your target channel
2. Take a screenshot of the channel logo/thumbnail in search results
3. Crop to just the logo area
4. Save as `Thiru_with_AI.png` in the script directory

#### **Subscribe Button** (`Subscribe2.png`)
1. Navigate to a channel page
2. Take a screenshot of the Subscribe button
3. Crop to just the button
4. Save as `Subscribe2.png` in the script directory

### 2. Configure Channel Name

The script will prompt you for the channel name, but you can also hardcode it:

```python
# Replace the prompt line with:
channel_name = "Your Channel Name"
```

### 3. Adjust Confidence Levels (if needed)

If image recognition fails, adjust confidence values in the script:

```python
# Lower confidence = more lenient matching (0.0 to 1.0)
channel = pyautogui.locateCenterOnScreen("Thiru_with_AI.png", confidence=0.5)
subscribe2 = pyautogui.locateCenterOnScreen("Subscribe2.png", confidence=0.7)
```

---

## 💻 Usage

### Basic Usage

1. **Open your web browser** (ensure it's visible on screen)
2. **Run the script:**

```bash
python youtube_subscribe_pyautogui.py
```

3. **Enter the channel name** when prompted
4. **Don't touch your keyboard/mouse** - let the automation run!

### Advanced Usage

#### Running with Custom Channel

Edit the script to skip the prompt:

```python
# Line 60 - replace prompt with hardcoded name
channel_name = "Fireship"
print(channel_name)
```

#### Batch Subscribe to Multiple Channels

Create a loop version:

```python
channels = ["Channel1", "Channel2", "Channel3"]

for channel in channels:
    # Run automation for each channel
    # Add delays between runs
    time.sleep(10)
```

---

## 🔍 How It Works

### Step-by-Step Breakdown

```python
# 1. Get channel name from user
channel_name = pyautogui.prompt(text="", title="enter the channel name")

# 2. Focus browser and open new tab
pyautogui.hotkey("ctrl", "t")

# 3. Navigate to YouTube
pyautogui.write("https://www.youtube.com/")
pyautogui.hotkey("enter")

# 4. Use YouTube's search shortcut
pyautogui.press("/")  # Focus search box
pyautogui.write(channel_name)
pyautogui.hotkey("enter")

# 5. Find channel using image recognition
channel = pyautogui.locateCenterOnScreen("Thiru_with_AI.png", confidence=0.5)
pyautogui.moveTo(channel, duration=1)
pyautogui.click()

# 6. Locate and click Subscribe button
subscribe2 = pyautogui.locateCenterOnScreen("Subscribe2.png", confidence=0.7)
pyautogui.moveTo(subscribe2, duration=1)
pyautogui.click()
```

### Key Techniques Used

- **`pyautogui.hotkey()`** - Simulates keyboard shortcuts
- **`pyautogui.locateCenterOnScreen()`** - Finds images on screen
- **`pyautogui.moveTo()`** - Moves mouse to coordinates
- **`pyautogui.click()`** - Simulates mouse clicks
- **`time.sleep()`** - Adds delays for page loading

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 🔴 "Channel image not found"

**Cause:** Image recognition failed to locate the channel logo

**Solutions:**
1. Retake screenshot with exact screen resolution
2. Lower confidence level: `confidence=0.3`
3. Use grayscale: `grayscale=True`
4. Check image file is in same directory

```python
# Try this adjustment
channel = pyautogui.locateCenterOnScreen(
    "Thiru_with_AI.png", 
    confidence=0.3,
    grayscale=True
)
```

#### 🔴 "Subscribe button not found"

**Cause:** Button appearance changed or not visible

**Solutions:**
1. Scroll to ensure button is visible
2. Take new screenshot of Subscribe button
3. Script includes fallback Tab navigation method

#### 🔴 Script runs too fast

**Cause:** Network latency or slow page loading

**Solution:** Increase sleep timers:

```python
# Change this (line 87)
pyautogui.sleep(5)  # Increase from 5 to 10 seconds

# And this (line 108)
time.sleep(3)  # Increase from 3 to 5 seconds
```

#### 🔴 Wrong element clicked

**Cause:** Multiple similar images on screen

**Solution:** Take more specific screenshots with unique features

#### 🔴 macOS Permission Issues

**Solution:** Grant accessibility permissions:
1. System Preferences → Security & Privacy → Privacy
2. Select "Accessibility"
3. Add Terminal/Python to allowed apps

---

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Multi-channel batch processing** - Subscribe to a list from CSV/TXT
- [ ] **Error logging** - Save failed attempts to log file
- [ ] **GUI interface** - Add Tkinter interface for easier use
- [ ] **Video tutorial** - Step-by-step setup guide
- [ ] **Cross-browser support** - Specific optimizations for Chrome/Firefox
- [ ] **Notification bell click** - Also enable notifications after subscribing
- [ ] **Unsubscribe mode** - Reverse operation for cleanup
- [ ] **Selenium migration** - More reliable alternative to PyAutoGUI

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Ideas for Contributions:
- Add support for other video platforms
- Improve image recognition accuracy
- Create cross-platform compatibility fixes
- Add comprehensive error handling
- Write unit tests

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- YouTube: [Your Channel](https://youtube.com/@yourchannel)
- Email: your.email@example.com

---

## 🙏 Acknowledgements

- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Python GUI automation library
- [Pillow](https://pillow.readthedocs.io/) - Python Imaging Library
- [OpenCV](https://opencv.org/) - Computer vision library for image recognition
- YouTube - For providing keyboard shortcuts that make automation easier

---

## ⚠️ Disclaimer

**IMPORTANT - READ BEFORE USE:**

### Educational Purpose Only
This project is created for **educational purposes** to demonstrate GUI automation concepts. It is NOT intended for:
- ❌ Spam or artificial engagement
- ❌ Violating YouTube's Terms of Service
- ❌ Mass automation of subscriptions
- ❌ Commercial use without proper authorization

### Legal Considerations
- **YouTube's Terms of Service** prohibit automated interaction at scale
- **Bot detection** may flag suspicious activity
- **Account suspension** risk if misused
- **Use responsibly** and respect platform policies

### Recommended Alternatives
For production use, consider:
- **YouTube Data API v3** - Official, reliable, and compliant
- **Selenium WebDriver** - More robust browser automation
- **Manual subscriptions** - Always the safest option

### Use at Your Own Risk
The author assumes no responsibility for:
- Account suspensions or bans
- Violations of Terms of Service
- Any damages resulting from use of this script

**This tool is provided AS-IS for learning purposes only.**

---

## 🎓 Learning Resources

Want to learn more about GUI automation?

- [PyAutoGUI Documentation](https://pyautogui.readthedocs.io/)
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Selenium Python Tutorial](https://selenium-python.readthedocs.io/)

---

<div align="center">

**⭐ If this project helped you learn something new, please consider giving it a star! ⭐**

**👍 Educational • 🤖 Automation • 🐍 Python**

Made for learning purposes with 💻 and ☕

</div>
