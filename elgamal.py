from Crypto.Util.number import getPrime, GCD, inverse
import hashlib
import random

def generate_keys(elgamal_keysize):
    p = getPrime(elgamal_keysize)  # Получаем простое число
    g = random.randint(2, p-2)  # Выбираем генератор группы
    x = random.randint(1, p-2)  # Секретный ключ
    y = pow(g, x, p)  # Вычисляем открытый ключ y = g^x mod p
    return (p, g, y), x

def sign_elgamal(p, g, x, message):
    h = int(hashlib.sha256(message).hexdigest(), 16)
    k = random.randint(1, p-2)
    while GCD(k, p-1) != 1:
        k = random.randint(1, p-2)
    r = pow(g, k, p)
    k_inv = inverse(k, p-1)
    s = (k_inv * (h - x * r)) % (p - 1)
    return r, s

def verify_elgamal(p, g, y, message, signature):
    h = int(hashlib.sha256(message).hexdigest(), 16)
    r, s = signature
    v1 = pow(y, r, p) * pow(r, s, p) % p
    v2 = pow(g, h, p)
    return v1 == v2

# Пример использования
elgamal_keysize = 2048
public_key, private_key = generate_keys(elgamal_keysize)
message = "Нельзя из яичницы снова сделать яйцо.".encode('utf-8')
signature = sign_elgamal(public_key[0], public_key[1], private_key, message)
verification_result = verify_elgamal(public_key[0], public_key[1], public_key[2], message, signature)

# Вывод результатов
print(f"Исходное сообщение: {message.decode('utf-8')}")
signature_hex = f"{signature[0]:X}{signature[1]:X}"
print(f"Цифровая подпись исходного сообщения: {signature_hex}")
print(f"Открытый ключ:\np: {public_key[0]}\ng: {public_key[1]}\ny: {public_key[2]}")
print(f"Проверяемое сообщение: {message.decode('utf-8')}")
print(f"Результат верификации: {'Верификация прошла успешно. Цифровая подпись верна.' if verification_result else 'Подпись недействительна.'}")
