from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

# Генерация ключевой пары RSA
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Создание хэша сообщения
message = "Нельзя из яичницы снова сделать яйцо.".encode('utf-8')
h = SHA256.new(message)

# Создание подписи
signature = pkcs1_15.new(key).sign(h)

# Проверка подписи
try:
    pkcs1_15.new(key.publickey()).verify(h, signature)
    print("Подпись действительна.")
except (ValueError, TypeError):
    print("Подпись недействительна.")
