import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier

# 1. Page Configuration
st.set_page_config(page_title="Wildlife Monitoring System", layout="centered")

# Initialize Session State for Navigation and User Data
if 'page' not in st.session_state:
    st.session_state.page = 'Login'
if 'users' not in st.session_state:
    st.session_state.users = {"Admin": "Admin123"} # Default User

# 2. Styling (To match your red/black/white theme)
st.markdown("""
    <style>
    .main { background-color: #000000; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #FF0000; color: white; }
    h1 { color: #FF0000; font-family: 'Fredoka One'; text-align: center; }
    .login-box { background-color: #ffffff; padding: 30px; border-radius: 10px; border: 2px solid #FF0000; }
    </style>
    """, unsafe_allow_html=True)

# --- PAGE: LOGIN ---
if st.session_state.page == 'Login':
    st.markdown("<h1>USER LOGIN</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("LOGIN"):
                if user in st.session_state.users and st.session_state.users[user] == pw:
                    st.success("Login Successful!")
                    st.session_state.page = 'Detect'
                    st.rerun()
                else:
                    st.error("Invalid Username or Password")
        with col2:
            if st.button("GO TO REGISTER"):
                st.session_state.page = 'Register'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- PAGE: REGISTER ---
elif st.session_state.page == 'Register':
    st.markdown("<h1>USER REGISTRATION</h1>", unsafe_allow_html=True)
    
    with st.form("reg_form"):
        new_user = st.text_input("Choose Username")
        new_pw = st.text_input("Choose Password", type="password")
        email = st.text_input("Email ID")
        address = st.text_area("Address")
        
        if st.form_submit_button("CREATE ACCOUNT"):
            if new_user and new_pw:
                st.session_state.users[new_user] = new_pw
                st.success("Account Created! You can now Login.")
                if st.button("Back to Login"):
                    st.session_state.page = 'Login'
                    st.rerun()
            else:
                st.error("Please fill in all fields.")
    
    if st.button("Back to Login"):
        st.session_state.page = 'Login'
        st.rerun()

# --- PAGE: PREDICTION (The actual project execution) ---
elif st.session_state.page == 'Detect':
    st.sidebar.button("Logout", on_click=lambda: setattr(st.session_state, 'page', 'Login'))
    st.markdown("<h1>🐾 WILDLIFE DETECTION</h1>", unsafe_allow_html=True)
    
    # Prediction Logic
    try:
        df = pd.read_csv('Datasets.csv')
        cv = CountVectorizer()
        X = cv.fit_transform(df['Fid'].apply(str))
        y = df['Label']
        model = MLPClassifier(max_iter=500).fit(X, y)

        with st.form("predict_form"):
            fid = st.text_input("Enter Fid for Analysis")
            if st.form_submit_button("PREDICT ACTIVITY"):
                pred = model.predict(cv.transform([fid]))[0]
                msgs = {0: "Crossing Forest Lines", 1: "Hindrance to Villagers", 2: "Trespassing"}
                st.info(f"RESULT: {msgs.get(pred, 'Unknown').upper()}")
    except:
        st.error("Datasets.csv not found!")
