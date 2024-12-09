# Melisa Demir --> Bu kod Redditten çekilen verileri 5 dakikalık aralıklarla NLP modeli sayesinde analiz eder.
#Olumsuz ve olumlu/tarafsız içerik oranları bir pasta grafiği ile görselleştirildi.
#Grafiği oluşturmak için matplotlib kütüphanesi kullanıldı ve grafik bir dosyaya (reddit_analysis_pie_chart.png) kaydedildi.
#time.sleep(1) ile terminalde kullanıcıya bir geri sayım gösteriliyor.
#Olumsuz içerik oranı ve tarafsız içerik oranı yüzdelik olarak gösteriliyor.


import praw   # Reddit API 'den veri çekmek için kullanılan kütüphanedir
import datetime
import csv   # Verileri CSV dosyasına kaydetmek için kullanılır
import time
from langdetect import detect # Türkçe algılama 
from deep_translator import GoogleTranslator #Türkçeye çevirme
import joblib  # SVM modelini yüklemek için
import pandas as pd
import matplotlib.pyplot as plt #Grafik oluşturmak için
import os

# Reddit API kimlik bilgileri
reddit = praw.Reddit(
    client_id="xRNvCX_eLIm2aTO-K_njlA",
    client_secret="6SG4kRK7dG1FqDpupWeyXcqRAtVEBA",
    user_agent="Federal_Young7944"
)

# SVM modelini yükle
svm_model = joblib.load("svm_model.pkl")  # Model dosyamızın adı
vectorizer = joblib.load("tfidf_vectorizer.pkl")  # Vektörleştirici dosyası

# Veri çekmek istediğiniz subreddit
subreddit = reddit.subreddit("Turkey")

# CSV dosyasını oluştur ve başlık satırını yaz
with open("reddit_real_time.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Başlık", "Gönderi İçeriği", "Yorum Sayısı", "Upvote Sayısı", "Gönderi Tarihi", "Tahmin"])

    while True:
        print("\nYeni veriler çekiliyor...")
        total_count = 0
        positive_count = 0
        negative_count = 0

        for submission in subreddit.hot(limit=50):  # Her seferinde 50 gönderi çek
            submission_title = submission.title
            submission_content = submission.selftext

            if not submission_title.strip() or not submission_content.strip():
                continue

            # İngilizce olanları Türkçeye çevir
            try:
                if detect(submission_title) != "tr":
                    submission_title = GoogleTranslator(source="auto", target="tr").translate(submission_title)
                if detect(submission_content) != "tr":
                    submission_content = GoogleTranslator(source="auto", target="tr").translate(submission_content)
            except Exception as e:
                print(f"Çeviri hatası: {e}")
                continue

            submission_time = datetime.datetime.fromtimestamp(submission.created_utc)

            # Metni vektörleştir ve sınıflandır
            combined_text = f"{submission_title} {submission_content}"
            text_vector = vectorizer.transform([combined_text])
            prediction = svm_model.predict(text_vector)[0]

            # Tahminlere göre sayacı güncelle
            total_count += 1
            if prediction == "Olumsuz":  # Modelimizin sınıf adı
                negative_count += 1
            else:
                positive_count += 1

            try:
                writer.writerow([
                    submission_title,
                    submission_content,
                    submission.num_comments,
                    submission.score,
                    submission_time,
                    prediction
                ])
            except Exception as e:
                print(f"Yazma hatası: {e}")

        # İstatistikleri yazdır
        print("\nVeri Çekme İstatistikleri:")
        print(f"Toplam Veri: {total_count}")
        print(f"Olumsuz İçerik: {negative_count} ({(negative_count / total_count) * 100:.2f}%)")
        print(f"Tarafsız/Olumlu İçerik: {positive_count} ({(positive_count / total_count) * 100:.2f}%)")

        # Pasta grafiği oluştur
        labels = ["Olumsuz", "Tarafsız/Olumlu"]
        sizes = [negative_count, positive_count]
        colors = ["red", "green"]
        explode = (0.1, 0)  # Olumsuz dilimi vurgulamak için

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct="%1.1f%%", shadow=True, startangle=140)
        plt.title("Veri Analizi Dağılımı")
        plt.savefig("reddit_analysis_pie_chart.png")
        plt.show()

        # Geri sayım
        countdown_time = 300  # 5 dakika
        print("\nBir sonraki analiz için geri sayım başlıyor...")
        for remaining in range(countdown_time, 0, -1):
            print(f"Kalan süre: {remaining} saniye", end="\r")
            time.sleep(1)
