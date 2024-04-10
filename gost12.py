from hashlib import sha256
from random import randint


a = 4
b = 3
p = 11
G = (0, 5)
n = 7
d = 6

# Функция умножения точки на число
def ecc_multiply(point, k, a, p):
    (x, y) = point
    (x_k, y_k) = point
    for i in range(1, k):
        (x_k, y_k) = ecc_add((x_k, y_k), (x, y), a, p)
    return (x_k, y_k)

# Функция сложения двух точек на эллиптической кривой
def ecc_add(p1, p2, a, p):
    (x1, y1) = p1
    (x2, y2) = p2
    if p1 == p2:
        lmbd = (3 * x1 * x1 + a) * pow(2 * y1, -1, p)
    else:
        lmbd = (y2 - y1) * pow(x2 - x1, -1, p)
    lmbd = lmbd % p
    x3 = (lmbd * lmbd - x1 - x2) % p
    y3 = (lmbd * (x1 - x3) - y1) % p
    return (x3, y3)

# Хеш-функция
def hash_function(message):
    return int(sha256(message.encode('utf-8')).hexdigest(), 16)

# Подпись сообщения
def sign(message, G, a, p, n, d):
    e = hash_function(message)
    e = e % n
    if e == 0:
        e = 1

    r = 0
    s = 0
    while r == 0 or s == 0:
        k = randint(1, n-1)
        C = ecc_multiply(G, k, a, p)
        r = C[0] % n
        s = (r * d + k * e) % n
    return (r, s)

# Проверка подписи
def verify(message, signature, G, a, p, n, Q):
    (r, s) = signature
    if r <= 0 or r >= n or s <= 0 or s >= n:
        return False

    e = hash_function(message)
    e = e % n
    if e == 0:
        e = 1

    v = pow(e, -1, n)
    z1 = (s * v) % n
    z2 = (-r * v) % n
    C = ecc_add(ecc_multiply(G, z1, a, p), ecc_multiply(Q, z2, a, p), a, p)

    R = C[0] % n
    return R == r

# Тестирование алгоритма
message = "ДАВИ"
signature = sign(message, G, a, p, n, d)
print("Подпись:", signature)

Q = ecc_multiply(G, d, a, p)
print("Публичный ключ (x, y):", Q)

verified = verify(message, signature, G, a, p, n, Q)
print("Подпись верна:", verified)
