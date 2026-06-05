df.fillna("", inplace=True)

df["tags"] = (
    df["Description"] + " " +
    df["Genres"] + " " +
    df["Directed by"] + " " +
    df["Written by"]
)

df["tags"] = df["tags"].str.lower()