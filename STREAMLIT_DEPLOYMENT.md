# 🚀 Streamlit Cloud Deployment Guide

## 📋 Prerequisites

1. **GitHub Repository**: Your code is on GitHub
2. **Streamlit Cloud Account**: Sign up at https://share.streamlit.io
3. **Google Sheets Setup**: Service account with access to your Sheet

## 🎯 Step-by-Step Deployment

### Step 1: Access Streamlit Cloud
1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"

### Step 2: Connect Your Repository
1. **Repository**: Select your `Physical-Form` repo
2. **Branch**: `main`
3. **Main file path**: `streamlit_app.py`

### Step 3: Configure Secrets
Click "Advanced settings" and add these secrets (use your real values):

```toml
[secrets]
# Paste the FULL JSON of your service account here as a single line string
GOOGLE_SHEETS_CREDENTIALS = "{\"type\":\"service_account\",\"project_id\":\"<project-id>\",\"private_key_id\":\"<key-id>\",\"private_key\":\"-----BEGIN PRIVATE KEY-----\\n<redacted>\\n-----END PRIVATE KEY-----\\n\",\"client_email\":\"<service-account>@<project>.iam.gserviceaccount.com\",\"client_id\":\"<client-id>\",\"auth_uri\":\"https://accounts.google.com/o/oauth2/auth\",\"token_uri\":\"https://oauth2.googleapis.com/token\",\"auth_provider_x509_cert_url\":\"https://www.googleapis.com/oauth2/v1/certs\",\"client_x509_cert_url\":\"https://www.googleapis.com/robot/v1/metadata/x509/<service-account>%40<project>.iam.gserviceaccount.com\"}"

GOOGLE_SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/<your-sheet-id>/edit"
GOOGLE_WORKSHEET_NAME = "Session_Audits"
```

### Step 4: Deploy
1. Click "Deploy"
2. Wait for build
3. App will be live at the provided URL

## 🔧 Configuration Details
- App auto-initializes Google Sheets via secrets
- You can also configure manually in Admin Panel

## 📁 File Structure
```
Physical-Form/
├── streamlit_app.py
├── main.py
├── config.py
├── scoring.py
├── database.py
├── requirements.txt
└── .streamlit/config.toml
```

## 🛠️ Troubleshooting
- Ensure secrets are valid JSON (use a JSON validator)
- Sheet must be shared with the service account email (Editor)
- Check Streamlit logs if the app fails to connect

## ✅ Done
Your Session Audit System is ready for Streamlit Cloud.
