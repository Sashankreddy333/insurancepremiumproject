import streamlit as st
import requests

api="http://127.0.0.1:8000/predict"


st.title("Insurance premium category predictor")
st.markdown("enter your details below")

age=st.number_input("age",min_value=1,max_value=100,value=20)
weight=st.number_input("weight",min_value=1,max_value=1000,value=30)
height=st.number_input("height",min_value=1,max_value=10,value=2)
income_lpa=st.number_input("lpa",min_value=0,max_value=10,value=2)
smoker=st.selectbox("are you a smoker",options=[True,False])
city=st.text_input("city",value="Mumbai")
occupation=st.selectbox("occupation",['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'])
if st.button("predict premium category"):
    data={
        "age":age,
        "weight":weight,
        "height":height,
        "income_lpa":income_lpa,
        "smoker":smoker,
        "city":city,
        "occupation":occupation
    }
    try:
        response=requests.post(api,json=data)
        if response.status_code==201:
            result=response.json()
            st.success(f"predicted insurance premium category:{result["predicted_category"]}")
        else:
            st.error(f"API error: {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
            st.error("could not connect to fast api server")
        

