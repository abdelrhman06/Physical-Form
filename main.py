"""
Main Streamlit Application for Session Audit Form System
Professional UI with modern design and comprehensive functionality
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any

# Import custom modules
from config import load_field_config, DEFAULT_FIELD_CONFIG
from scoring import calculate_session_score, get_scoring_summary
from database import get_database

# Page configuration
st.set_page_config(
    page_title="Session Audit System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .form-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
    }
    
    .success-message {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def render_field(field_name: str, field_config: Dict[str, Any], key_suffix: str = "") -> Any:
    """Render a form field based on its configuration"""
    field_type = field_config.get("type", "text")
    required = field_config.get("required", False)
    key = f"{field_name}_{key_suffix}" if key_suffix else field_name
    
    label = field_name + (" *" if required else "")
    
    if field_type == "text":
        return st.text_input(label, key=key)
    
    elif field_type == "textarea":
        return st.text_area(label, key=key, height=100)
    
    elif field_type == "dropdown":
        options = field_config.get("options", [])
        return st.selectbox(label, [""] + options, key=key)
    
    elif field_type == "number":
        min_val = field_config.get("min_value", 0.0)
        max_val = field_config.get("max_value", 100.0)
        step = field_config.get("step", 1.0)
        return st.number_input(label, min_value=min_val, max_value=max_val, step=step, key=key)
    
    elif field_type == "date":
        return st.date_input(label, key=key)
    
    elif field_type == "checkbox":
        return st.checkbox(label, key=key)
    
    else:
        return st.text_input(label, key=key)

def validate_form_data(form_data: Dict[str, Any], field_config: Dict[str, Any]) -> tuple[bool, list]:
    """Validate form data based on field configuration"""
    errors = []
    
    for field_name, config in field_config.items():
        if config.get("required", False):
            value = form_data.get(field_name)
            if not value or (isinstance(value, str) and value.strip() == ""):
                errors.append(f"{field_name} is required")
    
    return len(errors) == 0, errors

def main_form_page():
    """Main form page for session audit"""
    st.markdown("""
    <div class="main-header">
        <h1>📋 Session Audit Form</h1>
        <p>Comprehensive evaluation system for educational sessions</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load field configuration
    field_config = load_field_config()
    
    # Initialize form data in session state
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Create form
    with st.form("session_audit_form", clear_on_submit=False):
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Split fields into logical sections
        sections = {
            "📅 Session Information": [
                "Level", "Session type", "Day/Number", "Group Code", 
                "Recorded session link", "Month", "Session Date"
            ],
            "🏢 Location & Personnel": [
                "Governorate", "Area", "Center Name", "Instructor Code", 
                "Instructor Name", "Project Coordinator", "Auditor"
            ],
            "🎥 Technical Quality": [
                "Camera", "Camera quality", "Camera Coverage", "Sound", 
                "Internet connection", "Full Session?", "Session duration ( hours)"
            ],
            "👥 Session Environment": [
                "Students seated", "Coordinator appearance", "Room adequacy", 
                "Instructor appearance", "Instructor Attitude"
            ],
            "🗣️ Language & Communication": [
                "English language of instructor", 
                "Language of instructor (slang language is used)"
            ],
            "🎯 Activities & Breaks": [
                "Activity", "Break", "Break Time ( Minutes)"
            ],
            "📊 Feedback Scores": [
                "Students feedback average score", "Coordinator feedback score"
            ],
            "💬 Comments & Validation": [
                "Positive Comments", "Negative Comments", "Students Comment", 
                "Validity", "Our Comments"
            ]
        }
        
        # Render form sections
        for section_title, field_list in sections.items():
            st.markdown(f"### {section_title}")
            
            # Create columns for better layout
            cols = st.columns(2)
            
            for idx, field_name in enumerate(field_list):
                if field_name in field_config:
                    with cols[idx % 2]:
                        value = render_field(field_name, field_config[field_name], "main")
                        st.session_state.form_data[field_name] = value
            
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "🚀 Submit Audit", 
                use_container_width=True,
                type="primary"
            )
    
    # Handle form submission
    if submit_button:
        # Validate form
        is_valid, errors = validate_form_data(st.session_state.form_data, field_config)
        
        if not is_valid:
            st.error("❌ Please fix the following errors:")
            for error in errors:
                st.error(f"• {error}")
        else:
            # Calculate scores
            score_data = calculate_session_score(st.session_state.form_data)
            
            # Display results
            st.success("✅ Form submitted successfully!")
            
            # Create results columns
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 📊 Scoring Results")
                st.metric(
                    label="Total Score",
                    value=f"{score_data['total_score']}/100",
                    delta=f"{score_data['session_rating']}"
                )
                
                # Score breakdown chart
                breakdown_df = pd.DataFrame(
                    list(score_data['score_breakdown'].items()),
                    columns=['Category', 'Score']
                )
                
                fig = px.bar(
                    breakdown_df,
                    x='Score',
                    y='Category',
                    orientation='h',
                    title="Score Breakdown by Category",
                    color='Score',
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(height=600, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 📋 Form Data Summary")
                
                # Key metrics
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Session Rating: {score_data['session_rating']}</h4>
                    <p>Total Score: {score_data['total_score']}/100</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Critical information
                critical_fields = [
                    "Level", "Session type", "Governorate", "Center Name",
                    "Instructor Name", "Session Date"
                ]
                
                st.markdown("**Key Session Information:**")
                for field in critical_fields:
                    value = st.session_state.form_data.get(field, "N/A")
                    st.write(f"• **{field}:** {value}")
            
            # Save to database if configured
            db = get_database()
            if hasattr(st.session_state, 'db_configured') and st.session_state.db_configured:
                if db.save_audit_data(st.session_state.form_data, score_data):
                    st.success("💾 Data saved to Google Sheets successfully!")
                else:
                    st.error("❌ Failed to save data to Google Sheets")
            else:
                st.warning("⚠️ Database not configured. Data not saved. Configure in Settings.")
            
            # Option to download data as JSON
            import json
            export_data = {
                "form_data": st.session_state.form_data,
                "score_data": score_data,
                "timestamp": datetime.now().isoformat()
            }
            
            st.download_button(
                label="📥 Download Data (JSON)",
                data=json.dumps(export_data, indent=2, default=str),
                file_name=f"session_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def admin_page():
    """Admin page for managing field configurations"""
    st.markdown("""
    <div class="main-header">
        <h1>⚙️ Admin Panel</h1>
        <p>Manage form fields and system configuration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load current configuration
    field_config = load_field_config()
    
    tab1, tab2, tab3 = st.tabs(["🔧 Field Management", "💾 Database Settings", "📊 Statistics"])
    
    with tab1:
        st.markdown("### Field Configuration Management")
        
        # Add new field
        st.markdown("#### ➕ Add New Field")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_field_name = st.text_input("Field Name")
        with col2:
            new_field_type = st.selectbox("Field Type", 
                ["text", "textarea", "dropdown", "number", "date", "checkbox"])
        with col3:
            new_field_required = st.checkbox("Required")
        
        # Additional configuration based on field type
        additional_config = {}
        
        if new_field_type == "dropdown":
            options_text = st.text_area("Dropdown Options (one per line)")
            if options_text:
                additional_config["options"] = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
        
        elif new_field_type == "number":
            col1, col2, col3 = st.columns(3)
            with col1:
                additional_config["min_value"] = st.number_input("Min Value", value=0.0)
            with col2:
                additional_config["max_value"] = st.number_input("Max Value", value=100.0)
            with col3:
                additional_config["step"] = st.number_input("Step", value=1.0, min_value=0.1)
        
        if st.button("Add Field"):
            if new_field_name and new_field_name not in field_config:
                field_config[new_field_name] = {
                    "type": new_field_type,
                    "required": new_field_required,
                    **additional_config
                }
                from config import save_field_config
                save_field_config(field_config)
                st.success(f"✅ Field '{new_field_name}' added successfully!")
                st.rerun()
            else:
                st.error("❌ Field name is empty or already exists!")
        
        st.markdown("---")
        
        # Edit existing fields
        st.markdown("#### ✏️ Edit Existing Fields")
        
        selected_field = st.selectbox("Select Field to Edit", list(field_config.keys()))
        
        if selected_field:
            current_config = field_config[selected_field]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                edit_type = st.selectbox("Type", 
                    ["text", "textarea", "dropdown", "number", "date", "checkbox"],
                    index=["text", "textarea", "dropdown", "number", "date", "checkbox"].index(current_config.get("type", "text")))
            with col2:
                edit_required = st.checkbox("Required", value=current_config.get("required", False))
            with col3:
                if st.button("🗑️ Delete Field"):
                    del field_config[selected_field]
                    from config import save_field_config
                    save_field_config(field_config)
                    st.success(f"✅ Field '{selected_field}' deleted!")
                    st.rerun()
            
            # Type-specific editing
            edit_config = {"type": edit_type, "required": edit_required}
            
            if edit_type == "dropdown":
                current_options = current_config.get("options", [])
                options_text = st.text_area("Options (one per line)", 
                    value='\n'.join(current_options))
                if options_text:
                    edit_config["options"] = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
            
            elif edit_type == "number":
                col1, col2, col3 = st.columns(3)
                with col1:
                    edit_config["min_value"] = st.number_input("Min", 
                        value=current_config.get("min_value", 0.0))
                with col2:
                    edit_config["max_value"] = st.number_input("Max", 
                        value=current_config.get("max_value", 100.0))
                with col3:
                    edit_config["step"] = st.number_input("Step", 
                        value=current_config.get("step", 1.0), min_value=0.1)
            
            if st.button("💾 Update Field"):
                field_config[selected_field] = edit_config
                from config import save_field_config
                save_field_config(field_config)
                st.success(f"✅ Field '{selected_field}' updated!")
                st.rerun()
    
    with tab2:
        st.markdown("### 🔗 Google Sheets Database Configuration")
        
        # Attempt auto-connect from secrets
        db = get_database()
        if not hasattr(st.session_state, 'db_configured'):
            if db.initialize_connection_from_secrets():
                st.session_state.db_configured = True
                st.session_state.credentials_json = st.secrets.get("GOOGLE_SHEETS_CREDENTIALS") or st.secrets.get("GOOGLE_CREDENTIALS_JSON")
                st.session_state.spreadsheet_url = st.secrets.get("GOOGLE_SPREADSHEET_URL") or st.secrets.get("GOOGLE_SHEET_URL")
                st.session_state.worksheet_name = st.secrets.get("GOOGLE_WORKSHEET_NAME", "Session_Audits")
        
        st.markdown("#### Connection Settings")
        
        credentials_json = st.text_area(
            "Google Service Account Credentials (JSON)",
            height=200,
            help="Paste your Google Service Account credentials JSON here"
        )
        
        spreadsheet_url = st.text_input(
            "Google Sheets URL",
            help="Full URL of your Google Sheets document"
        )
        
        worksheet_name = st.text_input(
            "Worksheet Name",
            value="Session_Audits",
            help="Name of the worksheet to use"
        )
        
        if st.button("🔌 Test Connection"):
            if credentials_json and spreadsheet_url:
                if db.initialize_connection(credentials_json, spreadsheet_url, worksheet_name):
                    st.success("✅ Connection successful!")
                    st.session_state.db_configured = True
                    # Store connection info in session state
                    st.session_state.credentials_json = credentials_json
                    st.session_state.spreadsheet_url = spreadsheet_url
                    st.session_state.worksheet_name = worksheet_name
                else:
                    st.error("❌ Connection failed!")
            else:
                st.error("❌ Please provide both credentials and spreadsheet URL")
        
        # Show connection status
        if hasattr(st.session_state, 'db_configured') and st.session_state.db_configured:
            st.success("🟢 Database Connected")
        else:
            st.warning("🟡 Database Not Connected")
    
    with tab3:
        st.markdown("### 📊 System Statistics")
        
        if hasattr(st.session_state, 'db_configured') and st.session_state.db_configured:
            db = get_database()
            stats = db.get_statistics()
            
            if stats:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Records", stats.get("total_records", 0))
                with col2:
                    st.metric("Average Score", f"{stats.get('average_score', 0):.1f}")
                with col3:
                    st.metric("Latest Entry", stats.get("latest_entry", "N/A"))
                with col4:
                    rating_dist = stats.get("rating_distribution", {})
                    most_common = max(rating_dist.items(), key=lambda x: x[1])[0] if rating_dist else "N/A"
                    st.metric("Most Common Rating", most_common)
                
                # Charts
                col1, col2 = st.columns(2)
                
                with col1:
                    if rating_dist:
                        fig_ratings = px.pie(
                            values=list(rating_dist.values()),
                            names=list(rating_dist.keys()),
                            title="Session Rating Distribution"
                        )
                        st.plotly_chart(fig_ratings, use_container_width=True)
                
                with col2:
                    gov_dist = stats.get("governorate_distribution", {})
                    if gov_dist:
                        fig_gov = px.bar(
                            x=list(gov_dist.keys()),
                            y=list(gov_dist.values()),
                            title="Sessions by Governorate"
                        )
                        fig_gov.update_xaxes(tickangle=45)
                        st.plotly_chart(fig_gov, use_container_width=True)
            else:
                st.info("📊 No data available yet")
        else:
            st.warning("🔒 Please configure database connection first")

def data_viewer_page():
    """Data viewer page for browsing and managing records"""
    st.markdown("""
    <div class="main-header">
        <h1>📊 Data Viewer</h1>
        <p>Browse and manage audit records</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not (hasattr(st.session_state, 'db_configured') and st.session_state.db_configured):
        st.warning("🔒 Please configure database connection in Admin Panel first")
        return
    
    db = get_database()
    data = db.get_all_data()
    
    if data is not None and not data.empty:
        # Filters
        st.markdown("### 🔍 Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if "Governorate" in data.columns:
                gov_filter = st.selectbox("Governorate", ["All"] + list(data["Governorate"].unique()))
            else:
                gov_filter = "All"
        
        with col2:
            if "Session Rating" in data.columns:
                rating_filter = st.selectbox("Rating", ["All"] + list(data["Session Rating"].unique()))
            else:
                rating_filter = "All"
        
        with col3:
            if "Level" in data.columns:
                level_filter = st.selectbox("Level", ["All"] + list(data["Level"].unique()))
            else:
                level_filter = "All"
        
        # Apply filters
        filtered_data = data.copy()
        if gov_filter != "All" and "Governorate" in filtered_data.columns:
            filtered_data = filtered_data[filtered_data["Governorate"] == gov_filter]
        if rating_filter != "All" and "Session Rating" in filtered_data.columns:
            filtered_data = filtered_data[filtered_data["Session Rating"] == rating_filter]
        if level_filter != "All" and "Level" in filtered_data.columns:
            filtered_data = filtered_data[filtered_data["Level"] == level_filter]
        
        # Display data
        st.markdown(f"### 📋 Records ({len(filtered_data)} found)")
        
        # Download option
        if not filtered_data.empty:
            csv = filtered_data.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"session_audits_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        # Data table
        st.dataframe(
            filtered_data,
            use_container_width=True,
            height=600
        )
        
        # Summary statistics for filtered data
        if not filtered_data.empty and "Score" in filtered_data.columns:
            st.markdown("### 📈 Summary Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", len(filtered_data))
            with col2:
                st.metric("Average Score", f"{filtered_data['Score'].mean():.1f}")
            with col3:
                st.metric("Highest Score", filtered_data['Score'].max())
            with col4:
                st.metric("Lowest Score", filtered_data['Score'].min())
    
    else:
        st.info("📊 No data available yet. Submit some audit forms first!")

def main():
    """Main application function"""
    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")
    
    pages = {
        "📋 Audit Form": main_form_page,
        "⚙️ Admin Panel": admin_page,
        "📊 Data Viewer": data_viewer_page
    }
    
    selected_page = st.sidebar.selectbox("Select Page", list(pages.keys()))
    
    # Initialize database connection from secrets if available
    db = get_database()
    if not hasattr(st.session_state, 'db_configured'):
        # st.sidebar.info("🔄 Initializing database connection...")
        if db.initialize_connection_from_secrets():
            st.session_state.db_configured = True
            st.session_state.credentials_json = st.secrets.get("GOOGLE_SHEETS_CREDENTIALS") or st.secrets.get("GOOGLE_CREDENTIALS_JSON")
            st.session_state.spreadsheet_url = st.secrets.get("GOOGLE_SPREADSHEET_URL") or st.secrets.get("GOOGLE_SHEET_URL")
            st.session_state.worksheet_name = st.secrets.get("GOOGLE_WORKSHEET_NAME", "Session_Audits")
            # st.sidebar.success("✅ Database connected via secrets!")
        else:
            st.sidebar.warning("⚠️ Database not connected. Configure in Admin Panel.")
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Quick Stats")
    
    if hasattr(st.session_state, 'db_configured') and st.session_state.db_configured:
        stats = db.get_statistics()
        if stats:
            st.sidebar.metric("Total Records", stats.get("total_records", 0))
            st.sidebar.metric("Avg Score", f"{stats.get('average_score', 0):.1f}")
    else:
        st.sidebar.info("Connect database in Admin Panel or via Streamlit secrets")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 🚀 Features
    - ✅ Dynamic form configuration
    - 📊 Automated scoring
    - 🔗 Google Sheets integration
    - 📈 Real-time analytics
    - 🎨 Modern UI design
    """)
    
    # Run selected page
    pages[selected_page]()

if __name__ == "__main__":
    main()
