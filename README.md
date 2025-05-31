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