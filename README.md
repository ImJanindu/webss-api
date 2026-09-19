# WebSS-API 📸

A high-performance, lightweight REST API built with Flask and Selenium that takes full-page screenshots of any given website URL and directly returns the image.

## ✨ Features
- **Headless Chrome Automation:** Uses Selenium to render JavaScript-heavy websites before capturing.
- **In-Memory Capture:** Captures and processes screenshots directly in memory without writing to disk, ensuring fast response times and zero disk exhaustion.
- **Direct Image Response:** The API returns the raw `image/png` file seamlessly to the client.
- **JSON API Responses:** Clean, standard JSON formatting for errors (500).

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

## ☁️ AWS Deployment Guide (EC2 via Docker)

If you are deploying this to an Amazon EC2 instance, you can use Docker to easily run the application without manually configuring Python and Google Chrome.

### 1. Install System Dependencies & Docker
Connect to your EC2 instance via SSH and run:
```bash
sudo apt update -y
sudo apt install -y docker.io git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ubuntu
```
*(You may need to log out and log back in or run `newgrp docker` for the docker group permissions to apply.)*

### 2. Setup Your Project & Run
```bash
git clone https://github.com/imjanindu/webss-api.git
cd webss-api
docker build -t webss-api .
docker run -d -p 80:5000 --name webss-container webss-api
```

Your API will now be accessible directly via your EC2 instance's public IP address or domain on port 80.

---

## 👨‍💻 Developer Info

Created and maintained by [ImJanindu](https://github.com/ImJanindu). 
Feel free to open issues or pull requests to improve the API!