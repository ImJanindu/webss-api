import os
import sys
import io
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "success": True, 
        "message": "WebSS-API is running!"
    })

@app.route('/<path:url>')
def take_screenshot(url):
    try:
        chrome_options = Options()
        if os.environ.get("GOOGLE_CHROME_BIN"):
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        
        browser = webdriver.Chrome(options=chrome_options)

        if url.startswith("http://") or url.startswith("https://"):
            target_url = url
        else:
            target_url = "https://" + url
            
        browser.set_window_size(1920, 1080)
        browser.get(target_url)
        sleep(2)
        
        # Capture screenshot directly to memory
        image_data = browser.get_screenshot_as_png()
        browser.quit()
        
        # Return the raw image file directly to the user
        return send_file(
            io.BytesIO(image_data),
            mimetype='image/png'
        )

    except Exception as e:
        if 'browser' in locals():
            browser.quit()
            
        return jsonify({
            "success": False,
            "error": "Failed to capture screenshot.",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
        
    

