# Функция для конвертации текста в байты
def text_to_bytes(text):
    return bytearray(text.encode('utf-8'))


# Функция для выполнения XOR двух массивов байтов
def xor_bytes(bytes1, bytes2):
    return bytearray(a ^ b for a, b in zip(bytes1, bytes2))


# Функция для конвертации байтов в текст
def bytes_to_text(bytes_array):
    return bytes_array.decode('utf-8', errors='ignore')


def bytearray_to_binary_string(byte_array):
    return ' '.join(format(byte, '08b') for byte in byte_array)


def lfsr(taps, state):
    while True:
        yield state[-1]
        new_bit = sum(state[tap] for tap in taps) % 2
        state = [new_bit] + state[:-1]


def create_scrambler_key_bytes(poly, initial_state, length):
    taps = [i for i, bit in enumerate(reversed(poly)) if bit]
    lfsr_gen = lfsr(taps, initial_state)
    return bytearray(next(lfsr_gen) for _ in range(length))


# Исходный текст
text = "Нельзя из яичницы снова сделать яйцо."

# Полином скремблера x^5 + x^2 + 1
poly = [4, 1]  # индексы x^5 и x^2 в обратном порядке, т.к. индексация начинается с x^0

# Начальное состояние регистра длиной 5 бит
initial_state = [1, 0, 1, 1, 0]  # предполагаемое начальное состояние

# Преобразуем исходный текст в биты
text_bytes = text_to_bytes(text)
binary_text_bytes = bytearray_to_binary_string(text_bytes)

# Создаем ключ скремблера, равный по длине байтам текста
scrambler_key_bytes = create_scrambler_key_bytes(poly, initial_state, len(text_bytes))

# Производим операцию XOR между байтами исходного текста и байтами ключа
encrypted_bytes = xor_bytes(text_bytes, scrambler_key_bytes)

# Преобразуем зашифрованные байты обратно в текст
encrypted_text = bytes_to_text(encrypted_bytes)

# Производим операцию XOR между зашифрованными байтами и байтами ключа для расшифровки
decrypted_bytes = xor_bytes(encrypted_bytes, scrambler_key_bytes)
binary_decrypted_bytes = bytearray_to_binary_string(decrypted_bytes)
# Преобразуем расшифрованные байты обратно в текст
decrypted_text = bytes_to_text(decrypted_bytes)
binary_key = bytearray_to_binary_string(scrambler_key_bytes)
binary_encrypted_text = bytearray_to_binary_string(encrypted_bytes)

# Выводим информацию
print(f"Исходный текст: {text}")
print(f"Исходный текст в битах: {binary_text_bytes}")
print(f"Ключ скремблера в двоичном коде: {binary_key}")
print(f"Зашифрованный текст в двоичном коде: {binary_encrypted_text}")
print(f"Зашифрованный текст: {encrypted_text}")
print(f"Расшифрованный текст в битах: {binary_decrypted_bytes}")
print(f"Расшифрованный текст: {decrypted_text}")
print(f"Длина исходного текста в битах: {len(text_bytes)}")
print(f"Длина ключа скремблера: {len(scrambler_key_bytes)}")
