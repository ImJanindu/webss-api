import os
import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask, request, render_template

app = Flask(__name__)

chrome_options = Options()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<url>')
def ss(url):
    try:
        abc = "https://" + url
        browser.set_window_size(1920, 1080)
        browser.get(abc)
        sleep(2)
        browser.get_screenshot_as_file("static/screenshot.png")
        browser.quit()
        
        return render_template("ss.html")
    except:
        return "Website does not exist!"


if __name__ == "__main__":
    app.run(debug=True)
        
    

