from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS

# Генерация ключевой пары ECDSA
key = ECC.generate(curve='P-256')
private_key = key.export_key(format='PEM')
public_key = key.public_key().export_key(format='PEM')

# Создание хэша сообщения
message = "Нельзя из яичницы снова сделать яйцо.".encode('utf-8')
h = SHA256.new(message)

# Создание подписи
signer = DSS.new(key, 'fips-186-3')
signature = signer.sign(h)

# Проверка подписи
verification_result = ""
try:
    verifier = DSS.new(key.public_key(), 'fips-186-3')
    verifier.verify(h, signature)
    verification_result = "Верификация прошла успешно. Цифровая подпись верна."
except ValueError:
    verification_result = "Подпись недействительна."

# Формирование вывода
print(f"Исходное сообщение: {message.decode('utf-8')}")
print(f"Цифровая подпись исходного сообщения: {signature.hex().upper()}")
print(f"Открытый ключ:\n{public_key}")
print(f"Проверяемое сообщение: {message.decode('utf-8')}")
print(f"Результат верификации: {verification_result}")
