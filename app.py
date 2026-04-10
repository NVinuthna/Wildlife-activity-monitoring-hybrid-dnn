import streamlit as st
import pandas as pd
import os

# 1. Initialize Page State
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- PAGE 1: LOGIN ---
if st.session_state.page == 'login':
    st.title("🔐 System Login")
    u_name = st.text_input("Username")
    u_pass = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            # Simple bypass for local testing
            st.session_state.page = 'monitoring'
            st.rerun()
    with col2:
        if st.button("Go to Register"):
            st.session_state.page = 'register'
            st.rerun()

# --- PAGE 2: REGISTER ---
elif st.session_state.page == 'register':
    st.title("📝 Create Account")
    st.text_input("Full Name")
    st.text_input("Email")
    st.text_input("New Password", type="password")
    
    if st.button("Register Now"):
        st.success("Account created! Please login.")
        st.session_state.page = 'login'
        st.rerun()
    
    if st.button("Back to Login"):
        st.session_state.page = 'login'
        st.rerun()

# --- PAGE 3: MONITORING (UPDATED: ANALYTICS ONLY) ---
elif st.session_state.page == 'monitoring':
    st.title("🐾 Intelligent Wildlife Activity Monitoring and alert generation with hybrid DNN.")
    
    try:
        # Load the dataset
        df = pd.read_csv("Datasets.csv")
        df.columns = df.columns.str.strip() # Clean column names
        
        with st.form("monitoring_form"):
            u_forest = st.selectbox("Select Forest", df['Forest_Name'].unique())
            u_animal = st.selectbox("Select Animal", df['Animal'].unique())
            submitted = st.form_submit_button("Start Monitoring")

        if submitted:
            # Filter the row from CSV
            row = df[(df['Forest_Name'] == u_forest) & (df['Animal'] == u_animal)].iloc[0]
            
            st.divider()
            
            # --- UPDATED SECTION: FULL WIDTH ANALYTICS ---
            # We removed col1 (Visual Identification) and col2 layout.
            st.subheader(f"📊 Detection Analytics: {u_animal}")
            
            # Map the Label numbers to text
            status_map = {0: "Safe (Forest Crossing)", 1: "Warning (Village Proximity)", 2: "Alert (Trespassing)"}
            status_text = status_map.get(int(row['Label']), "Detection Active")
            
            # Show the primary alert status in a full-width box
            st.error(f"**Current Alert Status:** {status_text}")
            st.info(f"**System Notification:** {row['Alert_Message']}")
            
            # Display the technical data columns from your CSV
            st.markdown("### 🔍 Technical Specifications")
            
            # Creating a clean list of details
            st.write(f"**📏 Physical Height:** {row['Height_cm']} cm")
            st.write(f"**⚖️ Physical Weight:** {row['Weight_kg']} kg")
            st.write(f"**🌿 Natural Habitat:** {row['Habitat']}")
            st.write(f"**🛡️ Conservation Status:** {row['Conservation_Status']}")
            st.write(f"**👪 Social Structure:** {row['Social_Structure']}")
            st.write(f"**📅 Last Alert Logged:** {row['Alert_Message_Date']}")
            st.write(f"**📍 Location Area:** {u_forest}")

    except Exception as e:
        st.error(f"Configuration Error: {e}")

    # Logout Button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.page = 'login'
        st.rerun()
