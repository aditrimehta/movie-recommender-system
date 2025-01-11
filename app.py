import streamlit as st
import pickle
import pandas as pd
import requests
import time
from functools import lru_cache

poster_cache = {}

def fetch_poster(movie_id):
    if movie_id in poster_cache:  # Check if result is already cached
        return poster_cache[movie_id]

    url = "https://api.themoviedb.org/3/movie/{}?api_key=8289ff784b4f9e87005fe48626008cc9&language=en-US".format(
            movie_id)
    try:
        response = requests.get(url, timeout=5)  # Set a timeout for the request
        response.raise_for_status()
        data = response.json()

        poster_url = "http://image.tmdb.org/t/p/w500/" + data['poster_path']

        # Cache the result
        poster_cache[movie_id] = poster_url
        return poster_url
    except requests.ConnectionError as e:
        #st.error(f"Connection error: {e}")
        return "https://via.placeholder.com/500x750?text=No+Connection"


def recommend(movie):
    movie_index = movieslist[movieslist['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommendedmovies=[]
    recommendedmoviesposter=[]
    for i in movies_list:
        movie_id=movieslist.iloc[i[0]].id
        recommendedmovies.append(movieslist.iloc[i[0]].title)
        recommendedmoviesposter.append(fetch_poster(movie_id))
    return recommendedmovies,recommendedmoviesposter
movieslist=pickle.load(open('movies.pkl','rb'))
movies=movieslist['title'].values
similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommending system')
selected= st.selectbox('pick a movie:',movies)
if st.button('Recommend'):
    name,poster=recommend(selected)

    col1, col2, col3 ,col4,col5= st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])