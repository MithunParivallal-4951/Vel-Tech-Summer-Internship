import argparse

from recommender import DEFAULT_DATASET, DEFAULT_MODEL_PATH, DEFAULT_TEXT_COLUMNS, MovieRecommender


def main():
    parser = argparse.ArgumentParser(description="Train and save the movie recommendation model.")
    parser.add_argument("--data", default=DEFAULT_DATASET, help="Path to the movie dataset CSV")
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH, help="Where to save the trained model")
    parser.add_argument("--title-column", default="Title", help="Column containing movie titles")
    parser.add_argument(
        "--text-columns",
        nargs="+",
        default=DEFAULT_TEXT_COLUMNS,
        help="Columns used to calculate similarity",
    )
    args = parser.parse_args()

    recommender = MovieRecommender(
        csv_path=args.data,
        title_column=args.title_column,
        text_columns=args.text_columns,
    )
    recommender.save(args.model)

    print("Model trained successfully.")
    print(f"Movies loaded: {len(recommender.movies)}")
    print(f"Title column: {recommender.title_column}")
    print(f"Feature columns: {', '.join(recommender.used_text_columns)}")
    print(f"Saved model: {args.model}")


if __name__ == "__main__":
    main()
