# 🚀 Session Audit System - Deployment Guide

## Quick Start (5-minute setup)

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
streamlit run main.py
```

### 3. Access the Application
- Open browser to: `http://localhost:8501`
- Navigate to **Admin Panel** > **Database Settings**
- Configure Google Sheets connection

---

## 📋 Google Sheets Setup

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable **Google Sheets API**

### Step 2: Create Service Account
1. Navigate to **IAM & Admin** > **Service Accounts**
2. Click **Create Service Account**
3. Enter name: `session-audit-service`
4. Skip role assignment (for now)
5. Click **Done**

### Step 3: Generate Credentials
1. Click on created service account
2. Go to **Keys** tab
3. Click **Add Key** > **Create New Key**
4. Select **JSON** format
5. Download and save the JSON file

### Step 4: Prepare Google Sheet
1. Create new Google Sheets document
2. Name it: `Session Audits Database`
3. Share with service account email (from JSON file)
4. Give **Editor** permissions
5. Copy the sheet URL

---

## 🔧 Application Configuration

### In Admin Panel:
1. **Navigate to Admin Panel** > **Database Settings**
2. **Paste JSON credentials** in the text area
3. **Enter Google Sheets URL**
4. **Set worksheet name** (default: "Session_Audits")
5. **Click "Test Connection"**

### Verify Setup:
- ✅ Connection successful message
- ✅ Green status indicator
- ✅ Statistics showing in sidebar

---

## 🌐 Streamlit Cloud Deployment

### Step 1: Prepare Repository
```bash
# If using Git
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **New app**
4. Select your repository
5. Set main file: `main.py`
6. Click **Deploy**

### Step 3: Configure Secrets
1. In Streamlit Cloud app settings
2. Go to **Secrets** section
3. Add your credentials:

```toml
# Streamlit secrets format
GOOGLE_CREDENTIALS_JSON = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR-PRIVATE-KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@project.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40project.iam.gserviceaccount.com"
}
'''

GOOGLE_SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/your-spreadsheet-id/edit"
```

### Step 4: Update Code for Production
Update `database.py` to use Streamlit secrets:

```python
# Add this to database.py __init__ method
def initialize_connection_from_secrets(self):
    """Initialize connection using Streamlit secrets"""
    try:
        credentials_json = st.secrets["GOOGLE_CREDENTIALS_JSON"]
        spreadsheet_url = st.secrets["GOOGLE_SPREADSHEET_URL"]
        worksheet_name = st.secrets.get("GOOGLE_WORKSHEET_NAME", "Session_Audits")
        
        return self.initialize_connection(credentials_json, spreadsheet_url, worksheet_name)
    except Exception as e:
        st.error(f"Error loading secrets: {str(e)}")
        return False
```

---

## 🛡️ Security Best Practices

### 1. Credentials Management
- ✅ Never commit credentials to Git
- ✅ Use Streamlit secrets for production
- ✅ Regularly rotate service account keys
- ✅ Limit service account permissions

### 2. Sheet Access Control
- ✅ Share sheet only with service account
- ✅ Use "Editor" permissions (not "Owner")
- ✅ Monitor sheet access logs
- ✅ Regular backup of data

### 3. Application Security
- ✅ Validate all form inputs
- ✅ Sanitize data before saving
- ✅ Monitor for unusual activity
- ✅ Regular dependency updates

---

## 📊 Usage Guidelines

### For Auditors:
1. **Complete all required fields** (marked with *)
2. **Be consistent with dropdown selections**
3. **Provide detailed comments** when necessary
4. **Verify data before submission**

### For Administrators:
1. **Regularly backup Google Sheets data**
2. **Monitor system statistics**
3. **Update field configurations as needed**
4. **Review and export data monthly**

### For IT Support:
1. **Monitor application logs**
2. **Check Google Sheets API quotas**
3. **Maintain service account credentials**
4. **Update dependencies regularly**

---

## 🔍 Troubleshooting

### Common Issues:

#### "Connection Failed" Error
- ✅ Check service account credentials
- ✅ Verify sheet sharing permissions
- ✅ Ensure Sheets API is enabled
- ✅ Check internet connectivity

#### "Invalid JSON" Error
- ✅ Verify JSON format is correct
- ✅ Check for extra characters/spaces
- ✅ Re-download credentials if needed

#### "Quota Exceeded" Error
- ✅ Check Google Sheets API quotas
- ✅ Implement caching if needed
- ✅ Consider upgrading Google Cloud plan

#### Form Validation Errors
- ✅ Check required field configurations
- ✅ Verify dropdown options match
- ✅ Review field naming consistency

---

## 📈 Performance Optimization

### For Large Datasets:
1. **Enable caching** for sheet data
2. **Implement pagination** for data viewer
3. **Use batch operations** when possible
4. **Regular data archiving**

### For High Traffic:
1. **Monitor response times**
2. **Consider load balancing**
3. **Implement rate limiting**
4. **Cache computed scores**

---

## 🆘 Support

### Self-Help Resources:
- 📖 Read full `README.md`
- 🔍 Check application logs
- 💬 Review error messages carefully
- 🧪 Test with minimal data first

### Escalation:
- Document exact error messages
- Include steps to reproduce
- Provide system configuration details
- Share relevant log excerpts

---

**🎉 Your Session Audit System is ready for production use!**

**Built with ❤️ using Streamlit, Google Sheets API, and modern web technologies.**
