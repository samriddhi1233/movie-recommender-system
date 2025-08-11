import streamlit as st
import pickle
import pandas as pd
import requests

# ----------- Streamlit Config -----------
st.set_page_config(page_title="Movie Recommender 🎬", layout="wide")

# ----------- Load Data -----------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ----------- Custom CSS Styling -----------
st.markdown("""
    <style>
    body, .main {
        background-color: #FEFAE0;
    }

    .title {
        font-size: 48px;
        font-weight: 800;
        color: #283618;
        text-align: center;
        margin-bottom: 20px;
    }

    .subtext {
        text-align: center;
        font-size: 18px;
        color: #606C38;
        margin-bottom: 30px;
    }

    .stButton > button {
        background-color: #DDA15E;
        color: #FEFAE0;
        border-radius: 10px;
        padding: 10px 24px;
        font-size: 16px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #BC6C25;
        transform: scale(1.05);
    }

    .movie-title {
        text-align: center;
        font-size: 16px;
        font-weight: bold;
        margin: 10px 0;
        color: #283618;
    }

    .movie-card {
        padding: 12px;
        border-radius: 14px;
        background-color: #ffffff;
        box-shadow: 0 4px 10px rgba(40, 54, 24, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease, background-color 0.3s ease;
        text-align: center;
    }

    .movie-card:hover {
        transform: translateY(-8px);
        background-color: #fdf4dc;
        box-shadow: 0 12px 24px rgba(40, 54, 24, 0.2);
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# ----------- Helper Functions -----------
def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=9d7ff68c6cb4bc1c65319c2ca847c002&language=en-US'
        )
        data = response.json()
        poster_path = data.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/300x450?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]]['title'])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_titles, recommended_posters

# ----------- App UI Layout -----------
st.markdown('<div class="title">🎬 Movie Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Get personalized movie recommendations based on your favorite film.</div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox("🎥 Select a movie:", movies['title'].values)

if st.button("Recommend"):
    titles, posters = recommend(selected_movie_name)
    st.markdown("### ✨ You might also like:")

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(posters[idx], use_container_width=True)
            st.markdown(f'<div class="movie-title">{titles[idx]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
