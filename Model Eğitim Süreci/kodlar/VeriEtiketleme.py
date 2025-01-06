import pandas as pd

# Veri setini oku
df = pd.read_csv('data.csv')

# Olumsuz  kelime listesi
olumsuz_kelimeler = ["tehdit", "saldırı", "korku", "düşman", "zarar", "risk","patlama","pkk","terorist","bomba","öldür","bomba","bıçak","saldırgan","darbe","ölüm","istismar","şiddet","infaz","hırsızlık","cinsel istismar","taciz","tecavüz","iç savaş","dolandırıcılık","siber saldırı","siber tehdit","ajan","hakaret","yalan"]
# Boş hücreleri doldurma
df["text"] = df["text"].fillna("")  # NaN değerlerini boş string ile doldur

# Tüm hücreleri stringe çevirme
df["text"] = df["text"].astype(str)

# Etiketleme fonksiyonu
def etiketle(metin):
    # Boş hücreleri doldurma

    metin = metin.lower()  # Metni küçük harfe çevir
    olumsuz_var = any(kelime in metin for kelime in olumsuz_kelimeler)
   
    if olumsuz_var:
        return "Olumsuz"
   
    else:
        return "Tarafsız"
    

# Veriyi etiketler
df['etiket'] = df['text'].apply(etiketle)

# Etiketlenmiş veriyi csv'ye kaydet
df.to_csv('labeled_data.csv', index=False)
