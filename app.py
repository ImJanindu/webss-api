import os
import sys
import uuid
from time import sleep
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify

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
        
        os.makedirs("screenshots", exist_ok=True)
        screenshot_path = f"screenshots/screenshot_{uuid.uuid4().hex}.png"
        browser.get_screenshot_as_file(screenshot_path)
        
        if not os.path.exists(screenshot_path) or os.path.getsize(screenshot_path) == 0:
            raise Exception("Screenshot capture failed or file is empty.")

        with open(screenshot_path, 'rb') as f:
            # Catbox API requires 'reqtype' and 'fileToUpload'
            upload_req = requests.post(
                'https://catbox.moe/user/api.php', 
                data={'reqtype': 'fileupload'},
                files={'fileToUpload': f}
            )
            
        browser.quit()
        
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
        # Catbox returns the direct URL as plain text on success
        if upload_req.status_code == 200 and upload_req.text.startswith("https://"):
            image_url = upload_req.text
        else:
            raise Exception(f"Catbox upload failed: {upload_req.text}")
            
        return jsonify({
            "success": True,
            "url": target_url,
            "image_url": image_url
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
        
    

