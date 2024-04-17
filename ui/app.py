import streamlit as st
import requests

st.set_page_config(page_title="Sentiment Analysis", layout="wide")
st.title("Test communication with api")

link = st.text_input("Page link")

if st.button("Send POST request"):
    response = requests.post("http://api:5000/link", json={"link":link})
    st.write(response.json().get("message"))
    if response.status_code == 200:
        st.write("OK")
    else:
        st.write("NOT OK")
    dbc = requests.get("http://api:5000/data_count")
    st.write(dbc.json()["db_count"])

if st.button("Make prediction"):
    pred = requests.post("http://api:5000/prediction")
    st.write(pred.json().get("pred"))