import pandas as pd
import joblib
import re
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Metin temizleme fonksiyonu
def metin_temizleme(metin):
    if not isinstance(metin, str):
        return ""
    metin = metin.lower()
    metin = re.sub(r'[^\w\s]', '', metin)
    return metin

# Tahmin yapma fonksiyonu
def tahmin_yap(csv_dosya_adi, model_dosya_adi, vectorizer_dosya_adi, cikti_dosya_adi):
    # Model ve vectorizer'ı yükle
    svm_model = joblib.load(model_dosya_adi)
    tfidf_vectorizer = joblib.load(vectorizer_dosya_adi)

    # CSV dosyasını yükle
    df = pd.read_csv(csv_dosya_adi)
    df["text"]= df["Başlık"] + " " + df["Gönderi İçeriği"]
    

    
    # Metinleri temizle
    df['cleaned_text'] = df['text'].apply(metin_temizleme)

    # TF-IDF dönüşümü
    X = tfidf_vectorizer.transform(df['cleaned_text'])

    # Tahmin yap
    tahminler = svm_model.predict(X)

    # Tehdit seviyelerini belirle
    df['tehdit_seviyesi'] = ["Düşük" if t == "Tarafsız" else "Yüksek" for t in tahminler]

    # Tahmin sonuçlarını CSV'ye kaydet
    df.to_csv(cikti_dosya_adi, index=False)
    print(f"Tahminler tamamlandı ve '{cikti_dosya_adi}' olarak kaydedildi.")
    
    return df

# Tehdit seviyelerine göre mesaj uzunluğu görselleştirme
def uzunluk_tehdit_gorsellestirme(df):
    df['mesaj_uzunlugu'] = df['cleaned_text'].apply(len)

    # Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='tehdit_seviyesi', y='mesaj_uzunlugu', data=df, palette="coolwarm")
    plt.title("Tehdit Seviyelerine Göre Mesaj Uzunluğu Dağılımı")
    plt.xlabel("Tehdit Seviyesi")
    plt.ylabel("Mesaj Uzunluğu (Karakter)")
    plt.show()

# Kelime bulutu oluşturma
def kelime_bulutu(df):
    for seviye in df['tehdit_seviyesi'].unique():
        metinler = df[df['tehdit_seviyesi'] == seviye]['cleaned_text'].str.cat(sep=' ')
        wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(metinler)

        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.title(f"{seviye} Tehdit Seviyesi İçin Kelime Bulutu")
        plt.axis('off')
        plt.show()

# Tehdit seviyelerinin pasta ve çubuk grafiği
def gorunus_olustur(df):
    # Tehdit seviyelerine göre sayıları hesapla
    tehdit_sayilari = df['tehdit_seviyesi'].value_counts()

    # Pasta grafiği
    plt.figure(figsize=(8, 6))
    tehdit_sayilari.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'red'])
    plt.title("Tehdit Seviyeleri Dağılımı")
    plt.ylabel("")
    plt.show()

    # Çubuk grafiği
    plt.figure(figsize=(8, 6))
    tehdit_sayilari.plot(kind='bar', color=['lightgreen', 'red'])
    plt.title("Tehdit Seviyeleri Dağılımı")
    plt.xlabel("Tehdit Seviyesi")
    plt.ylabel("Mesaj Sayısı")
    plt.show()

# Ana fonksiyon
def main():
    # Dosya yolları
    csv_dosya_adi = "Reddit_etiketlenmis_data1.csv"  # Tahmin yapılacak veri dosyası
    model_dosya_adi = "svm_model.pkl"  # SVM model dosyası
    vectorizer_dosya_adi = "tfidf_vectorizer.pkl"  # TF-IDF vektörleştirici dosyası
    cikti_dosya_adi = "sonuc_reddit.csv"  # Tahmin sonuçlarının kaydedileceği dosya

    # Tahmin yap
    df = tahmin_yap(csv_dosya_adi, model_dosya_adi, vectorizer_dosya_adi, cikti_dosya_adi)

    # Görselleştirme
    gorunus_olustur(df)
    uzunluk_tehdit_gorsellestirme(df)
    kelime_bulutu(df)

# Çalıştır
if __name__ == "__main__":
    main()
