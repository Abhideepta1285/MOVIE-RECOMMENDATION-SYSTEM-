
# import pickle
# import os
# import time
# import requests
# import streamlit as st

# from dotenv import load_dotenv
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # ---------------- PAGE CONFIG ---------------- #
# st.set_page_config(
#     page_title="Movie Recommendation System",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ---------------- CUSTOM CSS ---------------- #
# st.markdown("""
# <style>
#     /* Overall background */
#     .stApp {
#         background: linear-gradient(180deg, #0f0f1a 0%, #14141f 100%);
#     }

#     /* Main title */
#     .main-title {
#         font-size: 4rem;
#         font-weight: 800;
#         background: linear-gradient(90deg, #ff4b6e, #ff8a4c);
#         -webkit-background-clip: text;
#         -webkit-text-fill-color: transparent;
#         margin-bottom: 0.5rem;
#         text-align: center;
#         line-height: 1.4;
#         letter-spacing: 1px;
#         padding: 2rem 1rem;
#         width: 100%;
#     }

#     /* Sidebar */
#     section[data-testid="stSidebar"] {
#         background-color: #16161f;
#         border-right: 1px solid #2a2a3a;
#     }
#     section[data-testid="stSidebar"] h2, 
#     section[data-testid="stSidebar"] h3 {
#         color: #ff8a4c;
#     }

#     /* Movie cards */
#     .movie-card {
#         background-color: #1b1b28;
#         border-radius: 14px;
#         padding: 10px;
#         text-align: center;
#         transition: transform 0.2s ease, box-shadow 0.2s ease;
#         border: 1px solid #2a2a3a;
#     }
#     .movie-card:hover {
#         transform: translateY(-6px);
#         box-shadow: 0 10px 25px rgba(255, 75, 110, 0.25);
#         border: 1px solid #ff4b6e;
#     }
#     .movie-title {
#         color: #f2f2f5;
#         font-weight: 600;
#         font-size: 0.95rem;
#         margin-top: 8px;
#         min-height: 42px;
#     }

#     /* Buttons */
#     .stButton > button {
#         background: linear-gradient(90deg, #ff4b6e, #ff8a4c);
#         color: white;
#         border: none;
#         border-radius: 8px;
#         padding: 0.6rem 1.2rem;
#         font-weight: 600;
#         width: 100%;
#         transition: opacity 0.2s ease;
#     }
#     .stButton > button:hover {
#         opacity: 0.85;
#         color: white;
#     }

#     /* Selectbox label */
#     .stSelectbox label {
#         color: #d0d0e0 !important;
#         font-weight: 600;
#     }

#     footer {visibility: hidden;}
# </style>
# """, unsafe_allow_html=True)

# # ---------------- LOAD ENV ---------------- #
# load_dotenv()

# def get_api_key():
#     """Resolve TMDB API key from env var, then Streamlit secrets, then fallback."""
#     env_key = os.getenv("TMDB_API_KEY")
#     if env_key:
#         return env_key

#     try:
#         return st.secrets["TMDB_API_KEY"]
#     except Exception:
#         pass

#     return "8265bd1679663a7ea12ac168da84d2e8"


# API_KEY = get_api_key()

# session = requests.Session()


# # ---------------- LOAD DATA ---------------- #
# @st.cache_resource
# def load_data():
#     movies = pickle.load(open("movie_list.pkl", "rb"))

#     cv = CountVectorizer(
#         max_features=5000,
#         stop_words="english"
#     )

#     vectors = cv.fit_transform(movies["tags"]).toarray()

#     similarity = cosine_similarity(vectors)

#     return movies, similarity


# movies, similarity = load_data()


# # ---------------- FETCH MOVIE DETAILS ---------------- #
# def fetch_details(movie_id):
#     """Fetch poster, rating, and release year for a movie."""

#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
#     headers = {"User-Agent": "Mozilla/5.0"}

#     for _ in range(2):
#         try:
#             response = session.get(url, headers=headers, timeout=10)
#             response.raise_for_status()
#             data = response.json()

#             poster_path = data.get("poster_path")
#             poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

#             rating = data.get("vote_average")
#             release_date = data.get("release_date", "")
#             year = release_date.split("-")[0] if release_date else "N/A"

#             return {"poster": poster, "rating": rating, "year": year}

#         except requests.exceptions.ConnectionError:
#             time.sleep(1)

#         except Exception:
#             return {"poster": None, "rating": None, "year": "N/A"}

#     return {"poster": None, "rating": None, "year": "N/A"}


# # ---------------- FETCH TOP RATED MOVIES ---------------- #
# @st.cache_data(ttl=3600)
# def fetch_top_rated(count=5):
#     """Fetch top rated movies directly from TMDB (independent of local dataset)."""

#     url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"
#     headers = {"User-Agent": "Mozilla/5.0"}

#     try:
#         response = session.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
#         results = response.json().get("results", [])

#         top_movies = []

#         for movie in results[:count]:
#             poster_path = movie.get("poster_path")
#             poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

#             release_date = movie.get("release_date", "")
#             year = release_date.split("-")[0] if release_date else "N/A"

#             top_movies.append({
#                 "title": movie.get("title"),
#                 "poster": poster,
#                 "rating": movie.get("vote_average"),
#                 "year": year,
#             })

#         return top_movies

#     except Exception:
#         return []
# def recommend(movie, num_results=5):

#     index = movies[movies["title"] == movie].index[0]

#     distances = sorted(
#         list(enumerate(similarity[index])),
#         reverse=True,
#         key=lambda x: x[1]
#     )

#     recommendations = []

#     for item in distances[1:num_results + 1]:

#         movie_index = item[0]
#         details = fetch_details(int(movies.iloc[movie_index].movie_id))

#         recommendations.append({
#             "title": movies.iloc[movie_index].title,
#             "poster": details["poster"],
#             "rating": details["rating"],
#             "year": details["year"],
#         })

#     return recommendations


# # ---------------- SIDEBAR ---------------- #
# with st.sidebar:
#     st.markdown("## 🎬 CineMatch AI")
#     st.markdown("Discover movies similar to your favorites using content-based filtering.")

#     st.markdown("---")
#     st.markdown("### ⚙️ Settings")

#     num_results = st.slider(
#         "Number of recommendations",
#         min_value=3,
#         max_value=10,
#         value=5
#     )

#     show_ratings = st.checkbox("Show ratings & year", value=True)

#     st.markdown("---")
#     st.markdown("### 🔍 Quick Search")
#     search_term = st.text_input("Filter movie list", placeholder="e.g. Batman")

#     st.markdown("---")
#     st.markdown("### ℹ️ About")
#     st.markdown(
#         "Built with **Streamlit** + **scikit-learn** cosine similarity "
#         "on movie tags. Posters & metadata via **TMDB API**."
#     )

# # ---------------- MAIN HEADER ---------------- #
# st.markdown('<h1 class="main-title">✨ CineMatch AI – Intelligent Movie Recommendation System ⭐ ✨</h1> ', unsafe_allow_html=True)

# # ---------------- MOVIE LIST (filtered by sidebar search) ---------------- #
# movie_titles = movies["title"].values

# if search_term:
#     filtered_titles = [t for t in movie_titles if search_term.lower() in t.lower()]
#     if not filtered_titles:
#         st.warning("No movies match your search. Showing full list instead.")
#         filtered_titles = movie_titles
# else:
#     filtered_titles = movie_titles

# # ---------------- UI ---------------- #
# col_select, col_button = st.columns([4, 1])

# with col_select:
#     selected_movie = st.selectbox(
#         "Select a Movie",
#         filtered_titles
#     )

# with col_button:
#     st.markdown("<br>", unsafe_allow_html=True)
#     recommend_clicked = st.button("✨ Recommend")

# # ---------------- TOP RATED SECTION (shown before any recommendation) ---------------- #
# if not recommend_clicked:

#     st.markdown("### 🔥 Top Rated Movies")

#     with st.spinner("Loading top rated movies..."):
#         top_rated = fetch_top_rated(5)

#     if top_rated:
#         top_cols = st.columns(5)

#         for col, movie in zip(top_cols, top_rated):
#             with col:
#                 st.markdown('<div class="movie-card">', unsafe_allow_html=True)

#                 if movie["poster"]:
#                     st.image(movie["poster"], use_container_width=True)
#                 else:
#                     st.write("🎞️ Poster Not Available")

#                 st.markdown(f'<div class="movie-title">{movie["title"]}</div>', unsafe_allow_html=True)

#                 if show_ratings:
#                     rating_display = f"⭐ {movie['rating']:.1f}" if movie["rating"] else "⭐ N/A"
#                     st.caption(f"{rating_display}  •  📅 {movie['year']}")

#                 st.markdown('</div>', unsafe_allow_html=True)
#     else:
#         st.info("Couldn't load top rated movies right now.")

# if recommend_clicked:

#     with st.spinner("Finding similar movies..."):
#         recommendations = recommend(selected_movie, num_results)

#     st.markdown("### Recommended for you")

#     cols = st.columns(min(num_results, 5))

#     for i, movie in enumerate(recommendations):

#         col = cols[i % len(cols)]

#         with col:
#             st.markdown('<div class="movie-card">', unsafe_allow_html=True)

#             if movie["poster"]:
#                 st.image(movie["poster"], use_container_width=True)
#             else:
#                 st.write("🎞️ Poster Not Available")

#             st.markdown(f'<div class="movie-title">{movie["title"]}</div>', unsafe_allow_html=True)

#             if show_ratings:
#                 rating_display = f"⭐ {movie['rating']:.1f}" if movie["rating"] else "⭐ N/A"
#                 st.caption(f"{rating_display}  •  📅 {movie['year']}")

#             st.markdown('</div>', unsafe_allow_html=True)

#         # wrap to new row every 5 items if num_results > 5
#         if (i + 1) % 5 == 0 and (i + 1) < len(recommendations):
#             cols = st.columns(min(num_results - (i + 1), 5))




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
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
    /* Overall background */
    .stApp {
        background: linear-gradient(180deg, #0f0f1a 0%, #14141f 100%);
    }

    /* Main title */
    .main-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ff4b6e, #ff8a4c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: center;
        line-height: 1.4;
        letter-spacing: 1px;
        padding: 2rem 1rem;
        width: 100%;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #16161f;
        border-right: 1px solid #2a2a3a;
    }
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #ff8a4c;
    }

    /* Movie cards */
    .movie-card {
        background-color: #1b1b28;
        border-radius: 14px;
        padding: 10px;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #2a2a3a;
    }
    .movie-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 10px 25px rgba(255, 75, 110, 0.25);
        border: 1px solid #ff4b6e;
    }
    .movie-title {
        color: #f2f2f5;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 8px;
        min-height: 42px;
    }

    /* Genre badges */
    .genre-wrap {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 4px;
        margin: 6px 0 4px 0;
        min-height: 24px;
    }
    .genre-badge {
        background-color: rgba(255, 75, 110, 0.15);
        color: #ff9fb3;
        border: 1px solid rgba(255, 75, 110, 0.35);
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 0.7rem;
        font-weight: 600;
        white-space: nowrap;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #ff4b6e, #ff8a4c);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        width: 100%;
        transition: opacity 0.2s ease;
    }
    .stButton > button:hover {
        opacity: 0.85;
        color: white;
    }

    /* Trailer link-button */
    .stLinkButton > a {
        background: linear-gradient(90deg, #ff0000, #cc0000) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
        justify-content: center !important;
    }
    .stLinkButton > a:hover {
        opacity: 0.85;
    }

    /* Selectbox label */
    .stSelectbox label {
        color: #d0d0e0 !important;
        font-weight: 600;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD ENV ---------------- #
load_dotenv()

def get_api_key():
    """Resolve TMDB API key from env var, then Streamlit secrets, then fallback."""
    env_key = os.getenv("TMDB_API_KEY")
    if env_key:
        return env_key

    try:
        return st.secrets["TMDB_API_KEY"]
    except Exception:
        pass

    return "8265bd1679663a7ea12ac168da84d2e8"


API_KEY = get_api_key()

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


def _extract_trailer(videos_payload):
    """Pick the best YouTube trailer/teaser key from a videos.results payload."""
    results = videos_payload.get("results", []) if videos_payload else []

    # Prefer an official YouTube trailer
    for v in results:
        if v.get("site") == "YouTube" and v.get("type") == "Trailer":
            return v.get("key")

    # Fall back to a YouTube teaser
    for v in results:
        if v.get("site") == "YouTube" and v.get("type") == "Teaser":
            return v.get("key")

    # Fall back to any YouTube video
    for v in results:
        if v.get("site") == "YouTube":
            return v.get("key")

    return None


# ---------------- FETCH MOVIE DETAILS ---------------- #
@st.cache_data(ttl=3600)
def fetch_details(movie_id):
    """Fetch poster, rating, release year, genres, and trailer link for a movie."""

    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={API_KEY}&language=en-US&append_to_response=videos"
    )
    headers = {"User-Agent": "Mozilla/5.0"}

    for _ in range(2):
        try:
            response = session.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            poster_path = data.get("poster_path")
            poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            rating = data.get("vote_average")
            release_date = data.get("release_date", "")
            year = release_date.split("-")[0] if release_date else "N/A"

            genres = [g["name"] for g in data.get("genres", [])][:3]

            trailer_key = _extract_trailer(data.get("videos"))
            trailer_url = f"https://www.youtube.com/watch?v={trailer_key}" if trailer_key else None

            return {
                "poster": poster,
                "rating": rating,
                "year": year,
                "genres": genres,
                "trailer_url": trailer_url,
            }

        except requests.exceptions.ConnectionError:
            time.sleep(1)

        except Exception:
            return {
                "poster": None,
                "rating": None,
                "year": "N/A",
                "genres": [],
                "trailer_url": None,
            }

    return {
        "poster": None,
        "rating": None,
        "year": "N/A",
        "genres": [],
        "trailer_url": None,
    }


# ---------------- FETCH TOP RATED MOVIES ---------------- #
@st.cache_data(ttl=3600)
def fetch_top_rated(count=5):
    """Fetch top rated movies directly from TMDB (independent of local dataset)."""

    url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=en-US&page=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json().get("results", [])

        top_movies = []

        for movie in results[:count]:
            # Reuse fetch_details so genres + trailer come from the same
            # cached call pattern as the recommendation cards.
            details = fetch_details(movie.get("id"))

            top_movies.append({
                "title": movie.get("title"),
                "poster": details["poster"],
                "rating": details["rating"],
                "year": details["year"],
                "genres": details["genres"],
                "trailer_url": details["trailer_url"],
            })

        return top_movies

    except Exception:
        return []


def recommend(movie, num_results=5):

    index = movies[movies["title"] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommendations = []

    for item in distances[1:num_results + 1]:

        movie_index = item[0]
        details = fetch_details(int(movies.iloc[movie_index].movie_id))

        recommendations.append({
            "title": movies.iloc[movie_index].title,
            "poster": details["poster"],
            "rating": details["rating"],
            "year": details["year"],
            "genres": details["genres"],
            "trailer_url": details["trailer_url"],
        })

    return recommendations


# ---------------- CARD RENDERER ---------------- #
def render_movie_card(movie, show_ratings):
    """Render a single movie card: poster, genres, title, rating/year, trailer button."""

    st.markdown('<div class="movie-card">', unsafe_allow_html=True)

    if movie["poster"]:
        st.image(movie["poster"], use_container_width=True)
    else:
        st.write("🎞️ Poster Not Available")

    if movie.get("genres"):
        badges = "".join(f'<span class="genre-badge">{g}</span>' for g in movie["genres"])
        st.markdown(f'<div class="genre-wrap">{badges}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="genre-wrap"></div>', unsafe_allow_html=True)

    st.markdown(f'<div class="movie-title">{movie["title"]}</div>', unsafe_allow_html=True)

    if show_ratings:
        rating_display = f"⭐ {movie['rating']:.1f}" if movie["rating"] else "⭐ N/A"
        st.caption(f"{rating_display}  •  📅 {movie['year']}")

    if movie.get("trailer_url"):
        st.link_button("▶ Watch Trailer", movie["trailer_url"])
    else:
        st.caption("Trailer not available")

    st.markdown('</div>', unsafe_allow_html=True)


# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.markdown("## 🎬 CineMatch AI")
    st.markdown("Discover movies similar to your favorites using content-based filtering.")

    st.markdown("---")
    st.markdown("### ⚙️ Settings")

    num_results = st.slider(
        "Number of recommendations",
        min_value=3,
        max_value=10,
        value=5
    )

    show_ratings = st.checkbox("Show ratings & year", value=True)

    st.markdown("---")
    st.markdown("### 🔍 Quick Search")
    search_term = st.text_input("Filter movie list", placeholder="e.g. Batman")

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown(
        "Built with **Streamlit** + **scikit-learn** cosine similarity "
        "on movie tags. Posters, genres & trailers via **TMDB API**."
    )

# ---------------- MAIN HEADER ---------------- #
st.markdown('<h1 class="main-title">✨ CineMatch AI – Intelligent Movie Recommendation System ⭐ ✨</h1> ', unsafe_allow_html=True)

# ---------------- MOVIE LIST (filtered by sidebar search) ---------------- #
movie_titles = movies["title"].values

if search_term:
    filtered_titles = [t for t in movie_titles if search_term.lower() in t.lower()]
    if not filtered_titles:
        st.warning("No movies match your search. Showing full list instead.")
        filtered_titles = movie_titles
else:
    filtered_titles = movie_titles

# ---------------- UI ---------------- #
col_select, col_button = st.columns([4, 1])

with col_select:
    selected_movie = st.selectbox(
        "Select a Movie",
        filtered_titles
    )

with col_button:
    st.markdown("<br>", unsafe_allow_html=True)
    recommend_clicked = st.button("✨ Recommend")

# ---------------- TOP RATED SECTION (shown before any recommendation) ---------------- #
if not recommend_clicked:

    st.markdown("### 🔥 Top Rated Movies")

    with st.spinner("Loading top rated movies..."):
        top_rated = fetch_top_rated(5)

    if top_rated:
        top_cols = st.columns(5)

        for col, movie in zip(top_cols, top_rated):
            with col:
                render_movie_card(movie, show_ratings)
    else:
        st.info("Couldn't load top rated movies right now.")

if recommend_clicked:

    with st.spinner("Finding similar movies..."):
        recommendations = recommend(selected_movie, num_results)

    st.markdown("### Recommended for you")

    cols = st.columns(min(num_results, 5))

    for i, movie in enumerate(recommendations):

        col = cols[i % len(cols)]

        with col:
            render_movie_card(movie, show_ratings)

        # wrap to new row every 5 items if num_results > 5
        if (i + 1) % 5 == 0 and (i + 1) < len(recommendations):
            cols = st.columns(min(num_results - (i + 1), 5))