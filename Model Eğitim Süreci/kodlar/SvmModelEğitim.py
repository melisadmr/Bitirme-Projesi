import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc

# Veri setini yükle
df = pd.read_csv('Reddit_etiketlenmis_data1.csv')
turkish_stopwords = ["ve", "bu", "bir", "için", "de", "ile", "o", "ben", "sen", "biz", "onlar", "ama", "çok", "daha"]

# Başlık ve gönderi içeriğini birleştir
df['metin'] = df['Başlık'] + " " + df['Gönderi İçeriği']

# Etiketlerin dağılımını görselleştirme
plt.figure(figsize=(6, 4))
sns.countplot(x='etiket', data=df, palette='viridis')
plt.title('Etiket Dağılımı')
plt.xlabel('Etiket')
plt.ylabel('Frekans')
plt.show()

# Kelime uzunluğu dağılımı
df['kelime_uzunlugu'] = df['metin'].apply(lambda x: len(x.split()))
plt.figure(figsize=(6, 4))
sns.histplot(df['kelime_uzunlugu'], bins=30, kde=True, color='purple')
plt.title('Kelime Uzunluğu Dağılımı')
plt.xlabel('Kelime Uzunluğu')
plt.ylabel('Frekans')
plt.show()

# Özellikler ve etiketleri ayır
X = df['metin']  # Başlık ve içerikten oluşan birleşik metin
y = df['etiket']  # Etiketler (tarafsız / olumsuz)

# Metni sayısal verilere dönüştürmek için TF-IDF kullanma
vectorizer = TfidfVectorizer(stop_words=turkish_stopwords)
X_tfidf = vectorizer.fit_transform(X)

# TF-IDF kelime önem skorları
tfidf_scores = pd.DataFrame({'kelime': vectorizer.get_feature_names_out(), 'tfidf_degeri': np.asarray(X_tfidf.mean(axis=0)).ravel()})
tfidf_scores = tfidf_scores.sort_values(by='tfidf_degeri', ascending=False).head(20)
plt.figure(figsize=(10, 5))
sns.barplot(data=tfidf_scores, x='tfidf_degeri', y='kelime', palette='viridis')
plt.title('En Önemli 20 Kelimenin TF-IDF Skorları')
plt.xlabel('TF-IDF Skoru')
plt.ylabel('Kelime')
plt.show()

# Veriyi eğitim ve test olarak ayır
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.3, random_state=42)

# SVM modelini oluştur ve eğit
svm_model = SVC(kernel='linear', probability=True)  # Lineer kernel kullanımı
svm_model.fit(X_train, y_train)

# Test verisiyle tahminler yap
y_pred = svm_model.predict(X_test)

# Sonuçları değerlendirme
print(classification_report(y_test, y_pred))

# Karışıklık matrisi
def plot_confusion_matrix(cm, classes, title='Karışıklık Matrisi'):
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title(title)
    plt.ylabel('Gerçek Etiket')
    plt.xlabel('Tahmin Edilen Etiket')
    plt.show()

cm = confusion_matrix(y_test, y_pred, labels=svm_model.classes_)
plot_confusion_matrix(cm, classes=svm_model.classes_)

# Precision, recall, F1-score grafiği
report = classification_report(y_test, y_pred, output_dict=True)
metrics_df = pd.DataFrame(report).transpose().iloc[:-1, :-1]
plt.figure(figsize=(8, 5))
metrics_df[['precision', 'recall', 'f1-score']].plot(kind='bar', figsize=(10, 6))
plt.title('Precision, Recall ve F1-Score Değerleri')
plt.ylabel('Skor')
plt.xticks(rotation=45)
plt.show()

# ROC-AUC eğrisi (Binary sınıflandırma için)
if len(svm_model.classes_) == 2:  # Sadece iki sınıf için geçerli
    y_score = svm_model.decision_function(X_test)
    fpr, tpr, _ = roc_curve(y_test.map({svm_model.classes_[0]: 0, svm_model.classes_[1]: 1}), y_score)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Eğrisi')
    plt.legend(loc='lower right')
    plt.show()

# Modeli kaydetme
joblib.dump(svm_model, 'svm_model.pkl')  # SVM modelini kaydettik

# TF-IDF Vectorizer'ı kaydetme
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')  # TF-IDF Vectorizer'ı da kaydettik
