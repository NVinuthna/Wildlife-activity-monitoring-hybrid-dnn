import streamlit as st
import pandas as pd

# 1. Initialize Page State
if 'page' not in st.session_state:
    st.session_state.page = 'login' # Start at login

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

# --- PAGE 3: MONITORING ---
elif st.session_state.page == 'monitoring':
    st.title("🐾 Wildlife Monitoring System")
    
    try:
        df = pd.read_csv("Datasets.csv")
        df.columns = df.columns.str.strip()
        
        with st.form("monitoring_form"):
            u_forest = st.selectbox("Select Forest", df['Forest_Name'].unique())
            u_animal = st.selectbox("Select Animal", df['Animal'].unique())
            if st.form_submit_button("Start Monitoring"):
                row = df[(df['Forest_Name'] == u_forest) & (df['Animal'] == u_animal)].iloc[0]
                st.write(f"*Status:* {row['Label']}")

    except Exception as e:
        st.error(f"Error: {e}")

    if st.button("Logout"):
        st.session_state.page = 'login'
        st.rerun()
