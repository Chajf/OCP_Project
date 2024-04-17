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

# st.write(Counter(st.session_state.pred_all))

coms = requests.get("http://api:5000/get_comments").json().get("db_content")
stop_words = ["https", "co", "RT"] + list(STOPWORDS)
positive_wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", stopwords = stop_words).generate(str(coms))
# Create a figure and axis
fig, ax = plt.subplots()

# Plot the word cloud
ax.imshow(positive_wordcloud, interpolation="bilinear")
ax.set_title("4chan thread Wordcloud")
ax.axis("off")

# Display the plot using Streamlit
st.pyplot(fig)

# Sample Counter object
data_counter = Counter(st.session_state.pred_all)

# Extracting labels and counts
labels = list(data_counter.keys())
counts = list(data_counter.values())

layout = go.Layout(title='Bar Plot of 4chan posts sentiment')

# Creating a bar plot
bar_plot = go.Bar(x=labels, y=counts)
fig = go.Figure(data=[bar_plot], layout=layout)

st.plotly_chart(fig, use_container_width=True)