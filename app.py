import streamlit as st
import pandas as pd
import os

# 1. Initialize Page State
if 'page' not in st.session_state:
    st.session_state.page = 'login'

# --- PAGE 1: LOGIN ---
if st.session_state.page == 'login':
    st.title("🔐 System Login")
    st.text_input("Username")
    st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
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

# --- PAGE 3: MONITORING (FIXED SECTION) ---
elif st.session_state.page == 'monitoring':
    st.title("🐾 Wildlife Monitoring System")
    
    try:
        # Load Dataset
        df = pd.read_csv("Datasets.csv")
        df.columns = df.columns.str.strip()
        
        # Selection Form
        with st.form("monitoring_form"):
            u_forest = st.selectbox("Select Forest", df['Forest_Name'].unique())
            u_animal = st.selectbox("Select Animal", df['Animal'].unique())
            submitted = st.form_submit_button("Start Monitoring")

        # OUTPUT SECTION: This only runs when the button is clicked
        if submitted:
            row = df[(df['Forest_Name'] == u_forest) & (df['Animal'] == u_animal)].iloc[0]
            
            st.divider() # Visual line separator
            
            # --- CREATE THE COLUMNS FOR CLEAR OUTPUT ---
            col1, col2 = st.columns([2, 1]) # col1 is wider for the visual
            
            with col1:
                st.subheader("🔴 Live Monitoring Feed")
                # Look for an image in your 'images' folder matching the animal name
                img_path = f"images/{u_animal}.jpg"
                
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True)
                else:
                    # Generic placeholder if image is missing
                    st.warning(f"No visual feed found for {u_animal}. Check your images folder.")
                    st.image("https://via.placeholder.com/400x300?text=No+Visual+Signal", use_container_width=True)

            with col2:
                st.subheader("📊 Analysis Data")
                st.metric(label="System Status", value=f"Code {row['Label']}")
                st.write(f"**Target:** {u_animal}")
                st.write(f"**Location:** {u_forest}")
                
                # Adding a small chart to fill the "other columns" requirement
                st.write("Detection Confidence")
                st.progress(85) # Example static value
                st.bar_chart([1, 3, 2, 5])

    except Exception as e:
        st.error(f"Error loading monitoring data: {e}")

    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"page": "login"}))
