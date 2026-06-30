# import pickle
# import streamlit as st
# import requests
# import pandas as pd

# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
    
#     for i in distances[1:6]:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_names.append(movies.iloc[i[0]].title)

#     return recommended_movie_names, recommended_movie_posters


# # Set page layout to wide for better horizontal display
# st.set_page_config(layout="wide")

# st.header('🎬 Movie Recommender System')

# # Load files safely
# movies_data = pickle.load(open('movies_list.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# if isinstance(movies_data, dict):
#     movies = pd.DataFrame(movies_data)
# else:
#     movies = movies_data

# movie_list = movies['title'].values
# selected_movie = st.selectbox(
#     "Type or select a movie from the dropdown",
#     movie_list
# )

# if st.button('Show Recommendation'):
#     with st.spinner('Fetching recommendations...'):
#         recommended_movie_names, _ = recommend(selected_movie)
    
#     st.write("### Here are your top recommendations:")
    
#     # Create 5 clean columns
#     cols = st.columns(5)
    
#     for idx, col in enumerate(cols):
#         with col:
#             # Custom HTML styling for a beautiful modern card layout
#             card_style = """
#             <div style="
#                 background-color: #f8f9fa;
#                 border: 1px solid #e0e0e0;
#                 border-radius: 10px;
#                 padding: 20px;
#                 text-align: center;
#                 box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
#                 min-height: 120px;
#                 display: flex;
#                 align-items: center;
#                 justify-content: center;
#             ">
#                 <h4 style="margin: 0; color: #2C3E50; font-family: sans-serif; font-size: 16px;">
#                     {}
#                 </h4>
#             </div>
#             """.format(recommended_movie_names[idx])
            
#             # Render the styled card
#             st.markdown(card_style, unsafe_allow_html=True)






import pickle
import streamlit as st
import requests
import pandas as pd

# ==============================
# OMDb API Key
# ==============================
API_KEY = "33ce3e04"


# ==============================
# Function to fetch movie poster
# ==============================
def fetch_poster(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        if data["Response"] == "True" and data["Poster"] != "N/A":
            return data["Poster"]

    except:
        pass

    # Default image if no poster is found
    return "https://via.placeholder.com/300x450?text=No+Poster"


# ==============================
# Recommendation Function
# ==============================
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

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


# ==============================
# Streamlit Page
# ==============================
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommender System")

# ==============================
# Load Data
# ==============================
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

# ==============================
# Recommendation Button
# ==============================
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
            use_column_width=True)

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