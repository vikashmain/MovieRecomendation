
import os
import gzip
import pickle
import streamlit as st
import requests
import pandas as pd
import gdown


st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)


API_KEY = "33ce3e04"


FILE_ID = "19-ptxicu7fW4gckWqydpKtRYacw_aDR9"
MODEL_FILE = "similarity.pkl.gz"


if not os.path.exists(MODEL_FILE):
    gdown.download(
        id=FILE_ID,
        output=MODEL_FILE,
        quiet=False
    )


@st.cache_data(show_spinner=False)
def fetch_poster(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["Response"] == "True" and data["Poster"] != "N/A":
            return data["Poster"]
    except:
        pass

    return "https://via.placeholder.com/300x450?text=No+Poster"


def recommend(movie):

    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        key=lambda x: x[1],
        reverse=True
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        title = movies.iloc[i[0]].title

        recommended_movie_names.append(title)
        recommended_movie_posters.append(fetch_poster(title))

    return recommended_movie_names, recommended_movie_posters



st.title("🎬 Movie Recommender System")


movies_data = pickle.load(open("movies_list.pkl", "rb"))

with gzip.open(MODEL_FILE, "rb") as f:
    similarity = pickle.load(f)

if isinstance(movies_data, dict):
    movies = pd.DataFrame(movies_data)
else:
    movies = movies_data

movie_list = movies["title"].values

selected_movie = st.selectbox(
    "Type or select a movie",
    movie_list
)


if st.button("Show Recommendation"):

    with st.spinner("Finding similar movies..."):

        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.subheader("Top 5 Recommended Movies")

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            st.image(
                recommended_movie_posters[i],
                width=220
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#f8f9fa;
                    border-radius:10px;
                    padding:10px;
                    margin-top:8px;
                    text-align:center;
                    min-height:70px;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    box-shadow:0px 2px 6px rgba(0,0,0,0.15);
                ">
                    <b>{recommended_movie_names[i]}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
