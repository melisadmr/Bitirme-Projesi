#Melisa Demir --> Bu kod Telegram verilerinin analizini bir NLP modeli sayesinde sağlar.
#fetch_and_analyze_messages fonksiyonu, belirli bir gruptan mesajları çeker ve sadece metin içerenleri döner.
#SVM modeli, her bir mesajı sınıflandırır ve tahmin sonuçları bir pasta grafiği ile görselleştirilir.
#Veri çekme işlemi bittikten sonra, bir geri sayım işlevi ile bir sonraki analize ne kadar kaldığı gösterilir.
#Kod, 5 dakikalık aralıklarla veri çekme ve analiz işlemini tekrarlar.


from telethon import TelegramClient  # Telegram API 'ye erişim 
import pandas as pd
import joblib  # SVM modeli için
from sklearn.feature_extraction.text import TfidfVectorizer
import time
import datetime
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm

# Telegram API bilgileri
api_id = '27421029'
api_hash = 'fe7895cb16ba4d957fe7c9cebbe0dd4e'
phone_number = '+905394529398' # Telefonn numarası

client = TelegramClient('session_name', api_id, api_hash)

# SVM model ve vektörleştirici yükleme
svm_model = joblib.load("svm_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# Grupları analiz etmek için fonksiyon
async def fetch_and_analyze_messages(group_id, limit=100):
    print(f"Grup ID: {group_id} için mesajlar çekiliyor...")
    messages_data = []

    try:
        async for message in client.iter_messages(group_id, limit=limit):
            # Sadece metin mesajlarını çekmek gerekli
            if message.text:
                messages_data.append(message.text)

        if not messages_data:
            print("Uyarı: Hiçbir mesaj alınamadı. Grup ID'sini veya erişim yetkisini kontrol edin.")
        else:
            print(f"{len(messages_data)} adet mesaj çekildi.")
        return messages_data
    except Exception as e:
        print(f"Mesajlar çekilirken hata oluştu: {e}")
        return []

# Veri analizi ve görselleştirme
def analyze_messages(messages):
    # Metinleri vektörleştir
    text_vectors = vectorizer.transform(messages)

    # Sınıflandırma tahmini
    predictions = svm_model.predict(text_vectors)

    # Sonuçları say
    counts = Counter(predictions)
    total_messages = len(messages)
    negative_count = counts.get("Olumsuz", 0)
    neutral_count = counts.get("Tarafsız", 0)

    # Yüzdeleri hesapla
    negative_percent = (negative_count / total_messages) * 100 if total_messages else 0
    neutral_percent = (neutral_count / total_messages) * 100 if total_messages else 0
    #verileri ekrana yazdır
    print(f"Toplam Mesaj: {total_messages}")
    print(f"Olumsuz Mesaj: {negative_count} ({negative_percent:.2f}%)")
    print(f"Tarafsız/Olumlu Mesaj: {neutral_count} ({neutral_percent:.2f}%)")

    # Grafik oluştur
    plt.figure(figsize=(8, 6))
    labels = ["Olumsuz", "Tarafsız/Olumlu"]
    sizes = [negative_count, neutral_count]
    colors = ["red", "green"]
    plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)  # olumsuz dilim biraz daha ön plana çıksın
    plt.title("Mesaj Analizi Sonuçları")
    plt.show()

# Geri sayım gösterimi
def countdown(minutes):
    total_seconds = minutes * 60
    while total_seconds > 0:
        m, s = divmod(total_seconds, 60)
        timer = f"{m:02d}:{s:02d}"
        print(f"Geri sayım: {timer}", end="\r")
        time.sleep(1)
        total_seconds -= 1

# Ana fonksiyon
async def main():
    await client.start()
    print("Telegram oturumu başlatıldı.")
    group_id = -1001535237830  # Grup ID'sini buraya yaz

    while True:
        print(f"{datetime.datetime.now()} - Veri çekme işlemi başlatılıyor...")
        messages = await fetch_and_analyze_messages(group_id)
        analyze_messages(messages)

        print("5 dakika bekleniyor...")
        countdown(5)

# Telegram istemcisini başlat
with client:
    client.loop.run_until_complete(main())
