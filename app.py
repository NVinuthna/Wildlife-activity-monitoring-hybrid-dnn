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
            # Simple bypass for local testing; connect to DB if needed
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

# --- PAGE 3: MONITORING (THE FIX) ---
elif st.session_state.page == 'monitoring':
    st.title("🐾 Wildlife Monitoring System")
    
    try:
        # Load your specific CSV
        df = pd.read_csv("Datasets.csv")
        df.columns = df.columns.str.strip() # Clean column names
        
        with st.form("monitoring_form"):
            u_forest = st.selectbox("Select Forest", df['Forest_Name'].unique())
            u_animal = st.selectbox("Select Animal", df['Animal'].unique())
            submitted = st.form_submit_button("Start Monitoring")

        if submitted:
            # Get the exact row from your Datasets.csv
            row = df[(df['Forest_Name'] == u_forest) & (df['Animal'] == u_animal)].iloc[0]
            
            st.divider()
            
            # --- STEP 1: CREATE TWO COLUMNS FOR OUTPUT ---
            col1, col2 = st.columns([1, 1]) 
            
            with col1:
                st.subheader("🖼️ Visual Identification")
                # Look for image in your GitHub images folder
                img_path = f"images/{u_animal}.jpg"
                if os.path.exists(img_path):
                    st.image(img_path, caption=f"Detected: {u_animal}", use_container_width=True)
                else:
                    # Placeholder if image is not uploaded to GitHub yet
                    st.warning(f"No image found for {u_animal} in /images folder.")
                    st.image("https://via.placeholder.com/400x300?text=Animal+Detection+Active", use_container_width=True)

            with col2:
                st.subheader("📊 Detection Analytics")
                
                # Map the Label numbers to text based on your views.py logic
                status_map = {0: "Safe (Forest Crossing)", 1: "Warning (Village Proximity)", 2: "Alert (Trespassing)"}
                status_text = status_map.get(int(row['Label']), "Detection Active")
                
                # Show the primary alert status
                st.error(f"**Alert Status:** {status_text}")
                st.info(f"**System Message:** {row['Alert_Message']}")
                
                # Display all the "other columns" from your CSV
                st.write("---")
                st.write(f"**Physical Height:** {row['Height_cm']} cm")
                st.write(f"**Physical Weight:** {row['Weight_kg']} kg")
                st.write(f"**Habitat:** {row['Habitat']}")
                st.write(f"**Conservation:** {row['Conservation_Status']}")
                st.write(f"**Social Structure:** {row['Social_Structure']}")
                st.write(f"**Alert Date:** {row['Alert_Message_Date']}")

    except Exception as e:
        st.error(f"Configuration Error: {e}")

    if st.sidebar.button("Logout"):
        st.session_state.page = 'login'
        st.rerun()
