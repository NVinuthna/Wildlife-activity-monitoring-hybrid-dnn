import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

st.set_page_config(page_title="Wildlife Monitoring", layout="wide")

st.title("🐾 Wildlife Activity Monitoring & Hybrid DNN System")

# Load Dataset
try:
    df = pd.read_csv('Datasets.csv')
    
    # Preprocessing logic from your views.py
    def apply_response(Label):
        if (Label == 0): return "Crossing the forest lines"
        elif (Label == 1): return "Hindrance to villagers and tourists"
        elif (Label == 2): return "Detection of trespassing"
        return "Unknown"

    df['Results_Text'] = df['Label'].apply(apply_response)
    
    st.sidebar.success("Dataset Loaded Successfully!")
    
    if st.sidebar.button("Train All Models"):
        st.subheader("Model Training Results (Accuracy)")
        
        # Prepare Data
        cv = CountVectorizer()
        X = cv.fit_transform(df['Fid'].apply(str))
        y = df['Label']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
        
        # Dictionary to store results
        results = {}

        # 1. MLP (CNN in your code)
        mlpc = MLPClassifier().fit(X_train, y_train)
        results["CNN (MLP)"] = accuracy_score(y_test, mlpc.predict(X_test)) * 100

        # 2. SVM
        svm_model = LinearSVC().fit(X_train, y_train)
        results["SVM"] = accuracy_score(y_test, svm_model.predict(X_test)) * 100

        # 3. Logistic Regression
        lr_model = LogisticRegression().fit(X_train, y_train)
        results["Logistic Regression"] = accuracy_score(y_test, lr_model.predict(X_test)) * 100

        # Display Results in a Table
        res_df = pd.DataFrame(list(results.items()), columns=['Model', 'Accuracy (%)'])
        st.table(res_df)
        st.bar_chart(res_df.set_index('Model'))

    # Prediction Section
    st.divider()
    st.subheader("🔍 Live Activity Detection")
    fid_input = st.text_input("Enter FID (ID) for detection:")
    
    if fid_input:
        # Simple detection logic based on your ratio logic
        cv = CountVectorizer()
        # Re-fitting to include the whole dataset for prediction
        X_full = cv.fit_transform(df['Fid'].apply(str))
        y_full = df['Label']
        final_model = MLPClassifier().fit(X_full, y_full)
        
        prediction = final_model.predict(cv.transform([fid_input]))
        result_label = apply_response(prediction[0])
        
        if prediction[0] == 0:
            st.warning(f"Result: {result_label}")
        elif prediction[0] == 1:
            st.error(f"Result: {result_label}")
        else:
            st.info(f"Result: {result_label}")

except FileNotFoundError:
    st.error("Datasets.csv not found. Please upload it to your GitHub repository.")
