# Reel Match — Movie Recommender (Flask)

A content-based movie recommender system served via Flask, with a
movie-theater themed web UI ("Reel Match"). It builds a TF-IDF vector for
each movie's genres + overview and recommends similar movies using cosine
similarity. The trained model is saved/loaded as a **`.pkl`** file.

## Project structure

```
movie_recommender/
├── app.py                 # Flask application & API routes
├── train_model.py         # Trains the model and saves model/movie_recommender.pkl
├── requirements.txt       # Python dependencies
├── data/
│   └── movies.csv         # Sample movie dataset (50 movies)
├── model/
│   ├── __init__.py
│   ├── recommender.py      # Loads the .pkl model (or trains if missing)
│   └── movie_recommender.pkl  # Trained TF-IDF + cosine similarity model
└── templates/
    └── index.html          # Movie-theater themed web UI ("Reel Match")
```

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Train the model (creates `model/movie_recommender.pkl`):
   ```bash
   python train_model.py
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Open your browser at: http://127.0.0.1:5000

> Note: if `model/movie_recommender.pkl` doesn't exist yet, the app will
> automatically train the model on startup and save it for next time, so
> step 3 is optional but recommended.

## Using your own dataset

Replace `data/movies.csv` with your own data. It must contain at least
these columns:

- `movieId` — unique identifier
- `title` — movie title
- `genres` — space or pipe separated genre tags
- `overview` — short text description / plot summary

After replacing the dataset, re-run `python train_model.py` to regenerate
`model/movie_recommender.pkl`.

## Web UI

- **Now Showing** — a poster grid of randomly featured movies (click a
  poster to get recommendations based on it).
- **Find Your Next Movie** — search box to enter any title in the dataset.
- **Results** — ranked recommendation "ticket stubs" each showing the
  movie title, genres, and a **Match Confidence** bar (the model's
  similarity score expressed as a percentage).
- A small badge under the title shows whether the `.pkl` model was loaded
  successfully and how many movies it was trained on.

## API Endpoints

### `GET /api/movies`
Returns all movie titles in the dataset.

```json
{ "movies": ["The Shawshank Redemption", "The Godfather", "..."] }
```

### `GET /api/featured`
Returns a small random selection of movies (with poster emoji/colors) for
the "Now Showing" grid.

### `GET /api/search?q=<query>`
Search for titles containing the given text (case-insensitive).

```json
{ "results": ["Inception", "Inside Out"] }
```

### `GET /api/recommend?title=<title>&n=<top_n>`
### `POST /api/recommend`  with JSON body `{"title": "...", "top_n": 5}`

Returns the top-N most similar movies, including a `confidence` score
(0–100).

```json
{
  "title": "Inception",
  "recommendations": [
    {
      "movieId": 7,
      "title": "The Matrix",
      "genres": "Action Sci-Fi",
      "score": 0.3127,
      "confidence": 31.3,
      "poster_emoji": "🚀",
      "poster_gradient": ["#2f6f9e", "#0e2433"]
    }
  ]
}
```

If the title isn't found, returns HTTP 404 with an `error` message.

### `GET /api/health`
Health check, returns model status:

```json
{
  "status": "ok",
  "model_loaded": true,
  "model_source": "movie_recommender.pkl",
  "movie_count": 50
}
```

## Retraining with your own model

If you already have a different trained recommender (e.g. collaborative
filtering, matrix factorization), you can build your own
`model/movie_recommender.pkl` as long as `model/recommender.py` knows how
to load and use it — or replace the contents of `model/recommender.py`
entirely. As long as `MovieRecommender.recommend(title, top_n)` returns a
list of dicts with `movieId`, `title`, `genres`, `score`/`confidence`,
`poster_emoji`, and `poster_gradient`, no other files need to change.

## Deployment notes

- For production, run with a WSGI server, e.g.:
  ```bash
  pip install gunicorn
  gunicorn -w 2 -b 0.0.0.0:8000 app:app
  ```
- Set `debug=False` in `app.py` (or use environment-based config) before
  deploying.
