import streamlit as st
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="BookBuddy AI", layout="wide")

st.title("📚 BookBuddy AI")
st.write("Discover the Perfect Book for Your Learning Journey")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("books_dataset.csv")   # make sure file name matches
    return df

df = load_data()

# Clean column names (important)
df.columns = df.columns.str.strip()

# Convert to lowercase for safe filtering
df["title"] = df["title"].astype(str)
df["skill_level"] = df["skill_level"].astype(str)
df["category"] = df["category"].astype(str)

df["skill_level"] = df["skill_level"].str.lower()
df["category"] = df["category"].str.lower()

# ----------------------------
# SEARCH SECTION
# ----------------------------
st.subheader("🔎 Search Books")

col1, col2, col3 = st.columns(3)

with col1:
    search_query = st.text_input("Search by Title")

with col2:
    selected_level = st.selectbox(
        "Skill Level",
        sorted(df["skill_level"].unique())
    )

with col3:
    selected_category = st.selectbox(
        "Category",
        sorted(df["category"].unique())
    )

# ----------------------------
# FILTER LOGIC
# ----------------------------
filtered_df = df.copy()

# Search filter (partial match safe)
if search_query:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search_query, case=False, na=False)
    ]

# Skill level filter
if selected_level:
    filtered_df = filtered_df[
        filtered_df["skill_level"] == selected_level.lower()
    ]

# Category filter
if selected_category:
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category.lower()
    ]

# ----------------------------
# RESULTS
# ----------------------------
st.markdown("---")
st.subheader("📖 Recommended Books")

if filtered_df.empty:
    st.warning("No books found. Try another search.")
else:
    for index, row in filtered_df.iterrows():
        with st.container():
            st.markdown(f"### {row['title']}")
            st.write(f"**Author:** {row.get('author', 'Unknown')}")
            st.write(f"**Skill Level:** {row['skill_level'].capitalize()}")
            st.write(f"**Category:** {row['category'].capitalize()}")
            st.markdown("---")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("Built by Prachi (Data Science Student)")
