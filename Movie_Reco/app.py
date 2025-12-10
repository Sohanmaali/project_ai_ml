import streamlit as st
import pickle

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")

st.title("🎬 Movie Recommendation System")
st.write("Content-based movie recommender using cosine similarity")

# ------------------ LOAD DATA ------------------
new_data = pickle.load(open("data.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# Precompute lookup (important for speed)
title_to_index = {title.lower(): idx for idx, title in enumerate(new_data["title"])}


# ------------------ RECOMMENDER ------------------
def recommend(movie, n=5):
    movie = movie.lower()

    if movie not in title_to_index:
        return []

    idx = title_to_index[movie]
    distances = similarity[idx]

    movie_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[
        1 : n + 1
    ]

    return [new_data.iloc[i[0]].title for i in movie_list]


# ------------------ UI ------------------
selected_movie = st.selectbox("Select a movie", new_data["title"].values)

if st.button("Recommend"):
    recommendations = recommend(selected_movie)

    if len(recommendations) == 0:
        st.error("Movie not found")
    else:
        st.subheader("✅ Recommended Movies")
        for movie in recommendations:
            st.write("👉", movie)
