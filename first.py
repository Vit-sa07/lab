import random
import pandas as pd


# Функция для исправления формата многочлена, конвертация в двоичный список
def poly_to_binary(poly_str):
    # Сначала разделим многочлен на отдельные члены
    terms = poly_str.split('+')
    # Определяем степень многочлена
    degree = int(terms[0].split('^')[1])
    # Создаем список с нулями размером степени многочлена + 1
    coeffs = [0] * (degree + 1)
    # Проходим по каждому члену многочлена и если там есть 'x', то устанавливаем 1
    # на соответствующей позиции в списке (учитываем, что 'x' без показателя степени соответствует x^1)
    for term in terms:
        if 'x' in term:
            if '^' in term:
                power = int(term.split('^')[1])
            else:
                power = 1
            coeffs[degree - power] = 1
        else:
            # Если это свободный член, то он соответствует x^0
            coeffs[-1] = 1
    return coeffs


# Функция для выполнения шага РСЛОС
def lfsr(taps, state):
    new_bit = sum(state[tap] for tap in taps) % 2
    # Сдвигаем состояние и добавляем новый бит
    state = state[1:] + [new_bit]
    return state, new_bit



# Многочлен для РСЛОС
poly = poly_to_binary('x^5 + x^2 + 1')


def is_lfsr_period_unique(poly, initial_state, period):
    generated_states = set()
    state = initial_state.copy()

    for _ in range(period):
        if tuple(state) in generated_states:
            # Если состояние уже было, значит период меньше ожидаемого
            return False
        generated_states.add(tuple(state))
        state, _ = lfsr(taps=[0, 2], state=state)  # Taps для x^5 и x^2

    # Если все состояния уникальны, период соответствует ожидаемому
    return True


max_attempts = 10000
for _ in range(max_attempts):
    # Генерируем случайное начальное состояние с условием, что оно не должно быть нулевым
    initial_state = [random.randint(0, 1) for _ in range(5)]
    if sum(initial_state) == 0:  # Проверяем, чтобы состояние не было нулевым
        continue

    # Проверяем уникальность состояний для этого начального состояния
    if is_lfsr_period_unique(poly, initial_state, 24):
        # Если состояния уникальны, выводим начальное состояние и прекращаем поиски
        break

# Выводим результат
print(initial_state)


def generate_lfsr_table_reversed(poly, initial_state, steps):
    state = initial_state.copy()
    lfsr_table = []

    # Получаем индексы тапов из многочлена (индексация начинается с 0 для x^0)
    taps = [len(poly) - i - 1 for i, x in enumerate(poly) if x == 1][1:]  # Исключаем x^0

    for step in range(steps):
        # Следующее состояние получается на основе тапов многочлена
        next_bit = sum(state[i] for i in taps) % 2
        state = state[:-1]  # Сдвигаем биты
        state.insert(0, next_bit)  # Вставляем новый бит на место старшего бита

        # Выводим состояние в обратном порядке (с младшего к старшему биту)
        lfsr_table.append((''.join(str(bit) for bit in state[::-1]), state[-1]))

    return lfsr_table


lfsr_table = generate_lfsr_table_reversed(poly, initial_state, 24)

# Создаем DataFrame из данных
df = pd.DataFrame(lfsr_table, columns=['Состояние регистра', 'Бит кольц. посыл.'])

# Добавляем столбец с номерами сдвигов
df.index += 1
df.reset_index(inplace=True)
df.rename(columns={'index': 'Номер сдвига'}, inplace=True)

print(df.head(24))
