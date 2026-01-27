import subprocess
import sys
import os
import webbrowser
import time


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(base_path, "concur_split_logic.py")

    # Start Streamlit as a subprocess
    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            app_path,
            "--server.port=8501",
            "--server.headless=true",
            "--browser.gatherUsageStats=false"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Give server time to start
    time.sleep(3)

    # Open browser
    webbrowser.open("http://localhost:8501")


if __name__ == "__main__":
    main()
