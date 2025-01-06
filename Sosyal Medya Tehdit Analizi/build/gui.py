
import asyncio
from pathlib import Path
from tkinter import Frame, Tk, Canvas, Entry, Text, Button, PhotoImage
import praw #Reddit API'ye erişim
import datetime
import csv
import time
from langdetect import detect
from deep_translator import GoogleTranslator
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import re
from telethon import TelegramClient  # Telegram API 'ye erişim 
from tqdm import tqdm
from collections import Counter
import random
import webbrowser
import os

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\MELİSA DEMİR\OneDrive\Masaüstü\arayuzBitirme\deneme\build\assets\frame0")

# Bilgi butonuna tıklandığında proje tezini açması için gerekli fonksiyon
def open_to_PDF():

    pdf_path = r"C:\Users\MELİSA DEMİR\OneDrive\Masaüstü\arayuzBitirme\deneme\25111600.pdf"  # Dosya yolunu güncelleyin

    webbrowser.open(pdf_path)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("1296x729")
window.configure(bg = "#101319")
window.title("Analysis Dashboards")

countdown_timer = None  # Global değişken, sayacın ID'sini tutar
current_platform = None  # Aktif platformu tutar
reddit_instance = None
svm_model = None #svm modeli tutan parametre
vectorizer = None # tfidf vektörizeri tutan parametre
csv_file = "reddit_analysis.csv"


#Twitter için veri çekilecek csv dosyasını alan  fonksiyon
def initialize_twitter():
    twitter_data="TwitterData.csv"
    return twitter_data

#Telegram İçin Veri Çekme Fonksiyonu
def initialize_telegram():
    try:
        api_id = '27421029'
        api_hash = 'fe7895cb16ba4d957fe7c9cebbe0dd4e'
        phone_number = '+905394529398' # Telefonn numarası
        client = TelegramClient('session_name', api_id, api_hash)
        return client
    except Exception as e:
        print(f"Telegram API bağlantı hatası: {e}")
    
# Reddit için veri çekme fonksiyonu
def initialize_reddit():
    try:
        reddit = praw.Reddit(
            client_id="xRNvCX_eLIm2aTO-K_njlA",
            client_secret="6SG4kRK7dG1FqDpupWeyXcqRAtVEBA",
            user_agent="Federal_Young7944"
        )
        # Test bağlantısını kontrol et
        test_subreddit = reddit.subreddit("Turkey")
        print(f"Bağlantı başarılı! Test subreddit adı: {test_subreddit.display_name}")
        return reddit
    except Exception as e:
        print(f"Reddit API bağlantı hatası: {e}")
        return None

# Modeli ve vektörleştiriciyi yükle
def load_model_and_vectorizer(current_platform):

    if current_platform=="reddit":
      model = joblib.load(r"C:\Users\MELİSA DEMİR\OneDrive\Masaüstü\arayuzBitirme\deneme\svm_model.pkl")
      vectorizer = joblib.load("tfidf_vectorizer.pkl")
    elif current_platform=="telegram":
        model = joblib.load("svm_model_telegram.pkl")
        vectorizer = joblib.load("tfidf_vectorizer_telegram.pkl")
    elif current_platform =="twitter":
        model =joblib.load("svm_model_twitter.pkl")
        vectorizer=joblib.load("tfidf_vectorizer_twitter.pkl")
    return model, vectorizer
# CSV dosyasını başlat
def initialize_csv(file_name):
    if not os.path.exists(file_name):
        with open(file_name, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Başlık", "Gönderi İçeriği", "Yorum Sayısı", "Upvote Sayısı", "Gönderi Tarihi", "Tahmin"])

#Twitter verilerinin analizi için kullanılan fonksiyon
def fect_and_analyze_twitter_data(svm_model,vectorizer,twitter_data):
    try:
        # 1. CSV'den rastgele 50 veri seç
        data = pd.read_csv(twitter_data)
        if data.empty:
            print("CSV dosyası boş!")
            return

        # Rastgele 50 satır seç ve işleme
        batch = data.sample(n=50, random_state=random.randint(1, 33000))
        tweets = batch["Tweet"]  # 'tweet' sütun adı varsayılmıştır, değiştirin gerekirse
        positive_count = 0
        negative_count = 0
        # 2. Verileri vektörize et
        features = vectorizer.transform(tweets)
        # 3. Model ile tahmin yap
        predictions = svm_model.predict(features)
        # 4. Sonuçları analiz et
        for pred in predictions:
            if pred == "Olumsuz":
                negative_count += 1
            elif pred == "Tarafsız":
                positive_count += 1
        total_count=positive_count + negative_count

    except Exception as e:
        print(f"Bir hata oluştu: {e}")
    canvas.itemconfig(sonuc_label, text=f"Bu analiz sonucunda toplamda {total_count} adet tweet analiz edildi.\n {negative_count} adet tweet olumsuz,\n{positive_count} adet tweet tarafsız olarak bulundu.")
    
    generate_statistics_and_plot_on_canvas(
    total_count,
    positive_count,
    negative_count,
    x=250,  # Grafiğin sol üst köşe x koordinatı
    y=150,  # Grafiğin sol üst köşe y koordinatı
    width=500,  # Grafiğin genişliği
    height=350  # Grafiğin yüksekliği
)
 # Reddit verilerinin  analizi için kullanılan fonksiyon   
def fetch_reddit_data(reddit, subreddit_name, model, vectorizer, csv_file):
    
    if vectorizer is None:
        print("Vectorizer None. Lütfen vectorizer'ı başlatın.")
        return

    try:
        subreddit = reddit.subreddit(subreddit_name)
    except Exception as e:
        print(f"Reddit subreddit hatası: {e}")
        return

    total_count = 0
    positive_count = 0
    negative_count = 0
    olumsuz_kelimeler = [
        "tehdit", "saldırı", "korku", "düşman", "zarar", "risk", "patlama", "pkk", "terorist", "bomba", 
        "öldür", "kürdistan", "kurdistan", "bomba", "bıçak", "saldırgan", "darbe", "ölüm", 
        "istismar", "şiddet", "infaz", "hırsızlık", "cinsel istismar", "taciz", "tecavüz", "iç savaş", 
        "dolandırıcılık", "siber saldırı", "siber tehdit", "ajan", "hakaret", "yalan"
    ]
      # Olumsuz kelimeleri içeren gönderiler
    olumsuz_kelime_listesi = []

    for submission in subreddit.hot(limit=50):
        submission_title = submission.title
        submission_content = submission.selftext

        if not submission_title.strip() or not submission_content.strip():
            continue

        try:
            # Dil tespiti ve çevirisi
            if detect(submission_title) != "tr":
                submission_title = GoogleTranslator(source="auto", target="tr").translate(submission_title)
            if detect(submission_content) != "tr":
                submission_content = GoogleTranslator(source="auto", target="tr").translate(submission_content)
        except Exception as e:
            print(f"Çeviri hatası: {e}")
            continue

        submission_time = datetime.datetime.fromtimestamp(submission.created_utc).strftime("%Y-%m-%d %H:%M:%S")
        # Metni vektörleştir ve sınıflandır
        combined_text = f"{submission_title} {submission_content}"
        text_vector = vectorizer.transform([combined_text])
        prediction = model.predict(text_vector)[0]
        # Sayacı güncelle
        total_count += 1
        if prediction == "Olumsuz":
            negative_count += 1
            combined_text = f"{submission_title} {submission_content}"
            olumsuz_kelime_bulunanlar = []
            # Kelimeler üzerinden kontrol yap
            for kelime in olumsuz_kelimeler:
                if re.search(r"\b" + re.escape(kelime) + r"\b", combined_text.lower()):
                    olumsuz_kelime_bulunanlar.append(kelime)
            
            # Eğer olumsuz kelimeler bulunursa listeye ekle
            if olumsuz_kelime_bulunanlar:
                olumsuz_kelime_listesi.append(olumsuz_kelime_bulunanlar)

        else:
            positive_count += 1
        # CSV'ye yaz
        try:
            with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
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

    print(f"Reddit Analizi Tamamlandı: Toplam {total_count} gönderi analiz edildi.")
    print(f"Pozitif: {positive_count}, Negatif: {negative_count}")
   
    # Olumsuz kelimeleri düz bir metne çevir
    olumsuz_kelime_string= []
    olumsuz_kelime_string = ", ".join([kelime for kelimeler in olumsuz_kelime_listesi for kelime in kelimeler])
    # Eğer olumsuz kelimeler varsa metni şu şekilde güncelle:
    if olumsuz_kelime_string:
      canvas.itemconfig(sonuc_label, text=f"Bu analiz sonucunda olumsuz gönderilerde\n şu kelimelere rastlanmıştır:\n {olumsuz_kelime_string}")
    else:
      canvas.itemconfig(sonuc_label, text="Bu analiz sonucunda olumsuz gönderilerde \n olumsuz kelime  listesinden bir kelime bulunmamıştır.")

    generate_statistics_and_plot_on_canvas(
    total_count,
    positive_count,
    negative_count,
    x=250,  # Grafiğin sol üst köşe x koordinatı
    y=150,  # Grafiğin sol üst köşe y koordinatı
    width=500,  # Grafiğin genişliği
    height=350  # Grafiğin yüksekliği
)
    
# Telegram verilerinin analizi için kullanılan fonksiyon
async def fetch_and_analyze_telegram_messages(group_id,svm_model,vectorizer, limit=100):
    """
    Telegram'dan mesajları çek ve analiz et.
    """
    print(f"Grup ID: {group_id} için mesajlar çekiliyor...")
    messages_data = []
    client = initialize_telegram()  # Telegram istemcisini başlat
    await client.start()
    print("Telegram oturumu başlatıldı.")

    try:
        # Telegram mesajlarını çek
        async for message in client.iter_messages(group_id, limit=limit):
            if message.text:  # Sadece metin mesajlarını ekle
                messages_data.append(message.text)

        if not messages_data:
            print("Uyarı: Hiçbir mesaj alınamadı. Grup ID'sini veya erişim yetkisini kontrol edin.")
            return

        print(f"{len(messages_data)} adet mesaj çekildi.")

        # Metinleri vektörleştir
        text_vectors = vectorizer.transform(messages_data)
        # Sınıflandırma tahmini
        predictions = svm_model.predict(text_vectors)
        # Sonuçları say
        counts = Counter(predictions)
        total_messages = len(messages_data)
        negative_count = counts.get("Olumsuz", 0)
        neutral_count = counts.get("Tarafsız", 0)
        canvas.itemconfig(sonuc_label, text=f"Bu analiz sonucunda toplamda {total_messages} adet mesaj analiz edildi.\n {negative_count} adet mesaj olumsuz,\n{neutral_count} adet mesaj tarafsız olarak bulundu.")

        # Sonuçları görselleştir
        generate_statistics_and_plot_on_canvas(
            total_messages,
            neutral_count,
            negative_count,
            x=250,  # Grafiğin sol üst köşe x koordinatı
            y=150,  # Grafiğin sol üst köşe y koordinatı
            width=500,  # Grafiğin genişliği
            height=350  # Grafiğin yüksekliği
        )

    except Exception as e:
        print(f"Hata oluştu: {e}")
    
# Analiz edilen verilerin grafiğinin oluşturulması
def generate_statistics_and_plot_on_canvas(total_count, positive_count, negative_count, x, y, width, height):
    # Veri İstatistikleri
    print("\nVeri Çekme İstatistikleri:")
    print(f"Toplam Veri: {total_count}")
    print(f"Olumsuz İçerik: {negative_count} ({(negative_count / total_count) * 100:.2f}%)")
    print(f"Tarafsız/Olumlu İçerik: {positive_count} ({(positive_count / total_count) * 100:.2f}%)")
    canvas.itemconfig(toplam_veri, text=total_count)
    canvas.itemconfig(olumsuz_label, text=f"{(negative_count / total_count) * 100:.2f}")
    canvas.itemconfig(tarafsız_label, text=f"{(positive_count / total_count) * 100:.2f}")
    # Pie Chart İçin Etiketler ve Veriler
    labels = ["Olumsuz", "Tarafsız/Olumlu"]
    sizes = [negative_count, positive_count]
    colors = ["#B84040", "#254274"]
    edge_colors = ["#DD4D4D", "#2C4F8B"] 
    explode = (0.1, 0)  # Olumsuz dilimi vurgulamak için
    # Matplotlib Şekli Oluşturma
    fig = Figure(figsize=(width / 100, height / 100), dpi=100)
    fig.patch.set_alpha(0)  # Şeklin dış arka planını şeffaf yap
    ax = fig.add_subplot(111)
    ax.set_facecolor("none")  # Ekseni şeffaf yap
    # Pie Chart'ı oluşturma ve wedge (dilim) nesnelerini alma
    wedges, texts, autotexts = ax.pie(
        sizes,
        explode=explode,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        textprops={'color': 'white'}, #burası grafiğin kendisindeki yazıları da beyaz yapıyor
        shadow=True,
        startangle=140,
        wedgeprops={"linewidth": 3.0}  # Kenarlık kalınlığı
    )

    # Her bir dilimin kenar rengini ayarlama
    for wedge, edge_color in zip(wedges, edge_colors):
        wedge.set_edgecolor(edge_color)

    ax.set_title("Veri Dağılım Grafiği", color="white")
    ax.axis("equal")  # Daireyi düzgün yapmak için

    # Şeffaf Arka Planlı Grafiği Kaydet
    temp_file = "transparent_pie_chart.png"
    fig.savefig(temp_file, transparent=True)

    # Tkinter Canvas Üzerine Görüntüyü Arka Plan Olarak Eklemek
    image_image_5 = PhotoImage(file=r"C:\Users\MELİSA DEMİR\OneDrive\Masaüstü\RedditModelEğitimi\Bitirme-Projesi\build\assets\frame0\image_5.png")  # Arka plan resmi
    canvas.create_image(
        494.0,
        331.0,
        image=image_image_5
    )
    # Kaydedilen Şeffaf Grafiği Yükle
    pie_chart_image = PhotoImage(file=temp_file)
    # Pie Chart'ı Canvas Üzerine Koy
    canvas.create_image(
        x + width // 2,  # Ortalamak için x + genişlik/2
        y + height // 2,  # Ortalamak için y + yükseklik/2
        image=pie_chart_image
    )
    
    # Geçici dosyayı temizleme
    os.remove(temp_file)

    # Bu önemli! Tkinter'ın PhotoImage nesnesini saklaması için image referansı tut
    canvas.pie_chart_image = pie_chart_image

# Geri sayım başlatan fonksiyon
def countdown(minutes=5):
    global countdown_timer, current_platform
    total_seconds = minutes * 60  # Dakikayı saniyeye çevir
    # Eğer sayaç çalışıyorsa, önceki timer'ı iptal et
    if countdown_timer is not None:
        window.after_cancel(countdown_timer)  # Önceki timer'ı iptal et
    def update_time():
        global countdown_timer  # Tekrar global olarak belirt
        nonlocal total_seconds
        
        total_seconds -= 1  # 1 saniye azalt
        minutes_left = total_seconds // 60  # Kalan dakika
        seconds_left = total_seconds % 60  # Kalan saniye
        minutes_str = f"{minutes_left:02}:{seconds_left:02}"  # Dakika ve saniyeyi formatla
        canvas.itemconfig(countdown_label, text=minutes_str)  # Label'ı güncelle

        if total_seconds > 0:
            countdown_timer = window.after(1000, update_time)  # 1 saniye sonra tekrar çağır
        else:
            if current_platform=="twitter":
               update_title_to_twitter()
            elif current_platform=="telegram":
               update_title_to_telegram()
            elif current_platform=="reddit":
                update_title_to_reddit()   
    # Geri sayımı başlat
    update_time()
 
# Twitter butonuna tıklandığında başlığı Twitter Analizi olarak değiştiren fonksiyon
def update_title_to_twitter():
    global current_platform
    current_platform = "twitter"  # Aktif platform Twitter olarak ayarlanır
    canvas.itemconfig(text_id, text="Twitter Analizi")
    twitter_data= initialize_twitter()
    svm_model,vectorizer= load_model_and_vectorizer(current_platform)
    fect_and_analyze_twitter_data(svm_model,vectorizer,twitter_data)
    countdown(5)  # Twitter tıklandığında geri sayım başlatılır

# Telegram butonuna tıklandığında başlığı Telegram Analizi olarak değiştiren fonksiyon
def update_title_to_telegram():
    global current_platform
    current_platform = "telegram"  # Aktif platform Telegram olarak ayarlanır
    canvas.itemconfig(text_id, text="Telegram Analizi")
   
    svm_model,vectorizer= load_model_and_vectorizer(current_platform)
    group_id=-1002443519536
    asyncio.run(fetch_and_analyze_telegram_messages(group_id,svm_model,vectorizer))
    countdown(5)  # telegram tıklandığında geri sayım başlatılır

# Reddit butonuna tıklandığında başlığı Reddit Analizi olarak değiştiren fonksiyon
def update_title_to_reddit():
    global svm_model,csv_file
    global current_platform
    canvas.itemconfig(text_id, text="Reddit Analizi")
    current_platform = "reddit"  # Aktif platform Reddit olarak ayarlanır
    reddit_instance=initialize_reddit()
    svm_model,vectorizer=load_model_and_vectorizer(current_platform)
    print("load başarılı!")
    initialize_csv("reddit_data.csv")
    print("csv başarılı")
    if reddit_instance is None:
        print("Reddit instance None. İşlem yapılamaz.")
        return
    else:
        print("Reddit instance mevcut. Veri çekme işlemi başlıyor...")
        fetch_reddit_data(reddit_instance, "Turkey", svm_model, vectorizer, csv_file)
    countdown(5)  # reddit tıklandığında geri sayım başlatılır 


#Arayüz Elemanlarının Tanımlamaları
canvas = Canvas(
    window,
    bg = "#101319",
    height = 729,
    width = 1296,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    648.0,
    364.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    318.0,
    88.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    79.692626953125,
    87.60125732421875,
    image=image_image_3
)

text_id=canvas.create_text(
    153.0,
    75.0,
    anchor="nw",
    text="Sosyal Medya Tehdit Analizi",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 23 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    1017.0,
    191.0001220703125,
    image=image_image_4
)

canvas.create_text(
    882.21923828125,
    146.30075073242188,
    anchor="nw",
    text="Toplam Veri",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 20 * -1)
)

toplam_veri=canvas.create_text(
    1005.99951171875,
    178.70095825195312,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 36 * -1)
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    1017.0,
    303.5013122558594,
    image=image_image_5
)

canvas.create_text(
    882.21923828125,
    257.8999938964844,
    anchor="nw",
    text="Tarafsız Duygu \nOranı",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 19 * -1)
)

canvas.create_text(
    1060.90771484375,
    311.8997802734375,
    anchor="nw",
    text="%",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 24 * -1)
)

tarafsız_label=canvas.create_text(
    1080.71142578125,
    298.39984130859375,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 36 * -1)
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    1017.0,
    416.0008850097656,
    image=image_image_6
)

canvas.create_text(
    882.193359375,
    370.40118408203125,
    anchor="nw",
    text="Olumsuz Duygu \nOranı",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 19 * -1)
)

canvas.create_text(
    1060.90771484375,
    421.70001220703125,
    anchor="nw",
    text="%",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 24 * -1)
)

olumsuz_label=canvas.create_text(
    1080.71142578125,
    408.2000732421875,
    anchor="nw",
    text="00",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 36 * -1)
)

image_image_7 = PhotoImage(
    file=relative_to_assets("image_7.png"))
image_7 = canvas.create_image(
    1017.0,
    571.0001220703125,
    image=image_image_7
)

canvas.create_text(
    880.0,
    499.0001220703125,
    anchor="nw",
    text="Bir Sonraki Analiz için\nKalan Süre ",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 19 * -1)
)

image_image_8 = PhotoImage(
    file=relative_to_assets("image_8.png"))
image_8 = canvas.create_image(
    941.895263671875,
    567.0001220703125,
    image=image_image_8
)

image_image_9 = PhotoImage(
    file=relative_to_assets("image_9.png"))
image_9 = canvas.create_image(
    1016.0,
    598.6994018554688,
    image=image_image_9
)

image_image_10 = PhotoImage(
    file=relative_to_assets("image_10.png"))
image_10 = canvas.create_image(
    1017.08740234375,
    597.8497314453125,
    image=image_image_10
)

countdown_label=canvas.create_text(
    990.0,
    583.0,
    anchor="nw",
    text="05:00",
    fill="#FFFFFF",
    font=("Digital-7", 26 * -1)
)

image_image_11 = PhotoImage(
    file=relative_to_assets("image_11.png"))
image_11 = canvas.create_image(
    484.0,
    571.0001220703125,
    image=image_image_11
)

canvas.create_text(
    178.661865234375,
    496.3007507324219,
    anchor="nw",
    text="Sonuç",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 23 * -1)
)

sonuc_label=canvas.create_text(
    178.661865234375,
    528.700927734375,
    anchor="nw",
    text="Analiz sonucunda elde edilen bulgulara gore....",
    fill="#FFFFFF",
    font=("Poppins SemiBold", 20 * -1)
)

image_image_12 = PhotoImage(
    file=relative_to_assets("image_12.png"))
image_12 = canvas.create_image(
    484.0,
    302.0001220703125,
    image=image_image_12
)

canvas.create_text(
    178.661865234375,
    149.90040588378906,
    anchor="nw",
    text="Veri Grafiği",
    fill="#F5F6FA",
    font=("Poppins SemiBold", 23 * -1)
)

image_image_13 = PhotoImage(
    file=relative_to_assets("image_13.png"))
image_13 = canvas.create_image(
    79.0,
    302.0001220703125,
    image=image_image_13
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=update_title_to_twitter,
    relief="flat"
)
button_1.place(
    x=58.58837890625,
    y=155.30072021484375,
    width=43.19999313354492,
    height=43.20000457763672
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=update_title_to_reddit,
    relief="flat"
)
button_2.place(
    x=58.58837890625,
    y=234.499755859375,
    width=43.19999313354492,
    height=43.20000457763672
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command= update_title_to_telegram,
    relief="flat"
)
button_3.place(
    x=58.58837890625,
    y=313.700439453125,
    width=43.19999313354492,
    height=43.20000457763672
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command= open_to_PDF,
    relief="flat"
)
button_4.place(
    x=57.679931640625,
    y=392.89947509765625,
    width=43.19999313354492,
    height=43.20000457763672
)
window.resizable(False, False)
window.mainloop()
