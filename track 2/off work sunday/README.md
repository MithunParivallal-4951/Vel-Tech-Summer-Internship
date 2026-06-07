# Movie Recommendation Model

This project recommends movies using TF-IDF text features and cosine similarity.

## Dataset

The code is configured for this dataset:

```text
C:/Users/Mithun/OneDrive/Desktop/git hub folder/Vel-Tech-Summer-Internship/Day 3/16k_Movies-mat-csv.csv
```

It uses these columns:

```text
Title, Description, Genres, Directed by, Written by
```

## Install

No external packages are required. You only need Python.

## Train Model

```bash
python train_model.py
```

This creates:

```text
movie_recommender.pkl
```

## Recommend Movies

```bash
python recommend_movie.py "Tokyo Story" --limit 5
```

## Search Movie Titles

```bash
python recommend_movie.py --search "three colors" --limit 10
```

## Use In Python

```python
from recommender import MovieRecommender

model = MovieRecommender.load("movie_recommender.pkl")
results = model.recommend("Tokyo Story", limit=5)

for movie in results:
    print(movie["title"], movie["similarity_score"])
```

## Direct Run Without Saving

You can also build and search in one command:

```bash
python recommender.py "Tokyo Story" --limit 5
```
