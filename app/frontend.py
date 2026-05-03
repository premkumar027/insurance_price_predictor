import os
import streamlit as st
import requests

API_URL = os.environ.get("API_URL", "http://localhost:8000/predict")

st.title("Insurance Price Predictor")

st.markdown("Enter your details below")

# input fields
age = st.number_input("Age", min_value=0, max_value=125, value=30)
sex = st.selectbox("What is your gender?", options=['male', 'female'])
weight = st.number_input("Weight", min_value=1.0, max_value=250.0, value=70.0)
height = st.number_input("Height", min_value=0.1, max_value=2.5)
children = st.number_input("Number of children", min_value=1, max_value=5, value=1)
smoker = st.selectbox("Do you smoke?", options=['yes', 'no'])
region = st.selectbox("Where do you live?", options=['northwest', 'northeast', 'southwest', 'southeast'])

if st.button("Predict Cost"):
    input_data = {
        'age': age,
        'sex': sex,
        'weight': weight,
        'height': height,
        'children': children,
        'smoker': smoker,
        'region': region
    }

    try:
        response = requests.post(API_URL, json=input_data)
        result = response.json()

        if response.status_code == 200 and "predicted_amount" in result:
            amount = result['predicted_amount']
            st.success(f'Predicted Insurance Cost: ${amount}')
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")