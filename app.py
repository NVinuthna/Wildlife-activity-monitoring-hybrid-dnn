import streamlit as st
import pandas as pd

# 1. Initialize Page State (Must be at the top)
if 'page' not in st.session_state:
    st.session_state.page = 'monitoring'

# --- PAGE 1: MONITORING SECTION ---
if st.session_state.page == 'monitoring':
    st.title("🐾 Wildlife Activity Monitoring System")

    try:
        # Load the Dataset
        df = pd.read_csv("Datasets.csv")
        # Remove hidden spaces from column names to fix KeyError
        df.columns = df.columns.str.strip() 

        # Main Monitoring Form
        with st.form("monitoring_form"):
            st.subheader("Analysis Parameters")
            
            # Use columns that exist in your Datasets.csv
            u_forest = st.selectbox("Select Forest", df['Forest_Name'].unique())
            u_animal = st.selectbox("Select Animal", df['Animal'].unique())
            
            # MANDATORY: Submit button must be INSIDE the form block
            submitted = st.form_submit_button("Start Monitoring")
            
            if submitted:
                # Filter data and show results
                match = df[(df['Forest_Name'] == u_forest) & (df['Animal'] == u_animal)]
                if not match.empty:
                    row = match.iloc[0]
                    st.success(f"Results: {row['Label']}")
                    st.warning(f"Alert: {row['Alert_Message']}")
                else:
                    st.error("No data found for this selection.")

    except FileNotFoundError:
        st.error("Datasets.csv not found. Please upload it to your GitHub.")
    except Exception as e:
        st.error(f"Execution Error: {e}")

    # Navigation Button (MUST be outside the form block)
    st.write("---")
    if st.button("Back to Login"):
        st.session_state.page = 'login'
        st.rerun()

# --- PAGE 2: LOGIN SECTION ---
elif st.session_state.page == 'login':
    st.title("🔐 System Login")
    st.info("You have successfully redirected to the login page.")
    
    st.text_input("Username")
    st.text_input("Password", type="password")
    
    if st.button("Login to Monitoring"):
        st.session_state.page = 'monitoring'
        st.rerun()
