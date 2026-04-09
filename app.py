import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Page Configuration
st.set_page_config(page_title="Wildlife Monitoring", layout="centered")

# Custom CSS to match your 'Righteous' font style from the HTML
st.markdown("""
    <style>
    .title-text { font-family: 'Fredoka One', cursive; color: #2c3e50; text-align: center; }
    .result-box { background-color: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center; font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='title-text'>🐾 Detect Animal Activity Type</h1>", unsafe_allow_html=True)

# Function to map prediction numbers to the messages in your Dataset
def get_prediction_message(label):
    mapping = {
        0: "crossing the forest lines",
        1: "hindrance to villagers and tourists people",
        2: "detection of trespassing"
    }
    return mapping.get(label, "Unknown Activity")

# 1. Background Training (Required to make the 'Predict' button work)
@st.cache_resource
def train_model():
    df = pd.read_csv('Datasets.csv')
    cv = CountVectorizer()
    # Using 'Fid' as the feature matching your views.py logic
    X = cv.fit_transform(df['Fid'].apply(str))
    y = df['Label']
    model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500).fit(X, y)
    return model, cv

try:
    model, cv = train_model()

    # 2. The Form (Matching your Detect_Animal_Activity_Type.html)
    with st.form("prediction_form"):
        st.write("### Enter Details for Prediction")
        
        col1, col2 = st.columns(2)
        with col1:
            fid = st.text_input("Enter Fid (e.g. 172.217.10.42...)")
            f_name = st.text_input("Forest Name")
            location = st.text_input("Location")
            animal = st.text_input("Animal")
            height = st.text_input("Height (cm)")
            weight = st.text_input("Weight (kg)")
            color = st.text_input("Color")
        
        with col2:
            diet = st.text_input("Diet")
            habitat = st.text_input("Habitat")
            predators = st.text_input("Predators")
            countries = st.text_input("Countries Found")
            status = st.text_input("Conservation Status")
            family = st.text_input("Family")
            social = st.text_input("Social Structure")
            date = st.text_input("Alert Message Date")

        submit = st.form_submit_with_button("Predict")

    # 3. Handle Prediction
    if submit:
        if fid:
            # Transform input and predict
            input_data = cv.transform([fid])
            prediction = model.predict(input_data)[0]
            result_msg = get_prediction_message(prediction)
            
            st.markdown(f"""
                <div class='result-box'>
                    <strong>Prediction Result:</strong><br>
                    <span style='color: #d32f2f; font-weight: bold;'>{result_msg.upper()}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Please enter an FID to run the prediction.")

except Exception as e:
    st.error(f"Initialization Error: Ensure 'Datasets.csv' is in the root folder. Error: {e}")
