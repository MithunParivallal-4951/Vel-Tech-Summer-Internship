import matplotlib.pyplot as plt
import seaborn as sns

print("=" * 50)
print("GENERATING VISUALIZATIONS")
print("=" * 50)

plt.figure(figsize=(8,5))
df["Rating"].hist(bins=20)
plt.title("Distribution of Movie Ratings")
plt.xlabel("Rating")
plt.ylabel("Number of Movies")
plt.savefig("rating_distribution.png")
plt.show()

print("rating_distribution.png saved")

plt.figure(figsize=(10,5))
df["Genres"].value_counts().head(10).plot(kind="bar")
plt.title("Top 10 Movie Genres")
plt.xlabel("Genres")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("top_genres.png")
plt.show()

print("top_genres.png saved")

numeric = df.select_dtypes(include=["int64", "float64"])

plt.figure(figsize=(8,6))
sns.heatmap(
    numeric.corr(),
    annot=True,
    cmap="coolwarm"
)
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("heatmap.png")
plt.show()

print("heatmap.png saved")

print("\nAll visualization files generated successfully.")