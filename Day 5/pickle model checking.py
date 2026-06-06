import pickle


pickle.dump(
	df,
	open("movies.pkl", "wb")
)

pickle.dump(
	similarity,
	open("similarity.pkl", "wb")
)

print("Movies data saved as movies.pkl")
print("Similarity matrix saved as similarity.pkl")

print("\n" + "="*50)
print("PREDICTION CASE 1")
print("="*50)
recommend("Avatar")

print("\n" + "="*50)
print("PREDICTION CASE 2")
print("="*50)
recommend("Titanic")

print("\n" + "="*50)
print("PREDICTION CASE 3")
print("="*50)
recommend("The Dark Knight")

print("\nAll files saved successfully.")
