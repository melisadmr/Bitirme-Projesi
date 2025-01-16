# Sosyal Medya Tehdit Analizi Projesi
Bu proje, Twitter(x),Telegram ve Reddit platformlarından gerçek zamanlı veri çekme ve bu verileri doğal dil işleme (NLP) teknikleriyle analiz ederek tehdit içeriklerini tespit etme amacı taşır. Proje, Python programlama dili kullanılarak geliştirilmiş ve çeşitli kütüphanelerle desteklenmiştir.

## Table of Contents

- [Giriş](#giris)
- [Özellikler](#ozellikler)
- [Kullanılan Teknolojiler](#kullanilan-teknolojiler)
- [Proje Arayüzü](#proje-arayuzu)
- [Gelecekteki Çalışmalar](#gelecekteki-calismalar)
## Giriş

Sosyal medya platformları hem etkileşim hem de kötü amaçlı faaliyetler için bir merkez haline geldi. Bu proje, gerçek zamanlı veri işleme ve makine öğrenimi kullanarak 

Analiz şunlara odaklanır:
- Potansiyel tehdit unsurlarını belirleme
- Toplanan verilerdeki kalıpları yorumlama
- Görsel içgörüler ve eyleme dönüştürülebilir raporlar sağlama

## Özellikler

- **Veri Toplama**: API'ler veya web kazıma yoluyla birden fazla sosyal medya platformundan veri toplamak.
- **Tehdit Analizi**: Riskli davranışları veya içeriği belirlemek için makine öğrenimi modellerini kullanmak.
- **Görselleştirme**: Kullanıcılar için anlaşılması kolay raporlar oluşturmak.
- **Özelleştirilebilir Arayüz**: Daha iyi etkileşim için kullanıcı dostu gösterge paneli.

## Kullanılan Teknolojiler

- **Programlama Dilleri**: Python,
- **Kütüphaneler**: Pandas, NumPy, Scikit-learn, Matplotlib,Praw,Telethon
- **Diğer**: Gerçek zamanlı veri çekmek için API'ler

## Proje Arayüzü
![image](https://github.com/user-attachments/assets/cadb55df-fe7f-4d2f-a3e2-024931410763)

- Sosyal medya verilerinin analizi sırasında elde edilen tahminlerin yalnızca sayısal
 sonuçlar olarak kalması yerine, bu verilerin kullanıcı tarafından kolay anlaşılabilir
 olması için görselleştirilmektedir. Bu bağlamda, tehdit tespiti için modellenen
 SVMmodeli analiz edilen metinlerin olumsuz veya tarafsız olarak sınıflandırılmasını
 sağlamaktadır. Bu sınıflandırma sonuçları, görselleştirme teknikleri ile desteklenerek
 kullanıcıya sunulmaktadır.


### Grafik Alanı

![Grafik Alanı](https://github.com/user-attachments/assets/e0d7fc81-b7c1-4599-b028-ed57c84534be)

- Görselleştirme işlemi için pasta grafik seçilmiştir. Pasta grafik, olumsuz ve tarafsız
 veri oranlarını net bir şekilde görselleştirmektedir. Analiz raporlarının net şekilde
 görselleştirilmesi sonuçların kolay yorumlanabilmesini de sağlamaktadır.


### Analiz Sonucu Oranları Bilgilendirme Kartları

![veriMetinalanlarıgörsel](https://github.com/user-attachments/assets/cf96c837-08b0-4b2e-8b29-44d235e8cffc)

- Verilerin görselleştirilmesi işleminde arayüzde gösterilen bir diğer görsel unsur da
 analiz sonucunda elde edilen olumsuz duygu oranı, tarafsız duygu oranı ve toplam
 çekilen veri sayısının yazdığı metin alanlarıdır. Bu alanlar kullanıcı deneyimini
 artırmak amacıyla kullanıcıya sunulmaktadır.

### Analiz Sonucu Yorum Alanı

![SonuçAlanıGörsel](https://github.com/user-attachments/assets/f3a547c1-69ea-4ec2-8c44-2deb941767aa)
- Bu alanda kullanıcıya analiz sonucunda elde edilen bulgular verilerek kullanıcının
 analiz sonucunu daha net anlamlandırabilmesi sağlanmaktadır. Ayrıca bu
 alanda olumsuz olarak sınıflandırılan verilerin içerisinde hangi tehdit kelimelerinin
 bulunduğu da gösterilmektedir.

### Geri Sayım Alanı

![GeriSayımAlanıGörsel](https://github.com/user-attachments/assets/576ccde5-b49c-407a-a554-3f76c9d9fdb7)

- Uygulama analizleri her 5 dakikada bir tekrar etmektedir. Kullanıcının bu süreyi
 kolay bir şekilde takip edebilmesi için arayüz ekranında bir geri sayım alanına yer
 verilmiştir.

### Button Bar

![ButtonBarGörsel](https://github.com/user-attachments/assets/faebc662-aae8-4c88-9bff-4356020e0f20)


- Bu projede Twitter (X), Reddit ve Telegram platformları için tehdit analizi
 modelleri geliştirilmiştir. Bu kısımda analiz işlemine bir başla komutu verebilmek
 için platformlar nezlinde–ki bunlar Twitter butonu, Reddit butonu ve Telegram
 butonudur– 3 buton oluşturulmuştur. Butonların görevi o platform için analiz
 işlemini başlatıp arayüze yansıtma görevini gerçekleştirmektir. Platformların
 logoları ile bütünleşmiş bu butonlar kullanıcı için platformlar arasında tercih
 yapabilme şansı tanımıştır. Butona tıklanılmasıyla beraber platformdan veri çekme
 işlemi başlar, analiz işlemini gerçekleştirir ve arayüze sonucu yansıtır. Kullanıcı
 başka bir platform butonuna tıklayana kadar en son seçtiği platform için analiz
 yapılmaya devam edecektir.



## Gelecekteki Çalışmalar

- Daha fazla sosyal medya platformu için yapı oluşturmak.
- Daha iyi doğruluk için gelişmiş makine öğrenimi modellerini entegre etmek.

[Melisa Demir](https://github.com/melisadmr) ve [Duygu Gözde KAYABAŞI](https://github.com/Duygugozde33) tarafından geliştirilmiştir.
Bu proje hakkında sorular ve görüşleriniz için bizimle iletişime geçmeyi unutmayın!! 😊
