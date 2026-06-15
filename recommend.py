import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data(path="dataset.csv"):
    df = pd.read_csv(path, encoding="latin-1")

    rename_map = {
        "Aggregate rating": "Rating",
        "rate": "Rating",
        "name": "Restaurant Name",
        "location": "Locality",
        "votes": "Votes",
        "cuisines": "Cuisines",
        "city": "City",
    }
    df = df.rename(columns=rename_map)

    required_cols = ["Restaurant Name", "City", "Locality", "Cuisines", "Rating", "Votes", ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = None

    df = df[required_cols]
    df = df.dropna(subset=["Restaurant Name", "Cuisines", "City"])

    df["City"] = df["City"].astype(str).str.lower().str.strip()
    df["Locality"] = df["Locality"].astype(str).str.lower().str.strip()
    df["Cuisines"] = df["Cuisines"].astype(str).str.lower().str.strip()

    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Rating"] = df["Rating"].fillna(df["Rating"].mean())

    df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce").fillna(0)

    

    df = df.reset_index(drop=True)
    return df


# ---------------------------------------------------------
# 2. LOCATION FILTER (Locality -> City -> All, with fallback)
# ---------------------------------------------------------
def filter_by_location(df, city=None, locality=None):
    filtered = df.copy()
    city = city.lower().strip() if city else None
    locality = locality.lower().strip() if locality else None

    if locality:
        if city:
            result = filtered[
                (filtered["City"].str.contains(city, na=False)) &
                (filtered["Locality"].str.contains(locality, na=False))
            ]
        else:
            result = filtered[filtered["Locality"].str.contains(locality, na=False)]

        if not result.empty:
            return result, "locality"

    if city:
        result = filtered[filtered["City"].str.contains(city, na=False)]
        if not result.empty:
            return result, "city"

    return filtered, "all"

def recommend_restaurants(food_item, location_filtered_df, top_n=5):
    if location_filtered_df.empty:
        return pd.DataFrame()

    df = location_filtered_df.copy().reset_index(drop=True)

    tfidf = TfidfVectorizer()
    cuisine_matrix = tfidf.fit_transform(df["Cuisines"])

    query_vec = tfidf.transform([food_item.lower().strip()])
    similarity_scores = cosine_similarity(query_vec, cuisine_matrix).flatten()

    df["similarity"] = similarity_scores
    df["rating_norm"] = df["Rating"] / 5.0

    votes_range = df["Votes"].max() - df["Votes"].min()
    if votes_range == 0:
        df["votes_norm"] = 0
    else:
        df["votes_norm"] = (df["Votes"] - df["Votes"].min()) / votes_range

    df["final_score"] = (
        df["similarity"] * 0.6 +
        df["rating_norm"] * 0.3 +
        df["votes_norm"] * 0.1
    )

    result = df.sort_values("final_score", ascending=False).head(top_n)
    return result[["Restaurant Name", "Cuisines", "Rating", "Votes", "City", "Locality", "similarity"]]


if __name__ == "__main__":
    df = load_data("sample_dataset.csv")
    print(f"Loaded {len(df)} restaurants")

    filtered, level = filter_by_location(df, city="bangalore", locality="koramangala")
    print(f"\nMatch level: {level} | Restaurants found: {len(filtered)}")

    results = recommend_restaurants("biryani", filtered, top_n=5)
    print("\nTop recommendations:")
    print(results)
