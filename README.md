# 🐍 DirtHub API (Python/Flask) Project Checklist

Welcome to the DirtHub API backend! This Python (Flask) application provides calculation endpoints for use by the DirtHub frontend. For frontend setup and user-facing features, see the [DirtHub Frontend README](https://github.com/Zeke142/DirtHub-V4.1).

---

## Project Checklist

- [ ] **README.md** clearly explains:
  - API purpose & features
  - How to run locally (`python app.py`)
  - Required environment variables (with examples)
  - How to deploy to Railway or other cloud
  - API endpoint documentation with example requests
  - How to enable CORS for frontend integration
  - How to update API URLs in frontend (see Frontend README)
- [ ] Add or update `LICENSE`
- [ ] `.gitignore` ignores virtualenvs, pycache, credentials
- [ ] All dependencies listed in `requirements.txt`
- [ ] Add logging and error handling as needed
- [ ] Test endpoints with sample requests (curl/Postman)
- [ ] Enable CORS (`flask_cors`)
- [ ] Link to [frontend repo](https://github.com/Zeke142/DirtHub-V4.1)

---
# 🐍 DirtHub API (Python/Flask)

This repository contains the backend API for DirtHub. It exposes endpoints for slope and vertical curve calculations. The API is designed for integration with the DirtHub frontend ([Flutter repo](https://github.com/Zeke142/DirtHub-V4.1)).

---

## 🚦 API Purpose & Features

- Provides engineering calculation endpoints for slope, grade, and vertical curve problems.
- Accepts JSON input, returns results as JSON.
- Designed for integration with web or mobile frontends (e.g., Flutter).

**Features:**
- Calculate elevations at specified stations given initial elevation and grade.
- Modular: New calculation endpoints can be added as the project grows.
- CORS-enabled for safe cross-origin requests.

---

## 🛠️ Running Locally

1. **Clone this repository:**
    ```sh
    git clone https://github.com/Zeke142/dh-vertical-curve-calculator.git
    cd dh-vertical-curve-calculator
    ```
2. **Install dependencies:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3. **Set environment variables:**  
   Create a `.env` file (optional, for secrets/configs). Example variables are listed below.
4. **Run the app:**
    ```sh
    python app.py
    ```
5. **The API will be available at:**  
   [http://localhost:8080/](http://localhost:8080/)

---

## 🗝️ Required Environment Variables

Most simple APIs only need a port, but you can extend with DB/API keys.  
Example `.env` file:
---

**For frontend integration, user interface, and next steps, please refer to the [DirtHub Frontend README](https://github.com/Zeke142/DirtHub-V4.1).**


# DirtHub Vertical Curve Designer

This is a Streamlit tool designed for engineers working on road and grading projects. It allows both grade-based and elevation-based vertical curve design, including real-time elevation lookups and profile visualization.

## Features
- Supports elevation- and grade-based input modes
- Computes K-values and curve properties
- Altair-powered vertical curve graph
- Point lookup tool for elevation at any station
- Email capture for beta waitlist

## How to Run

1. Clone the repository: