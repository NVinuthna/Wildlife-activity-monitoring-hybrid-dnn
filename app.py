import streamlit as st
import pandas as pd

st.title("Wildlife Activity Monitoring System")

try:
    # 1. Load data
    df = pd.read_csv("Datasets.csv")
    
    # FIX for KeyError: Remove hidden spaces from column names
    df.columns = df.columns.str.strip()
    
    # 2. Setup the Form
    with st.form("my_form"):
        st.subheader("Select Parameters")
        
        # This will now work because we 'stripped' the column names above
        selected_forest = st.selectbox("Select Forest Name", df['Forest Name'].unique())
        selected_loc = st.selectbox("Select Location", df['Location'].unique())
        
        # FIX for Missing Submit Button:
        submitted = st.form_submit_button("Run Monitoring")
        
        if submitted:
            st.success(f"Monitoring active for {selected_forest}")
            st.info("Status: Normal Activity Detected")

except FileNotFoundError:
    st.error("Datasets.csv not found in the root folder!")
except KeyError as e:
    st.error(f"Column Name Error: The app couldn't find the column {e}. Check your CSV headers!")
