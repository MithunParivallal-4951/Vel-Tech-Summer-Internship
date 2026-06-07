import argparse

from recommender import DEFAULT_MODEL_PATH, MovieRecommender


def main():
    parser = argparse.ArgumentParser(description="Recommend movies from a trained model.")
    parser.add_argument("movie", nargs="?", help="Movie title to recommend from")
    parser.add_argument("--model", default=DEFAULT_MODEL_PATH, help="Path to the trained model")
    parser.add_argument("--limit", type=int, default=10, help="Number of recommendations")
    parser.add_argument("--search", help="Search movie titles instead of recommending")
    args = parser.parse_args()

    recommender = MovieRecommender.load(args.model)

    if args.search:
        matches = recommender.search_titles(args.search, limit=args.limit)
        print(f"\nTitle matches for: {args.search}\n")
        for number, title in enumerate(matches, start=1):
            print(f"{number}. {title}")
        return

    if not args.movie:
        raise SystemExit("Please provide a movie title, or use --search.")

    recommendations = recommender.recommend(args.movie, limit=args.limit)
    print(f"\nRecommendations for: {args.movie}\n")
    for number, movie in enumerate(recommendations, start=1):
        print(f"{number}. {movie['title']}  | score: {movie['similarity_score']}")


if __name__ == "__main__":
    main()
