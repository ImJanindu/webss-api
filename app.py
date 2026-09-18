import os
import sys
from time import sleep
from selenium import webdriver
from telegraph import upload_file
from selenium.webdriver.chrome.options import Options
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hemlo!"

@app.route('/<url>')
def ss(url):
    try:
        chrome_options = Options()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        abc = "https://" + url
        browser.set_window_size(1920, 1080)
        browser.get(abc)
        sleep(2)
        browser.get_screenshot_as_file("static/screenshot.png")
        response = upload_file("static/screenshot.png")
        browser.quit()
        return f"https://telegra.ph{response[0]}"
    except Exception as e:
        if 'browser' in locals():
            browser.quit()
        return "None"


if __name__ == "__main__":
    app.run(debug=True)
        
    

