"""
Configuration file for Session Audit Form System
Contains field definitions and dropdown options
"""

import streamlit as st
from typing import Dict, List, Any
import json

# Default field configurations
DEFAULT_FIELD_CONFIG = {
    "Level": {
        "type": "dropdown",
        "options": ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"],
        "required": True
    },
    "Session type": {
        "type": "dropdown", 
        "options": ["Online", "Offline", "Hybrid"],
        "required": True
    },
    "Day/Number": {
        "type": "text",
        "required": True
    },
    "Group Code": {
        "type": "text", 
        "required": True
    },
    "Recorded session link": {
        "type": "text",
        "required": False
    },
    "Month": {
        "type": "dropdown",
        "options": ["January", "February", "March", "April", "May", "June", 
                   "July", "August", "September", "October", "November", "December"],
        "required": True
    },
    "Session Date": {
        "type": "date",
        "required": True
    },
    "Governorate": {
        "type": "dropdown",
        "options": ["Cairo", "Alexandria", "Giza", "Qalyubia", "Port Said", "Suez", 
                   "Luxor", "Aswan", "Asyut", "Beheira", "Beni Suef", "Dakahlia", 
                   "Damietta", "Fayyum", "Gharbia", "Ismailia", "Kafr el-Sheikh", 
                   "Matrouh", "Minya", "Monufia", "New Valley", "North Sinai", 
                   "Qena", "Red Sea", "Sharqia", "Sohag", "South Sinai"],
        "required": True
    },
    "Area": {
        "type": "text",
        "required": True
    },
    "Center Name": {
        "type": "text",
        "required": True
    },
    "Instructor Code": {
        "type": "text",
        "required": True
    },
    "Instructor Name": {
        "type": "text",
        "required": True
    },
    "Camera": {
        "type": "dropdown",
        "options": ["Working", "Not Working"],
        "required": True,
        "scoring": {"Working": 5, "Not Working": 0}
    },
    "Camera quality": {
        "type": "dropdown",
        "options": ["Clear", "Not clear enough", "Bad quality", "NA"],
        "required": True,
        "scoring": {"Clear": 5, "Not clear enough": 3, "Bad quality": 1, "NA": 0}
    },
    "Camera Coverage": {
        "type": "dropdown",
        "options": ["Full coverage", "Instructor isn't appear", "Some students are not appear", 
                   "Students are not appear", "Neither students nor instructor appear"],
        "required": True,
        "scoring": {"Full coverage": 5, "Instructor isn't appear": 3, "Some students are not appear": 2,
                   "Students are not appear": 1, "Neither students nor instructor appear": 0}
    },
    "Sound": {
        "type": "dropdown",
        "options": ["Working excellent", "Good quality", "Bad quality", "Not working"],
        "required": True,
        "scoring": {"Working excellent": 5, "Good quality": 3, "Bad quality": 1, "Not working": 0}
    },
    "Internet connection": {
        "type": "dropdown",
        "options": ["Excellent", "Frequent Disconnects", "Poor Connection", "Non-Operational"],
        "required": True,
        "scoring": {"Excellent": 5, "Frequent Disconnects": 3, "Poor Connection": 1, "Non-Operational": 0}
    },
    "Full Session?": {
        "type": "dropdown",
        "options": ["Yes", "No", "NA"],
        "required": True,
        "scoring": {"Yes": 10, "No": 0, "NA": 0}
    },
    "Session duration ( hours)": {
        "type": "number",
        "required": True,
        "min_value": 0.0,
        "max_value": 24.0,
        "step": 0.5
    },
    "Students seated": {
        "type": "dropdown",
        "options": ["Yes", "No", "NA", "No not seated in place"],
        "required": True,
        "scoring": {"Yes": 5, "No": 0, "NA": 0, "No not seated in place": 0}
    },
    "Coordinator appearance": {
        "type": "dropdown",
        "options": ["Yes", "No", "NA"],
        "required": True,
        "scoring": {"Yes": 5, "No": 0, "NA": 0}
    },
    "Room adequacy": {
        "type": "dropdown",
        "options": ["Room adequate", "Room not adequate", "NA"],
        "required": True,
        "scoring": {"Room adequate": 5, "Room not adequate": 0, "NA": 0}
    },
    "Instructor appearance": {
        "type": "dropdown",
        "options": ["Yes", "No", "NA"],
        "required": True,
        "scoring": {"Yes": 5, "No": 0, "NA": 0}
    },
    "Instructor Attitude": {
        "type": "dropdown",
        "options": ["Good", "Bad", "NA"],
        "required": True,
        "scoring": {"Good": 5, "Bad": 0, "NA": 0}
    },
    "English language of instructor": {
        "type": "dropdown",
        "options": ["Excellent", "Good", "Bad", "NA"],
        "required": True,
        "scoring": {"Excellent": 5, "Good": 3, "Bad": 0, "NA": 0}
    },
    "Language of instructor (slang language is used)": {
        "type": "dropdown",
        "options": ["No", "Yes", "NA"],
        "required": True,
        "scoring": {"No": 5, "Yes": 0, "NA": 0}
    },
    "Activity": {
        "type": "dropdown",
        "options": ["Yes", "No", "NA"],
        "required": True,
        "scoring": {"Yes": 5, "No": 0, "NA": 0}
    },
    "Break": {
        "type": "dropdown",
        "options": ["Yes", "No", "NA"],
        "required": True,
        "scoring": {"Yes": 5, "No": 0, "NA": 0}
    },
    "Break Time ( Minutes)": {
        "type": "number",
        "required": True,
        "min_value": 0,
        "max_value": 120,
        "step": 1
    },
    "Students feedback average score": {
        "type": "number",
        "required": True,
        "min_value": 0.0,
        "max_value": 100.0,
        "step": 0.1
    },
    "Coordinator feedback score": {
        "type": "number",
        "required": True,
        "min_value": 0.0,
        "max_value": 100.0,
        "step": 0.1
    },
    "Positive Comments": {
        "type": "textarea",
        "required": False
    },
    "Negative Comments": {
        "type": "textarea",
        "required": False
    },
    "Auditor": {
        "type": "text",
        "required": True
    },
    "Project Coordinator": {
        "type": "text",
        "required": True
    },
    "Students Comment": {
        "type": "textarea",
        "required": False
    },
    "Validity": {
        "type": "dropdown",
        "options": ["Valid", "Invalid", "Pending Review"],
        "required": True
    },
    "Our Comments": {
        "type": "textarea",
        "required": False
    }
}

def load_field_config():
    """Load field configuration from session state or use default"""
    if 'field_config' not in st.session_state:
        st.session_state.field_config = DEFAULT_FIELD_CONFIG.copy()
    return st.session_state.field_config

def save_field_config(config: Dict[str, Any]):
    """Save field configuration to session state"""
    st.session_state.field_config = config

def get_field_types():
    """Get available field types"""
    return ["text", "textarea", "dropdown", "number", "date", "checkbox"]

def export_config():
    """Export current configuration as JSON"""
    return json.dumps(st.session_state.field_config, indent=2)

def import_config(config_json: str):
    """Import configuration from JSON"""
    try:
        config = json.loads(config_json)
        st.session_state.field_config = config
        return True
    except Exception as e:
        st.error(f"Error importing configuration: {str(e)}")
        return False
