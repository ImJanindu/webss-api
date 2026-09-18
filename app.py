import os
import sys
import uuid
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from telegraph import upload_file
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "success": True, 
        "message": "WebSS-API is running!"
    })

@app.route('/<url>')
def take_screenshot(url):
    try:
        chrome_options = Options()
        if os.environ.get("GOOGLE_CHROME_BIN"):
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        
        service = Service(ChromeDriverManager().install())
        browser = webdriver.Chrome(service=service, options=chrome_options)

        target_url = "https://" + url
        browser.set_window_size(1920, 1080)
        browser.get(target_url)
        sleep(2)
        
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/screenshot_{uuid.uuid4().hex}.png"
        browser.get_screenshot_as_file(screenshot_path)
        
        telegraph_response = upload_file(screenshot_path)
        browser.quit()
        
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
        return jsonify({
            "success": True,
            "url": target_url,
            "image_url": f"https://telegra.ph{telegraph_response[0]}"
        }), 200

    except Exception as e:
        if 'browser' in locals():
            browser.quit()
        if 'screenshot_path' in locals() and os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
        return jsonify({
            "success": False,
            "error": "Failed to capture screenshot or upload image.",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
        
    

