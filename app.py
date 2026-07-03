# import pickle
# import time
# import requests
# import streamlit as st

# # ---------------- CONFIG ---------------- #


# from dotenv import load_dotenv
# import os

# load_dotenv()

# API_KEY = os.getenv("TMDB_API_KEY")

# st.set_page_config(page_title="Movie Recommendation System", layout="wide")

# # Reuse the same HTTP connection
# session = requests.Session()


# # ---------------- FETCH POSTER ---------------- #
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }

#     # Retry twice if connection fails
#     for _ in range(2):
#         try:
#             response = session.get(
#                 url,
#                 headers=headers,
#                 timeout=10
#             )

#             response.raise_for_status()

#             data = response.json()

#             poster_path = data.get("poster_path")

#             if poster_path:
#                 return f"https://image.tmdb.org/t/p/w500{poster_path}"

#             return None

#         except requests.exceptions.ConnectionError:
#             time.sleep(1)

#         except Exception as e:
#             print(e)
#             return None

#     return None


# # ---------------- RECOMMEND ---------------- #
# def recommend(movie):
#     index = movies[movies["title"] == movie].index[0]

#     distances = sorted(
#         list(enumerate(similarity[index])),
#         reverse=True,
#         key=lambda x: x[1]
#     )

#     recommended_movies = []

#     for item in distances[1:6]:

#         movie_index = item[0]

#         movie_id = int(movies.iloc[movie_index].movie_id)

#         recommended_movies.append(
#             {
#                 "title": movies.iloc[movie_index].title,
#                 "poster": fetch_poster(movie_id)
#             }
#         )

#     return recommended_movies


# # ---------------- LOAD MODEL ---------------- #
# movies = pickle.load(open("movie_list.pkl", "rb"))
# similarity = pickle.load(open("similarity.pkl", "rb"))


# # ---------------- UI ---------------- #
# st.title("🎬 Movie Recommendation System")

# selected_movie = st.selectbox(
#     "Select a Movie",
#     movies["title"].values
# )

# if st.button("Recommend"):

#     recommendations = recommend(selected_movie)

#     cols = st.columns(5)

#     for col, movie in zip(cols, recommendations):

#         with col:

#             st.markdown(f"**{movie['title']}**")

#             if movie["poster"]:
#                 st.image(movie["poster"], use_container_width=True)
#             else:
#                 st.write("Poster not available")


import pickle
import os
import time
import requests
import streamlit as st

from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")

# ---------------- LOAD ENV ---------------- #
load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

session = requests.Session()

# ---------------- LOAD DATA ---------------- #
@st.cache_resource
def load_data():
    movies = pickle.load(open("movie_list.pkl", "rb"))

    cv = CountVectorizer(
        max_features=5000,
        stop_words="english"
    )

    vectors = cv.fit_transform(movies["tags"]).toarray()

    similarity = cosine_similarity(vectors)

    return movies, similarity


movies, similarity = load_data()


# ---------------- FETCH POSTER ---------------- #
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for _ in range(2):

        try:

            response = session.get(
                url,
                headers=headers,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

            return None

        except requests.exceptions.ConnectionError:
            time.sleep(1)

        except Exception:
            return None

    return None


# ---------------- RECOMMEND ---------------- #
def recommend(movie):

    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []

    for item in distances[1:6]:

        movie_index = item[0]

        recommendations.append({
            "title": movies.iloc[movie_index].title,
            "poster": fetch_poster(
                int(movies.iloc[movie_index].movie_id)
            )
        })

    return recommendations


# ---------------- UI ---------------- #
selected_movie = st.selectbox(
    "Select a Movie",
    movies["title"].values
)

if st.button("Recommend"):

    with st.spinner("Finding similar movies..."):

        recommendations = recommend(selected_movie)

    cols = st.columns(5)

    for col, movie in zip(cols, recommendations):

        with col:

            st.markdown(f"**{movie['title']}**")

            if movie["poster"]:
                st.image(
                    movie["poster"],
                    use_container_width=True
                )
            else:
                st.write("Poster Not Available")