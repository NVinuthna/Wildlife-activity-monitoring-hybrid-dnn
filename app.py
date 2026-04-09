import streamlit as st
import pandas as pd

st.title("Wildlife Activity Monitoring System")

try:
    # 1. Load the data
    df = pd.read_csv("Datasets.csv")
    
    # CRITICAL FIX: This removes any hidden spaces at the start/end of column names
    df.columns = df.columns.str.strip()
    
    # 2. Build the Form
    with st.form("monitoring_form"):
        st.subheader("Select Parameters")
        
        # We use the stripped column names here
        selected_forest = st.selectbox("Select Forest Name", df['Forest Name'].unique())
        selected_loc = st.selectbox("Select Location", df['Location'].unique())
        
        # MANDATORY FIX: This button MUST be inside the 'with st.form' block
        submitted = st.form_submit_button("Run Monitoring")
        
        if submitted:
            st.success(f"Monitoring active for {selected_forest}!")
            st.info("System Status: Normal Activity")

except FileNotFoundError:
    st.error("Could not find 'Datasets.csv'. Please ensure it is in your GitHub main folder.")
except KeyError as e:
    # This helps you see exactly what the column name is if it still fails
    st.error(f"The app couldn't find the column: {e}. Available columns are: {list(df.columns)}")
