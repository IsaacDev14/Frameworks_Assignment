import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Configure page
st.set_page_config(page_title="CORD-19 Research Analysis", layout="wide")

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df = df.dropna(subset=['publish_time'])
    df['year'] = pd.to_datetime(df['publish_time'], errors='coerce').dt.year
    return df

# Load dataset
st.title("CORD-19 Research Papers Analysis")
st.write("This application provides a basic analysis of the CORD-19 research dataset (metadata.csv).")

df = load_data()

# Dataset preview
st.subheader("Dataset Preview")
st.write(df.head())

# Publications by Year
st.subheader("Publications by Year")
year_counts = df['year'].value_counts().sort_index()

fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.barplot(x=year_counts.index, y=year_counts.values, color="skyblue", ax=ax1)
ax1.set_title("Publications by Year")
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Publications")
st.pyplot(fig1)

# Top Journals
st.subheader("Top 10 Journals")
top_journals = df['journal'].value_counts().head(10)

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(y=top_journals.index, x=top_journals.values, color="lightgreen", ax=ax2)
ax2.set_title("Top 10 Journals by Publications")
ax2.set_xlabel("Number of Publications")
ax2.set_ylabel("Journal")
st.pyplot(fig2)

# Word Cloud of Titles
st.subheader("Word Cloud of Paper Titles")
text = " ".join(str(title) for title in df['title'].dropna())

if text.strip():
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    ax3.imshow(wordcloud, interpolation="bilinear")
    ax3.axis("off")
    st.pyplot(fig3)
else:
    st.write("No titles available for word cloud.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit | CORD-19 Dataset")
