import streamlit as st
import requests

st.set_page_config(page_title="Sentiment Analysis", layout="wide")
st.title("Sentiment Analysis App")

if 'com_count' not in st.session_state:
    st.session_state.com_count = 0

if 'sen_count' not in st.session_state:
    st.session_state.sen_count = 0

if 'pred' not in st.session_state:
    st.session_state.pred = 0

if 'pred_all' not in st.session_state:
    pred_all = requests.get("http://api:5000/get_data")
    st.session_state.pred_all = pred_all.json().get("db_content")

link = st.text_input("Page link")

c1,c2 = st.columns(2)

with c1:
    if st.button("Scrape thread"):
        response = requests.post("http://api:5000/link", json={"link":link})
        # st.write(response.json().get("message"))
        # if response.status_code == 200:
        #     st.write("OK")
        # else:
        #     st.write("NOT OK")
with c2:
    if st.button("Make prediction"):
        pred = requests.post("http://api:5000/prediction")
        pred_all = requests.get("http://api:5000/get_data")
        st.session_state.pred_all = pred_all.json().get("db_content")

com_count = requests.get("http://api:5000/comments_count")
st.session_state.com_count = com_count.json().get("db_count")

# sen_count = requests.get("http://api:5000/sentiment_count")
# st.session_state.sen_count = sen_count.json().get("db_count")

c1,c2 = st.columns(2)

with c1:
    st.metric("Comments in database", st.session_state.com_count)
with c2:
    st.metric("Predictions in database", len(st.session_state.pred_all))