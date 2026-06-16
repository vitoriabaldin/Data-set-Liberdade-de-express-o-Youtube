import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# -------------------------
# CARREGAR DADOS
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(
        "videolist_search491_2026_04_29-17_59_24.csv"
    )

    df["publishedAt"] = pd.to_datetime(df["publishedAt"], errors="coerce")
    df["year"] = df["publishedAt"].dt.year

    df["viewCount"] = pd.to_numeric(df["viewCount"], errors="coerce")
    df["likeCount"] = pd.to_numeric(df["likeCount"], errors="coerce")
    df["commentCount"] = pd.to_numeric(df["commentCount"], errors="coerce")

    df["text"] = (
        df["videoTitle"].fillna("") + " " +
        df["videoDescription"].fillna("")
    )

    return df


df = load_data()

# -------------------------
# INTERFACE
# -------------------------
st.title("Dashboard - YouTube Dataset")

st.write("Linhas:", df.shape[0])
st.write("Colunas:", df.shape[1])

# -------------------------
# 1. CANAIS MAIS RELEVANTES
# -------------------------
st.header("Top canais por visualizações")

top_channels = df.groupby("channelTitle")["viewCount"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_channels)

# -------------------------
# 2. TOP VÍDEOS
# -------------------------
st.header("Top 10 vídeos mais vistos")

top_videos = df.sort_values("viewCount", ascending=False)[
    ["videoTitle", "channelTitle", "viewCount"]
].head(10)

st.dataframe(top_videos)

# -------------------------
# 3. LINHA DO TEMPO
# -------------------------
st.header("Visualizações por ano")

timeline = df.groupby("year")["viewCount"].sum()
st.line_chart(timeline)

# -------------------------
# 4. NUVEM DE PALAVRAS (TÍTULOS + DESCRIÇÕES)
# -------------------------
st.header("Nuvem de palavras")

text = " ".join(df["text"].dropna())

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate(text)

fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")

st.pyplot(fig)