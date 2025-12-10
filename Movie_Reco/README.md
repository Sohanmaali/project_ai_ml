# Movie Recommender (Streamlit)

Content-based movie recommender built with Streamlit. It loads precomputed cosine similarity scores to surface the closest titles to a selected movie.

## What this app does
- Simple web UI to select a movie and get top related recommendations.
- Uses precomputed `similarity.pkl` for fast lookup against titles stored in `data.pkl`.
- Lightweight dependencies (Streamlit + pickle data files) so it runs quickly.

## Project structure
- `app.py` – Streamlit UI plus the recommend function.
- `data.pkl` – pandas DataFrame containing at least a `title` column.
- `similarity.pkl` – similarity matrix aligned with the rows in `data.pkl`.
- `requirements.txt` – runtime Python dependencies.

## Setup
1) Install Python 3.9+.
2) (Optional) Create and activate a virtual environment.
3) Install dependencies:
```
pip install -r requirements.txt
```

Ensure `data.pkl` and `similarity.pkl` remain alongside `app.py`.

## Run the app
From the `Movie_Reco` directory:
```
streamlit run app.py
```

Then open the local URL Streamlit prints (typically `http://localhost:8501`).

## Notes
- Recommendations are case-insensitive but rely on an exact title match from `data.pkl`.
- To change the number of returned movies, adjust the default `n` argument in `recommend()` inside `app.py`.

