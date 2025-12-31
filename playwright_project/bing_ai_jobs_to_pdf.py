from playwright.sync_api import sync_playwright
import urllib.parse
import os

# 🔍 Search topic
SEARCH_TERM = "How will Artificial Intelligence Affect Jobs 2026-2030"
query = urllib.parse.quote(SEARCH_TERM)

BING_SEARCH_URL = f"https://www.bing.com/search?q={query}"
OUTPUT_PDF = "AI_Jobs_2026_2030.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        slow_mo=50
    )

    context = browser.new_context(
        viewport={"width": 1280, "height": 900},
        locale="en-US"
    )

    page = context.new_page()

    print("🔎 Opening Bing search results...")
    page.goto(BING_SEARCH_URL, timeout=60000)

    # Wait for results
    page.wait_for_selector("li.b_algo h2 a", timeout=15000)

    # 👉 Click FIRST search result
    first_result = page.locator("li.b_algo h2 a").first
    first_link = first_result.get_attribute("href")

    print("➡️ Opening first link:")
    print(first_link)

    page.goto(first_link, timeout=60000)
    page.wait_for_timeout(5000)

    # Clean page for PDF (remove nav/ads if possible)
    page.evaluate("""
        () => {
            const tags = document.querySelectorAll('nav, header, footer, aside');
            tags.forEach(t => t.remove());
            document.body.style.margin = '40px';
            document.body.style.fontSize = '14px';
            document.body.style.lineHeight = '1.6';
        }
    """)

    print("📄 Generating PDF...")
    page.pdf(
        path=OUTPUT_PDF,
        format="A4",
        print_background=True,
        margin={
            "top": "20mm",
            "bottom": "20mm",
            "left": "20mm",
            "right": "20mm",
        }
    )

    print(f"\n✅ PDF created successfully: {os.path.abspath(OUTPUT_PDF)}")

    browser.close()
