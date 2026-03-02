import streamlit as st
import requests
import pandas as pd
import math

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="BookBuddy AI", layout="wide")

# ----------------------------
# PURPLE UI STYLING
# ----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.header-box {
    background: linear-gradient(90deg, #6a5acd, #9370db);
    padding: 40px;
    border-radius: 15px;
    text-align: center;
}
.header-box h1 {
    color: white;
    font-size: 40px;
}
.header-box p {
    color: #f0f0f0;
}
.book-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-box">
<h1>📚 BookBuddy AI</h1>
<p>Discover the Perfect Book for Your Learning Journey</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# 🔐 Secure API Key
API_KEY = st.secrets["GOOGLE_API_KEY"]

# ----------------------------
# INPUT SECTION
# ----------------------------
col1, col2 = st.columns([3, 1])

with col1:
    subject = st.text_input("Search Books")

with col2:
    skill_level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])

# ----------------------------
# FETCH BOOKS
# ----------------------------
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
            volume = item.get("volumeInfo", {})

            books.append({
                "title": volume.get("title", ""),
                "authors": ", ".join(volume.get("authors", ["Unknown"])),
                "description": volume.get("description", ""),
                "rating": volume.get("averageRating", 0),
                "thumbnail": volume.get("imageLinks", {}).get("thumbnail", "")
            })

    return pd.DataFrame(books)

# ----------------------------
# SIMPLE NLP SCORING (NO SKLEARN)
# ----------------------------
def calculate_score(row, query):
    score = 0
    query_words = query.lower().split()

    content = (row["title"] + " " + row["description"]).lower()

    for word in query_words:
        score += content.count(word)

    rating_weight = (row["rating"] / 5) if row["rating"] else 0

    return score + rating_weight

# ----------------------------
# SEARCH BUTTON
# ----------------------------
if st.button("🔍 Search"):

    if subject.strip() == "":
        st.warning("Please enter a subject")
    else:
        df = fetch_books(subject)

        if df.empty:
            st.error("No books found")
        else:
            df["score"] = df.apply(lambda row: calculate_score(row, subject), axis=1)
            df = df.sort_values(by="score", ascending=False).head(5)

            st.write("")
            st.subheader("Top 5 Recommended Books")

            for _, row in df.iterrows():
                st.markdown('<div class="book-card">', unsafe_allow_html=True)

                col1, col2 = st.columns([1, 3])

                with col1:
                    if row["thumbnail"]:
                        st.image(row["thumbnail"])

                with col2:
                    st.markdown(f"### {row['title']}")
                    st.write(f"**Author:** {row['authors']}")
                    st.write(f"⭐ Rating: {row['rating']}")
                    st.write(row["description"][:300] + "...")

                st.markdown('</div>', unsafe_allow_html=True)

st.write("")
st.markdown("Built by Prachi | AI Mini Project")

