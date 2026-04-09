import streamlit as st
import pandas as pd

# Set Page Title
st.set_page_config(page_title="Wildlife Monitoring System", layout="wide")
st.title("🐾 Wildlife Activity Monitoring System")

try:
    # 1. Load the Dataset
    df = pd.read_csv("Datasets.csv")
    
    # 2. Input Section (Sidebar or Form)
    with st.form("monitoring_form"):
        st.subheader("Select Parameters for Analysis")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_forest = st.selectbox("Select Forest Name", df['Forest_Name'].unique())
        with col2:
            # Filters the location based on the selected forest
            loc_options = df[df['Forest_Name'] == selected_forest]['Location'].unique()
            selected_loc = st.selectbox("Select Location", loc_options)
        
        # Corrected: Submit button MUST be inside the 'with' block
        submitted = st.form_submit_button("Run Monitoring Detection")

    # 3. Execution and Data Extraction
    if submitted:
        # Filter the dataset to find the specific row
        row = df[(df['Forest_Name'] == selected_forest) & (df['Location'] == selected_loc)].iloc[0]
        
        st.success(f"### Monitoring Results for {selected_forest}")
        
        # Displaying all extracted columns in an organized layout
        tab1, tab2, tab3 = st.tabs(["Animal Details", "Habitat & Biology", "Alert Status"])
        
        with tab1:
            st.write(f"*Target Animal:* {row['Animal']}")
            st.write(f"*Family:* {row['Family']}")
            st.metric("Height (cm)", row['Height_cm'])
            st.metric("Weight (kg)", row['Weight_kg'])
            
        with tab2:
            st.write(f"*Habitat:* {row['Habitat']}")
            st.write(f"*Diet:* {row['Diet']}")
            st.write(f"*Social Structure:* {row['Social_Structure']}")
            st.write(f"*Predators:* {row['Predators']}")
            
        with tab3:
            # Highlight the Alert and Label
            st.error(f"*Alert Message:* {row['Alert_Message']}")
            st.warning(f"*System Label:* {row['Label']}")
            st.info(f"*Date recorded:* {row['Alert_Message_Date']}")

except FileNotFoundError:
    st.error("Error: 'Datasets.csv' not found. Ensure it is in the same folder as app.py on GitHub.")
except Exception as e:
    st.error(f"Execution Error: {e}")
