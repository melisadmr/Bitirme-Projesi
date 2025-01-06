import tweepy
import pandas as pd

BEARER_TOKEN = 'BEARER TOKEN' #Twitter API'den elde edilen kimlik bilgisi bu alana yazılır
client = tweepy.Client(bearer_token=BEARER_TOKEN)
#hangi kelime aranacak ? TÜRKÇE OLANLARI ÇEKER
query = "Turkey lang:tr"

# MAX_RESULTS=10 MAX 10 ADET VERİ ÇEKİLİR, LİMİT ARTIRILABİLİR.
tweets = client.search_recent_tweets(query=query, max_results=80)

#Tweetlerin saklandığı liste
tweets_list = []

# Tweetleri listeye ekleme
for tweet in tweets.data:
    tweets_list.append([tweet.id, tweet.text])

# Tweetleri bir DataFrame'e dönüştürme
tweets_df = pd.DataFrame(tweets_list, columns=["ID", "Tweet"])

# DataFrame'i CSV dosyasına kaydedilir.
tweets_df.to_csv("tweets.csv", index=False, encoding="utf-8")
# Tweetler kaydedildiğinde gösterilir.
print("Tweetler 'tweets.csv' dosyasına kaydedildi.")
