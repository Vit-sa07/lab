from pygost import gost3410
from pygost.utils import hexdec
from pygost import gost34112012

# Генерация ключей
def generate_keys():
    curve = gost3410.CURVES["id-GostR3410-2001-CryptoPro-A-ParamSet"]
    prv = gost3410.private_key(curve)
    pub = gost3410.public_key(curve, prv)
    return prv, pub

# Хеширование сообщения
def create_hash(message):
    return gost34112012.GOST34112012(message.encode()).digest()

# Создание подписи
def create_signature(private_key, hash_value):
    curve = gost3410.CURVES["id-GostR3410-2001-CryptoPro-A-ParamSet"]
    return gost3410.sign(curve, private_key, hash_value)

# Проверка подписи
def verify_signature(public_key, hash_value, signature):
    curve = gost3410.CURVES["id-GostR3410-2001-CryptoPro-A-ParamSet"]
    try:
        return gost3410.verify(curve, public_key, hash_value, signature)
    except gost3410.GOST3410Error:
        return False

# Основная функция для демонстрации создания и проверки подписи
def main():
    prv_key, pub_key = generate_keys()
    message = "Нельзя из яичницы снова сделать яйцо."
    hash_value = create_hash(message)
    signature = create_signature(prv_key, hash_value)

    print(f"Сообщение: {message}")
    print(f"Хеш: {hash_value.hex()}")
    print(f"Подпись: {signature.hex()}")

    verification_result = verify_signature(pub_key, hash_value, signature)
    print("Подпись действительна." if verification_result else "Подпись недействительна.")

if __name__ == "__main__":
    main()
