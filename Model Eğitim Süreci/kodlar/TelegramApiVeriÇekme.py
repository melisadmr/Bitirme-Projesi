from telegram.client import Telegram

# Telegram API kimlik bilgileri
api_id = 'API ID' #TELEGRAM API'DEN ELDE EDİLEN API ID BU LANA YAZILIR
api_hash = 'API HASH'
phone_number = '+90xxxxxxxxx' #BU ALANA VERİ ÇEKMEK İÇİN KULLANILACAK TELEGRAM HESABINA AİT TELEFON NUMARASI YAZILMALI


# Telegram istemcisi başlatma
tg = Telegram(
    api_id=api_id,
    api_hash=api_hash,
    phone=phone_number,
    database_encryption_key='my_secret_key',  # Veritabanı şifreleme anahtarı
)
def get_group_messages(chat_id):
    messages = tg.get_chat_history(chat_id=chat_id)
    for message in messages['messages']:
        print(message['content']['text']['text'])

chat_id = 'CHAT ID' # BU ALANA TELEGRAMDAN ELDE ETTİĞİMİZ CHAT ID BİLGİSİ YAZILMALIDIR
try:
    tg.login()
except Exception as e:
    print(f"Login failed: {e}")

try:
    get_group_messages(chat_id)
except Exception as e:
    print(f"Failed to get messages: {e}")

# Gruba ait mesajları almak için fonksiyon



# Grup ID'si ile mesajları çekin


