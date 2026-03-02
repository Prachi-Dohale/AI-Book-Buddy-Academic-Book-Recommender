import streamlit as st
import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Book Buddy", layout="wide")

st.title("📚 AI Book Buddy – NLP Recommender")
st.write("Find the most relevant academic books using AI")

# 🔐 Get API Key from Streamlit Secrets
API_KEY = st.secrets["GOOGLE_API_KEY"]

# -----------------------------
# USER INPUT
# -----------------------------
subject = st.text_input("Enter Subject (e.g., Machine Learning)")

# -----------------------------
# FETCH BOOKS FUNCTION
# -----------------------------
def fetch_books(query):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query,
        "maxResults": 30,
        "key": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()
    books = []

    if "items" in data:
        for item in data["items"]:
            volume = item["volumeInfo"]

            books.append({
                "title": volume.get("title", ""),
                "authors": ", ".join(volume.get("authors", ["Unknown"])),
                "description": volume.get("description", ""),
                "rating": volume.get("averageRating", 0),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail", "")
            })

    return pd.DataFrame(books)

# -----------------------------
# MAIN SEARCH LOGIC
# -----------------------------
if st.button("Search Books"):

    if subject.strip() == "":
        st.warning("Please enter a subject")
    else:
        df = fetch_books(subject)

        if df.empty:
            st.error("No books found")
        else:
            # Combine title and description
            df["content"] = df["title"] + " " + df["description"]

            corpus = df["content"].tolist()
            corpus.append(subject)

            # TF-IDF Vectorization
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(corpus)

            # Cosine Similarity
            similarity_scores = cosine_similarity(
                tfidf_matrix[-1], tfidf_matrix[:-1]
            ).flatten()

            df["similarity"] = similarity_scores

            # Final ranking score (Similarity + Rating weight)
            df["final_score"] = df["similarity"] + (df["rating"] / 5) * 0.2

            df = df.sort_values(by="final_score", ascending=False).head(5)

            st.subheader("📖 Top Recommended Books")

            for _, row in df.iterrows():
                with st.container():
                    col1, col2 = st.columns([1, 3])

                    with col1:
                        if row["thumbnail"]:
                            st.image(row["thumbnail"])

                    with col2:
                        st.markdown(f"### {row['title']}")
                        st.write(f"**Author:** {row['authors']}")
                        st.write(f"⭐ Rating: {row['rating']}")
                        st.write(row["description"][:300] + "...")

                    st.markdown("---")

st.markdown("Built by Prachi | Mini Project | NLP Recommendation System")
