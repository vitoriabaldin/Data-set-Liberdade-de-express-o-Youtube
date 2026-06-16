import pandas as pd
import re
from collections import Counter
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")

stop_words = set(stopwords.words("portuguese"))

# -----------------------
# CARREGAR DADOS
# -----------------------
df = pd.read_csv(
    r"C:\Users\viihb\Downloads\videolist_search491_2026_04_29-17_59_24.csv"
)

# -----------------------
# TEXTO
# -----------------------
df["text"] = (
    df["videoTitle"].fillna("") + " " +
    df["videoDescription"].fillna("")
).str.lower()

# -----------------------
# TÓPICOS
# -----------------------
topics_dict = {
    "Embate institucional": [
        "kirk", "democracia", "liberdadedeexpressão",
        "política", "debate", "stf", "brasil", "censura"
    ],

    "Polarização de plataforma": [
        "lula", "shorts", "internet", "redes",
        "podcast", "bolsonaro", "monark", "debate"
    ],

    "Limites do humor e discurso de ódio": [
        "ódio", "humor", "news", "crime",
        "bolsonaro", "sociais", "lins"
    ],

    "Formatos educacionais": [
        "aula", "fundamentais", "economia",
        "governo", "crianças", "episódio"
    ],

    "Discurso jornalístico": [
        "notícias", "análises", "direito",
        "opiniões", "comentários", "mundo",
        "democracia", "política"
    ]
}

# -----------------------
# CLASSIFICADOR
# -----------------------
def classify_topic(text):

    scores = {}

    for topic, keywords in topics_dict.items():
        score = sum(1 for word in keywords if word in text)
        scores[topic] = score

    best_topic = max(scores, key=scores.get)

    if scores[best_topic] == 0:
        return "Outros"

    return best_topic

df["topic"] = df["text"].apply(classify_topic)

# -----------------------
# FILTRAR "OUTROS"
# -----------------------
outros = df[df["topic"] == "Outros"]

print("\n======================")
print("TOTAL EM 'OUTROS'")
print("======================")

print(len(outros))

# -----------------------
# LIMPEZA TEXTUAL
# -----------------------
def clean(text):

    text = text.lower()

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-záéíóúâêôãõç\s]", " ", text)

    tokens = text.split()

    tokens = [
        t for t in tokens
        if t not in stop_words and len(t) > 2
    ]

    return tokens

# -----------------------
# FREQUÊNCIA DE PALAVRAS
# -----------------------
all_words = []

for text in outros["text"]:
    all_words.extend(clean(text))

freq = Counter(all_words)

print("\n======================")
print("PALAVRAS MAIS FREQUENTES EM 'OUTROS'")
print("======================")

for word, count in freq.most_common(50):
    print(word, "-", count)

# -----------------------
# EXEMPLOS DE VÍDEOS
# -----------------------
print("\n======================")
print("EXEMPLOS DE VÍDEOS EM 'OUTROS'")
print("======================")

print(
    outros[["videoTitle", "channelTitle"]]
    .head(20)
)