import streamlit as st
import requests

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="BookBuddy AI", layout="wide")

# -----------------------
# CUSTOM PURPLE UI
# -----------------------
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }

    .main-title {
        background: linear-gradient(90deg, #7b2ff7, #9b59b6);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: white;
    }

    .subtitle {
        text-align: center;
        color: #ddd;
        margin-bottom: 30px;
    }

    .book-card {
        background-color: #1c1f26;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #9b59b6;
    }

    .footer {
        margin-top: 40px;
        text-align: center;
        color: #aaa;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------
# HEADER
# -----------------------
st.markdown('<div class="main-title">📚 BookBuddy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover the Perfect Book for Your Learning Journey</div>', unsafe_allow_html=True)

# -----------------------
# INPUT SECTION
# -----------------------
col1, col2 = st.columns([3,1])

with col1:
    topic = st.text_input("Search Books")

with col2:
    level = st.selectbox("Skill Level", ["Beginner", "Intermediate", "Advanced"])

search_button = st.button("🔍 Search")

# -----------------------
# SEARCH LOGIC
# -----------------------
if search_button and topic:

    # Smart query including level
    search_query = f"{topic} {level} programming textbook"

    url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults=10"

    response = requests.get(url)
    data = response.json()

    books = data.get("items", [])

    study_books = []

    for item in books:
        info = item.get("volumeInfo", {})
        title = info.get("title", "No Title")
        categories = info.get("categories", [])
        description = info.get("description", "")

        # Filter out fiction
        if "fiction" not in str(categories).lower():

            study_books.append({
                "title": title,
                "description": description
            })

        if len(study_books) == 5:
            break

    # -----------------------
    # DISPLAY RESULTS
    # -----------------------
    if study_books:
        for book in study_books:

            st.markdown(f"""
            <div class="book-card">
                <h4>{book['title']}</h4>
                <p><b>Why helpful?</b><br>
                {book['description'][:300] if book['description'] else "Covers important concepts for structured learning and practical understanding."}
                </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.error("No study books found. Try another topic.")

# -----------------------
# FOOTER
# -----------------------
st.markdown('<div class="footer">Built by Prachi | AI Mini Project 💜</div>', unsafe_allow_html=True)

