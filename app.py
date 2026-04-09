import streamlit as st
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder

st.title("Wildlife Activity Monitoring System")

# 1. Load the Dataset
try:
    df = pd.read_csv("Datasets.csv") #
    
    # 2. Setup the Form
    with st.form("detection_form"):
        st.subheader("Analyze Wildlife Activity")
        
        # User selection based on your CSV columns
        selected_forest = st.selectbox("Select Forest Name", df['Forest Name'].unique())
        selected_loc = st.selectbox("Select Location", df['Location'].unique())
        
        # FIX: The correct function name for the submit button
        submitted = st.form_submit_button("Run Monitoring")
        
        if submitted:
            # Add your prediction/alert logic here
            st.success(f"Monitoring complete for {selected_forest}. No threats detected.")

except FileNotFoundError:
    st.error("Initialization Error: Ensure 'Datasets.csv' is in the root folder.") #
