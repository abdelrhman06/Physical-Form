"""
Google Sheets database integration for Session Audit Form
Handles reading from and writing to Google Sheets
"""

import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

class GoogleSheetsDB:
    def __init__(self):
        self.client = None
        self.sheet = None
        self.worksheet = None
        
    def initialize_connection(self, credentials_json: str, spreadsheet_url: str, worksheet_name: str = "Session_Audits"):
        """Initialize Google Sheets connection - DEPRECATED: Use initialize_connection_from_dict instead"""
        try:
            credentials_dict = json.loads(credentials_json)
            return self.initialize_connection_from_dict(credentials_dict, spreadsheet_url, worksheet_name)
        except Exception as e:
            st.error(f"❌ Error parsing credentials: {str(e)}")
            return False
    
    def initialize_connection_from_secrets(self) -> bool:
        """Initialize connection using Streamlit secrets. Returns True on success."""
        try:
            st.info("🔍 Checking Streamlit secrets...")
            
            # Check if using TOML sections format
            if hasattr(st.secrets, 'google_credentials'):
                st.info("📋 Using TOML sections format...")
                credentials_dict = {
                    "type": st.secrets.google_credentials.type,
                    "project_id": st.secrets.google_credentials.project_id,
                    "private_key_id": st.secrets.google_credentials.private_key_id,
                    "private_key": st.secrets.google_credentials.private_key,
                    "client_email": st.secrets.google_credentials.client_email,
                    "client_id": st.secrets.google_credentials.client_id,
                    "auth_uri": st.secrets.google_credentials.auth_uri,
                    "token_uri": st.secrets.google_credentials.token_uri,
                    "auth_provider_x509_cert_url": st.secrets.google_credentials.auth_provider_x509_cert_url,
                    "client_x509_cert_url": st.secrets.google_credentials.client_x509_cert_url,
                    "universe_domain": st.secrets.google_credentials.universe_domain
                }
                spreadsheet_url = st.secrets.google_sheet.url
                worksheet_name = st.secrets.google_sheet.worksheet
            else:
                # Fallback to JSON string format
                st.info("📋 Using JSON string format...")
                credentials_json = (
                    st.secrets.get("GOOGLE_SHEETS_CREDENTIALS") or 
                    st.secrets.get("GOOGLE_CREDENTIALS_JSON") or
                    st.secrets.get("credentials_json")
                )
                
                if not credentials_json:
                    st.error("❌ GOOGLE_SHEETS_CREDENTIALS not found in Streamlit secrets")
                    st.info("💡 Add credentials in TOML sections format or JSON string format")
                    return False
                
                # Parse JSON credentials
                credentials_dict = json.loads(credentials_json)
                
                spreadsheet_url = (
                    st.secrets.get("GOOGLE_SPREADSHEET_URL") or 
                    st.secrets.get("GOOGLE_SHEET_URL") or
                    st.secrets.get("spreadsheet_url")
                )
                
                worksheet_name = (
                    st.secrets.get("GOOGLE_WORKSHEET_NAME") or 
                    st.secrets.get("worksheet_name", "Session_Audits")
                )
            
            if not spreadsheet_url:
                st.error("❌ GOOGLE_SPREADSHEET_URL not found in Streamlit secrets")
                st.info("💡 Make sure you have added the spreadsheet URL in Streamlit Cloud > App Settings > Secrets")
                return False
            
            # Clean URL (remove any query parameters or fragments)
            if "?" in spreadsheet_url:
                spreadsheet_url = spreadsheet_url.split("?")[0]
            if "#" in spreadsheet_url:
                spreadsheet_url = spreadsheet_url.split("#")[0]
            
            st.success(f"✅ Found secrets: URL={spreadsheet_url[:50]}..., Worksheet={worksheet_name}")
            st.info("🔗 Attempting to connect to Google Sheets...")
            
            return self.initialize_connection_from_dict(credentials_dict, spreadsheet_url, worksheet_name)
            
        except Exception as e:
            st.error(f"❌ Error loading Google Sheets secrets: {str(e)}")
            st.info("💡 Check your Streamlit secrets configuration")
            return False
    
    def initialize_connection_from_dict(self, credentials_dict: dict, spreadsheet_url: str, worksheet_name: str = "Session_Audits"):
        """Initialize Google Sheets connection using credentials dictionary"""
        try:
            st.info("🔐 Creating credentials...")
            
            # Define the scope
            scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            
            # Create credentials
            credentials = Credentials.from_service_account_info(credentials_dict, scopes=scope)
            
            st.info("🔌 Initializing client...")
            
            # Initialize the client
            self.client = gspread.authorize(credentials)
            
            st.info("📄 Opening spreadsheet...")
            
            # Open the spreadsheet
            self.sheet = self.client.open_by_url(spreadsheet_url)
            
            st.info(f"📋 Getting worksheet: {worksheet_name}")
            
            # Get or create worksheet
            try:
                self.worksheet = self.sheet.worksheet(worksheet_name)
                st.success(f"✅ Found existing worksheet: {worksheet_name}")
            except gspread.WorksheetNotFound:
                st.info(f"📝 Creating new worksheet: {worksheet_name}")
                self.worksheet = self.sheet.add_worksheet(title=worksheet_name, rows=1000, cols=50)
                self._initialize_headers()
                st.success(f"✅ Created new worksheet: {worksheet_name}")
            
            st.success("🎉 Google Sheets connection successful!")
            return True
            
        except Exception as e:
            st.error(f"❌ Error connecting to Google Sheets: {str(e)}")
            st.info("💡 Make sure the Google Sheet is shared with: physical-form@physical-form.iam.gserviceaccount.com")
            return False
    
    def _initialize_headers(self):
        """Initialize headers in the Google Sheet"""
        headers = [
            "Timestamp", "Level", "Session type", "Day/Number", "Group Code",
            "Recorded session link", "Month", "Session Date", "Governorate", "Area",
            "Center Name", "Instructor Code", "Instructor Name", "Camera",
            "Camera quality", "Camera Coverage", "Sound", "Internet connection",
            "Full Session?", "Session duration ( hours)", "Students seated",
            "Coordinator appearance", "Room adequacy", "Instructor appearance",
            "Instructor Attitude", "English language of instructor",
            "Language of instructor (slang language is used)", "Activity", "Break",
            "Break Time ( Minutes)", "Students feedback average score",
            "Coordinator feedback score", "Positive Comments", "Negative Comments",
            "Auditor", "Score", "Session Rating", "Project Coordinator",
            "Students Comment", "Validity", "Our Comments"
        ]
        
        self.worksheet.update('A1:AN1', [headers])
    
    def save_audit_data(self, form_data: Dict[str, Any], score_data: Dict[str, Any]) -> bool:
        """Save audit data to Google Sheets"""
        try:
            if not self.worksheet:
                st.error("Google Sheets connection not initialized")
                return False
            
            # Prepare data row
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            row_data = [
                timestamp,
                form_data.get("Level", ""),
                form_data.get("Session type", ""),
                form_data.get("Day/Number", ""),
                form_data.get("Group Code", ""),
                form_data.get("Recorded session link", ""),
                form_data.get("Month", ""),
                str(form_data.get("Session Date", "")),
                form_data.get("Governorate", ""),
                form_data.get("Area", ""),
                form_data.get("Center Name", ""),
                form_data.get("Instructor Code", ""),
                form_data.get("Instructor Name", ""),
                form_data.get("Camera", ""),
                form_data.get("Camera quality", ""),
                form_data.get("Camera Coverage", ""),
                form_data.get("Sound", ""),
                form_data.get("Internet connection", ""),
                form_data.get("Full Session?", ""),
                form_data.get("Session duration ( hours)", ""),
                form_data.get("Students seated", ""),
                form_data.get("Coordinator appearance", ""),
                form_data.get("Room adequacy", ""),
                form_data.get("Instructor appearance", ""),
                form_data.get("Instructor Attitude", ""),
                form_data.get("English language of instructor", ""),
                form_data.get("Language of instructor (slang language is used)", ""),
                form_data.get("Activity", ""),
                form_data.get("Break", ""),
                form_data.get("Break Time ( Minutes)", ""),
                form_data.get("Students feedback average score", ""),
                form_data.get("Coordinator feedback score", ""),
                form_data.get("Positive Comments", ""),
                form_data.get("Negative Comments", ""),
                form_data.get("Auditor", ""),
                score_data.get("total_score", ""),
                score_data.get("session_rating", ""),
                form_data.get("Project Coordinator", ""),
                form_data.get("Students Comment", ""),
                form_data.get("Validity", ""),
                form_data.get("Our Comments", "")
            ]
            
            # Append to sheet
            self.worksheet.append_row(row_data)
            return True
            
        except Exception as e:
            st.error(f"Error saving data to Google Sheets: {str(e)}")
            return False
    
    def get_all_data(self) -> Optional[pd.DataFrame]:
        """Retrieve all data from Google Sheets as DataFrame"""
        try:
            if not self.worksheet:
                return None
            
            data = self.worksheet.get_all_records()
            return pd.DataFrame(data)
            
        except Exception as e:
            st.error(f"Error retrieving data from Google Sheets: {str(e)}")
            return None
    
    def get_data_by_filter(self, column: str, value: Any) -> Optional[pd.DataFrame]:
        """Retrieve filtered data from Google Sheets"""
        try:
            df = self.get_all_data()
            if df is not None and column in df.columns:
                return df[df[column] == value]
            return None
            
        except Exception as e:
            st.error(f"Error filtering data: {str(e)}")
            return None
    
    def update_record(self, row_index: int, column: str, new_value: Any) -> bool:
        """Update a specific cell in the Google Sheet"""
        try:
            if not self.worksheet:
                return False
            
            # Find column index
            headers = self.worksheet.row_values(1)
            if column not in headers:
                st.error(f"Column '{column}' not found")
                return False
            
            col_index = headers.index(column) + 1
            
            # Update cell (row_index + 2 because of header and 1-indexed)
            self.worksheet.update_cell(row_index + 2, col_index, new_value)
            return True
            
        except Exception as e:
            st.error(f"Error updating record: {str(e)}")
            return False
    
    def delete_record(self, row_index: int) -> bool:
        """Delete a record from Google Sheets"""
        try:
            if not self.worksheet:
                return False
            
            # Delete row (row_index + 2 because of header and 1-indexed)
            self.worksheet.delete_rows(row_index + 2)
            return True
            
        except Exception as e:
            st.error(f"Error deleting record: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get basic statistics from the data"""
        try:
            df = self.get_all_data()
            if df is None or df.empty:
                return {}
            
            stats = {
                "total_records": len(df),
                "average_score": df["Score"].mean() if "Score" in df.columns else 0,
                "rating_distribution": df["Session Rating"].value_counts().to_dict() if "Session Rating" in df.columns else {},
                "latest_entry": df["Timestamp"].max() if "Timestamp" in df.columns else "",
                "governorate_distribution": df["Governorate"].value_counts().to_dict() if "Governorate" in df.columns else {}
            }
            
            return stats
            
        except Exception as e:
            st.error(f"Error calculating statistics: {str(e)}")
            return {}

# Global database instance
db_instance = GoogleSheetsDB()

def get_database():
    """Get the global database instance"""
    return db_instance
