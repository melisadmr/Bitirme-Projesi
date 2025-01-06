import pandas as pd
import re

# Veri setini okur
df = pd.read_csv('data.csv')

# Gereksiz sütunları kaldırma
df = df.drop(columns=['media'], errors='ignore')

# Boş değerleri kaldırır
df = df.dropna()

# Metin temizleme fonksiyonu
def temizle(metin):
    metin = metin.lower()
    metin = re.sub(r'[^\w\s]', '', metin)
    metin = re.sub(r'\s+', ' ', metin).strip()
    return metin

# Metni temizle
df['text'] = df['text'].apply(temizle)
#['Başlık'] = df['Başlık'].apply(temizle)


# Temizlenmiş veriyi kaydet
df.to_csv('Cleared_Data.csv', index=False)
