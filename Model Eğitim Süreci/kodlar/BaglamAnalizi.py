# Gerekli kütüphaneler
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter, defaultdict
from itertools import combinations
from gensim.models import Word2Vec
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import networkx as nx

# NLTK kütüphanesi için indirmeler
nltk.download("stopwords")
nltk.download("punkt")

# Veri Yükleme
df = pd.read_csv("TwitterData.csv")  # CSV dosyanızı buraya ekleyin
print("Veri Yüklendi: İlk 5 Satır:")
print(df.head())

# 1. Ön İşleme
stop_words = set(stopwords.words("turkish"))


# Boş hücreleri doldurma
df["Tweet"] = df["Tweet"].fillna("")  # NaN değerlerini boş string ile doldur

# Tüm hücreleri stringe çevirme
df["Tweet"] = df["Tweet"].astype(str)

# Tokenizasyon Fonksiyonu
def temizle_ve_tokenize(metin):
    if not isinstance(metin, str):  # Eğer metin string değilse
        return []  # Boş liste döndür
    metin = metin.lower()  # Küçük harfe çevir
    tokenlar = word_tokenize(metin)  # Tokenize et
    temiz_tokenlar = [kelime for kelime in tokenlar if kelime.isalnum() and kelime not in stop_words]  # Temizleme
    return temiz_tokenlar

# Tokenize işlemini uygulama
df["tokenize"] = df["Tweet"].apply(temizle_ve_tokenize)
print("Ön İşleme Tamamlandı.")

# 2. Kelime Sıklığı Analizi
kelime_listesi = [kelime for tokenler in df["tokenize"] for kelime in tokenler]
kelime_sıklığı = Counter(kelime_listesi).most_common(20)

print("\nEn Sık Geçen Kelimeler:")
for kelime, frekans in kelime_sıklığı:
    print(f"{kelime}: {frekans}")

# 3. Kelime Ortaklığı Analizi
ortaklıklar = defaultdict(int)
for tokenler in df["tokenize"]:
    for kelime1, kelime2 in combinations(set(tokenler), 2):
        ortaklıklar[(kelime1, kelime2)] += 1

print("\nEn Sık Geçen Kelime Ortaklıkları:")
for (kelime1, kelime2), sayi in sorted(ortaklıklar.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{kelime1} - {kelime2}: {sayi}")

# 4. Kelime Gömme ve Bağlam Analizi
model = Word2Vec(sentences=df["tokenize"], vector_size=100, window=5, min_count=2, sg=1)
print("\n'Tehdit' Kelimesine Bağlamda En Yakın Kelimeler:")
#for kelime, skor in model.wv.most_similar("tehdit", topn=10):
 #   print(f"{kelime}: {skor}")
# Kelimelerin bağlamda en yakınlarını bulmak
kelimeler = ["saldırı", "risk", "ölüm","tehdit","ayrımcılık","cinayet","şiddet","siber saldırı","istismar"]


for kelime in kelimeler:
    print(f"'{kelime}' Kelimesine Bağlamda En Yakın Kelimeler:")
    try:
        for benzer_kelime, skor in model.wv.most_similar(kelime, topn=10):
            print(f"{benzer_kelime}: {skor}")
    except KeyError:
        print(f"'{kelime}' kelimesi modelin kelime dağarcığında bulunamadı.")
    print()

# 5. Görselleştirme: Kelime Bulutu
kelime_bulutu = WordCloud(width=800, height=400, background_color="white").generate(" ".join(kelime_listesi))
plt.figure(figsize=(10, 5))
plt.imshow(kelime_bulutu, interpolation="bilinear")
plt.axis("off")
plt.title("Kelime Bulutu")
plt.show()

# 6. Görselleştirme: İlişki Grafiği
G = nx.Graph()
for (kelime1, kelime2), sayi in list(ortaklıklar.items())[:50]:
    G.add_edge(kelime1, kelime2, weight=sayi)

plt.figure(figsize=(12, 12))
nx.draw(G, with_labels=True, node_color="lightblue", edge_color="gray", node_size=1500, font_size=10)
plt.title("Kelime İlişki Grafiği")
plt.show()

print("Bağlam Analizi Tamamlandı!")
