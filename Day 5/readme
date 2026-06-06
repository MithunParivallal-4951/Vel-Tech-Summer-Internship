# CineProphet

## Project Overview

CineProphet is a content-based movie recommendation system developed using Python and Machine Learning techniques. The system recommends movies similar to a user's selected movie by analyzing movie descriptions, genres, directors, and writers.

## Problem Statement

With thousands of movies available across different platforms, users often struggle to discover movies that match their interests. CineProphet solves this problem by recommending similar movies based on their content and characteristics.

## Dataset Source

16K Movies Dataset

Dataset Features:
- Title
- Release Date
- Description
- Rating
- Number of Persons Voted
- Directed by
- Written by
- Duration
- Genres

Total Records: 16,290 Movies

## Features Used

The recommendation engine uses:

- Movie Description
- Genres
- Director
- Writer

These features are combined into a single "tags" column for similarity analysis.

## Algorithm Used

### CountVectorizer
Converts movie tags into numerical vectors.

### Cosine Similarity
Calculates similarity scores between movies and recommends the most similar movies.

## Project Workflow

1. Load Dataset
2. Perform Exploratory Data Analysis (EDA)
3. Handle Missing Values
4. Create Tags Column
5. Convert Text to Vectors using CountVectorizer
6. Generate Similarity Matrix using Cosine Similarity
7. Build Recommendation Function
8. Save Model Files using Pickle
9. Visualize Dataset
10. Deploy using Flask

## Visualizations

The following visualizations were generated:

- Rating Distribution
- Top 10 Movie Genres
- Correlation Heatmap

## Files Generated

- movies.pkl
- similarity.pkl
- rating_distribution.png
- top_genres.png
- heatmap.png

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Seaborn
- Pickle
- Flask
- HTML
- CSS
- JavaScript
- SQLite

## Accuracy Achieved

This project is a recommendation system and does not use classification accuracy.

Performance is evaluated using cosine similarity scores that identify the most relevant movies based on content similarity.

## How to Run the Project

### Install Required Libraries

```bash
pip install pandas numpy scikit-learn matplotlib seaborn flask
```

### Run the Recommendation System

```bash
python movie_recommendation.py
```

### Run Flask Application

```bash
python app.py
```

### Open Browser

```text
http://127.0.0.1:5000
```

## Sample Recommendation

Input Movie:

```text
Avatar
```

Output:

```text
Top 5 Similar Movies
1. Movie A
2. Movie B
3. Movie C
4. Movie D
5. Movie E
```

## Conclusion

CineProphet successfully recommends similar movies using content-based filtering techniques. The system provides fast and relevant movie suggestions by analyzing textual movie features and calculating similarity scores.
