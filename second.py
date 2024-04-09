from first import df, poly_to_binary
import pandas as pd

# Многочлен для 4-битного РСЛОС
poly_4bit = poly_to_binary('x^4 + x + 1')

# Функция для генерации таблицы РСЛОС для 4-битного регистра, используя многочлен x^4 + x + 1
def generate_lfsr_table_4bit(poly, initial_state, steps):
    taps = [len(poly) - i - 1 for i, x in enumerate(poly) if x == 1][1:]
    state = initial_state.copy()
    lfsr_table = []
    for step in range(steps):
        next_bit = sum(state[i] for i in taps) % 2
        state = state[:-1]
        state.insert(0, next_bit)
        lfsr_table.append((''.join(str(bit) for bit in state[::-1]), state[-1]))
    return lfsr_table

# Генерация таблицы для 4-битного РСЛОС
initial_state_4bit = [0, 1, 0, 1]
lfsr_table_4bit = generate_lfsr_table_4bit(poly_4bit, initial_state_4bit, 35)

# Создаем DataFrame из данных для второго задания
df_4bit = pd.DataFrame(lfsr_table_4bit, columns=['Состояние регистра 2', 'Бит кольц. посыл. 2'])

# Добавляем столбец с номерами сдвигов
df_4bit.index += 1
df_4bit.reset_index(inplace=True)
df_4bit.rename(columns={'index': 'Номер сдвига'}, inplace=True)

# Объединяем результаты первого и второго задания в одном DataFrame
combined_df = pd.merge(df, df_4bit, on='Номер сдвига', how='left')

# Переименовываем столбцы
combined_df.rename(columns={
    'Состояние регистра': 'Состояние регистра 1',
    'Бит кольц. посыл.': 'Бит кольц. посыл. 1'
}, inplace=True)


combined_df['Бит код. посыл.'] = combined_df['Бит кольц. посыл. 1'] ^ combined_df['Бит кольц. посыл. 2']


print(combined_df.head(35))


combined_df.to_excel("combined_lfsr_results.xlsx", index=False)