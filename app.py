import os
import pickle
import streamlit as st
import requests
import pandas as pd
import gdown

# ==============================
# OMDb API Key
# ==============================
API_KEY = "33ce3e04"


GOOGLE_DRIVE_LINK = "https://drive.google.com/file/d/1y6pESS5R6mliVNy9u1AbhEtmVkZH-trM/view?usp=sharing"


if not os.path.exists("similarity.pkl"):
    with st.spinner("Downloading recommendation model... Please wait."):
        gdown.download(
            url=GOOGLE_DRIVE_LINK,
            output="similarity.pkl",
            fuzzy=True
        )



@st.cache_data(show_spinner=False)
def fetch_poster(movie_name):

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=3)
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
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:

        movie_title = movies.iloc[i[0]].title

        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_title))

    return recommended_movie_names, recommended_movie_posters



st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommender System")


movies_data = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

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

        recommended_movie_names, recommended_movie_posters = recommend(
            selected_movie
        )

    st.subheader("Top 5 Recommended Movies")

    cols = st.columns(5)

    for idx, col in enumerate(cols):

        with col:

            st.image(
                recommended_movie_posters[idx],
                use_column_width=True
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
                    <b>{recommended_movie_names[idx]}</b>
                </div>
                """,
                unsafe_allow_html=True
            )
