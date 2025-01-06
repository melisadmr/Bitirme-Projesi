import praw
from langdetect import detect
from deep_translator import GoogleTranslator
import csv
import datetime
import time

# Reddit API kimlik bilgileri
reddit = praw.Reddit(
    client_id="client id",
    client_secret="client secret",
    user_agent="user agent"
)

# Veri çekmek istediğiniz subreddit
subreddit = reddit.subreddit("Turkey")

# CSV dosyasını aç ve başlık satırını yaz
with open("reddit7_haberler.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Başlık", "Gönderi İçeriği", "Yorum Sayısı", "Upvote Sayısı", "Gönderi Tarihi"])

    # Her gönderiyi kontrol et
    for submission in subreddit.hot(limit=1000):
        time.sleep(2)
        submission_title = submission.title
        submission_content = submission.selftext

        # Boş metin kontrolü
        if not submission_title.strip() or not submission_content.strip():
            continue  # Boş içerikler atlanır

        # Dil tespiti ve çeviri işlemi
        try:
            if detect(submission_title) != "tr":
                submission_title = GoogleTranslator(source="auto", target="tr").translate(submission_title)
            if detect(submission_content) != "tr":
                submission_content = GoogleTranslator(source="auto", target="tr").translate(submission_content)
        except Exception as e:
            print(f"Çeviri sırasında hata: {e}")
            continue  # Çevirisi yapılamayan içerikler atlanır

        submission_time = datetime.datetime.fromtimestamp(submission.created_utc)
        writer.writerow([
            submission_title,
            submission_content,
            submission.num_comments,
            submission.score,
            submission_time
        ])

print("Veriler başarıyla kaydedildi.")
