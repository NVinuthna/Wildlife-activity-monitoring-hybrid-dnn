import streamlit as st
import pandas as pd

st.title("🐾 Wildlife Activity Monitoring System")

# 1. Load the Dataset
try:
    df = pd.read_csv("Datasets.csv")
    df.columns = df.columns.str.strip() # Cleans any hidden spaces in CSV headers

    # 2. Main Monitoring Form
    with st.form("monitoring_form"):
        st.subheader("Analysis Parameters")
        u_forest = st.selectbox("Select Forest", df['Forest_Name'].unique())
        u_animal = st.selectbox("Select Animal", df['Animal'].unique())
        
        # CORRECTED: Use form_submit_button inside the form
        submitted = st.form_submit_button("Start Monitoring")
        
        if submitted:
            row = df[(df['Forest_Name'] == u_forest) & (df['Animal'] == u_animal)].iloc[0]
            st.success(f"Results: {row['Label']}")
            st.warning(f"Alert: {row['Alert_Message']}")

    # 3. Navigation Buttons (MUST be outside the form to avoid the API error)
    if st.button("Back to Login"):
        st.write("Redirecting to login...")
        st.rerun()
        # Add your login redirection logic here

except Exception as e:
    st.error(f"Execution Error: {e}")
