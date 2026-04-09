import streamlit as st
import pandas as pd

st.title("Wildlife Activity Monitoring System")

try:
    # 1. Load the data
    df = pd.read_csv("Datasets.csv")
    
    # 2. Build the Form
    with st.form("monitoring_form"):
        st.subheader("Select Parameters")
        
        # FIXED: Using underscores to match your CSV headers
        selected_forest = st.selectbox("Select Forest Name", df['Forest_Name'].unique())
        selected_loc = st.selectbox("Select Location", df['Location'].unique())
        
        # FIXED: This button is now correctly inside the form block
        submitted = st.form_submit_button("Run Monitoring")
        
        if submitted:
            # Finding the row for the selected forest
            results = df[df['Forest_Name'] == selected_forest].iloc[0]
            
            st.success(f"Monitoring active for {selected_forest}!")
            st.write(f"*Alert Message:* {results['Alert_Message']}")
            st.write(f"*Status:* {results['Label']}")

except FileNotFoundError:
    st.error("Could not find 'Datasets.csv'.")
except KeyError as e:
    st.error(f"The app couldn't find the column: {e}.")
