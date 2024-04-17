import streamlit as st
import requests
from collections import Counter
import plotly.graph_objs as go
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sentiment Analysis", layout="wide")
st.title("Sentiment Analysis App")

if 'com_count' not in st.session_state:
    st.session_state.com_count = 0

if 'sen_count' not in st.session_state:
    st.session_state.sen_count = 0

if 'pred' not in st.session_state:
    st.session_state.pred = 0

if 'coms' not in st.session_state:
    st.session_state.coms = 0

if 'pred_all' not in st.session_state:
    pred_all = requests.get("http://api:5000/get_data")
    if len(pred_all.json().get("db_content"))!=0:
        st.session_state.pred_all = pred_all.json().get("db_content")
    else:
        st.session_state.pred_all = 0

link = st.text_input("Page link")

c1,c2,c3 = st.columns(3)

with c1:
    if st.button("Scrape thread"):
        response = requests.post("http://api:5000/link", json={"link":link})
with c2:
    if st.button("Make prediction"):
        pred = requests.post("http://api:5000/prediction")
        pred_all = requests.get("http://api:5000/get_data")
        st.session_state.pred_all = pred_all.json().get("db_content")
        st.session_state.pred = pred.json().get("pred")
with c3:
    if st.button("Clear sentiment database"):
        requests.post("http://api:5000/db_clear")
        st.session_state.pred_all = 0

com_count = requests.get("http://api:5000/comments_count")
st.session_state.com_count = com_count.json().get("db_count")

sen_count = requests.get("http://api:5000/sentiment_count")
st.session_state.sen_count = sen_count.json().get("db_count")

c1,c2 = st.columns(2)

with c1:
    st.metric("Comments in database", st.session_state.com_count)
with c2:
    st.metric("Predictions in database", st.session_state.sen_count)


coms = requests.get("http://api:5000/get_comments").json().get("db_content")
if len(coms)!=0:
    st.session_state.coms = coms
try:
    stop_words = ["https", "co", "RT"] + list(STOPWORDS)
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="#0E1117", stopwords = stop_words).generate(str(st.session_state.coms))
    # Create a figure and axis
    fig, ax = plt.subplots()

    # Plot the word cloud
    ax.imshow(wordcloud, interpolation="bilinear")
    fig.set_facecolor('#0E1117') 
    ax.set_title("4chan thread Wordcloud", color = "white")
    ax.axis("off")

    # Display the plot using Streamlit
    st.pyplot(fig)
except:
    st.info("To generate Wordcloud you need to scrape some threads.", icon="ℹ️")

try:
    data_counter = Counter(st.session_state.pred)

    # Extracting labels and counts
    labels = list(data_counter.keys())
    counts = list(data_counter.values())

    sorted_indices = sorted(range(len(labels)), key=lambda i: labels[i])
    labels = [labels[i] for i in sorted_indices]
    counts = [counts[i] for i in sorted_indices]

    total_count = sum(counts)
    percentages = [f'{count / total_count * 100:.2f}%' for count in counts]

    layout = go.Layout(title='Bar Plot of 4chan posts sentiment from scrapped threads')

    # Creating a bar plot
    bar_plot = go.Bar(x=labels, y=counts, text=percentages, textposition='inside', textfont=dict(size=26, color='black'))
    fig = go.Figure(data=[bar_plot], layout=layout)

    st.plotly_chart(fig, use_container_width=True)
except:
    st.info("To generate barplot you need to scrape some threads and make prediction.", icon="ℹ️")

try:
    data_counter = Counter(st.session_state.pred_all)

    # Extracting labels and counts
    labels = list(data_counter.keys())
    counts = list(data_counter.values())

    sorted_indices = sorted(range(len(labels)), key=lambda i: labels[i])
    labels = [labels[i] for i in sorted_indices]
    counts = [counts[i] for i in sorted_indices]

    total_count = sum(counts)
    percentages = [f'{count / total_count * 100:.2f}%' for count in counts]

    layout = go.Layout(title='Bar Plot of 4chan posts sentiment from database')

    # Creating a bar plot
    bar_plot = go.Bar(x=labels, y=counts, text=percentages, textposition='inside', textfont=dict(size=26, color='black'))
    fig = go.Figure(data=[bar_plot], layout=layout)

    st.plotly_chart(fig, use_container_width=True)
except:
    st.info("To generate barplot you need to have some predictions in database.", icon="ℹ️")