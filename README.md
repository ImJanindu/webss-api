# WebSS-API 📸

A high-performance, lightweight REST API built with Flask and Selenium that takes full-page screenshots of any given website URL and automatically uploads them to Telegraph (telegra.ph).

## ✨ Features
- **Headless Chrome Automation:** Uses Selenium to render JavaScript-heavy websites before capturing.
- **Auto Driver Management:** Integrated with `webdriver-manager` so you never have to manually download ChromeDriver again.
- **Concurrent Request Safe:** Generates unique `uuid` filenames for every screenshot and cleans them up from the disk immediately after upload to prevent space exhaustion.
- **JSON API Responses:** Clean, standard JSON formatting with HTTP status codes for success (200) and error (500).

---

## 🚀 Example Usage

To take a screenshot of a website, simply append the target URL to your API's root address. The API automatically handles URLs with or without `https://`.

**Request:**
```http
GET http://localhost:5000/google.com
```

**Response (Success - 200 OK):**
The API will directly return the raw `image/png` file. The image will render seamlessly in your browser, frontend application, or HTML `<img>` tag.

**Response (Error - 500 Internal Server Error):**
```json
{
  "success": false,
  "error": "Failed to capture screenshot.",
  "details": "..."
}
```

---

## 🛠️ Local Setup Instructions

You can run this project locally using **Docker** (recommended) or a standard Python environment.

### Option A: Using Docker (Recommended)
Docker handles all system dependencies (like Google Chrome) automatically so you don't have to install them on your machine.

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/webss-api.git
   cd webss-api
   ```
2. **Build the Docker Image:**
   ```bash
   docker build -t webss-api .
   ```
3. **Run the Container:**
   ```bash
   docker run -d -p 5000:5000 --name webss-container webss-api
   ```
   The API will be available at `http://localhost:5000`.

### Option B: Using Python (Standard)

1. **Install Python and Google Chrome:** Ensure you have Python 3 and the Google Chrome browser installed on your computer.
2. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/webss-api.git
   cd webss-api
   ```
3. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the API:**
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000`.

---

## ☁️ AWS Deployment Guide (Amazon Linux 2 / 2023)

If you are deploying this to an Amazon Linux EC2 instance, follow these steps. Amazon Linux uses `yum`/`dnf` instead of `apt`.

### 1. Install System Dependencies & Google Chrome
Connect to your EC2 instance via SSH and run:
```bash
sudo yum update -y
sudo yum install -y git python3 python3-pip nginx wget
```

Install the Google Chrome browser via the official RPM package:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
sudo yum install -y ./google-chrome-stable_current_x86_64.rpm
```

### 2. Setup Your Project
```bash
git clone https://github.com/your-username/webss-api.git
cd webss-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Create a Systemd Service for Gunicorn
Run `sudo nano /etc/systemd/system/webss.service` and paste:
```ini
[Unit]
Description=Gunicorn instance to serve webss-api
After=network.target

[Service]
User=ec2-user
Group=ec2-user
WorkingDirectory=/home/ec2-user/webss-api
Environment="PATH=/home/ec2-user/webss-api/venv/bin"
ExecStart=/home/ec2-user/webss-api/venv/bin/gunicorn --workers 3 --bind unix:webss.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```
Start and enable the service:
```bash
sudo systemctl start webss
sudo systemctl enable webss
```

### 4. Configure Nginx as a Reverse Proxy
Run `sudo nano /etc/nginx/conf.d/webss.conf` and paste:
```nginx
server {
    listen 80;
    server_name your_ec2_public_ip;

    location / {
        proxy_pass http://unix:/home/ec2-user/webss-api/webss.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Restart Nginx:
```bash
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## 👨‍💻 Developer Info

Created and maintained by [ImJanindu](https://github.com/ImJanindu). 
Feel free to open issues or pull requests to improve the API!