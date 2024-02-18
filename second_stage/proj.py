import tkinter as tk
from heapq import heappush, heappop, heapify
from collections import defaultdict


# Шаг 1: Создание дерева Хаффмана
def huffman_tree(data):
    frequencies = defaultdict(int)
    for char in data:
        frequencies[char] += 1

    heap = [[weight, [symbol, ""]] for symbol, weight in frequencies.items()]
    heapify(heap)

    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# Шаг 2: Кодирование сообщения
def encode(data):
    tree = huffman_tree(data)
    codes = {sym: code for sym, code in tree}
    encoded_data = ''.join(codes[sym] for sym in data)
    return encoded_data, codes

# Шаг 3: Декодирование закодированного сообщения
def decode(encoded_data, codes):
    curr_code = ''
    decoded_data = ''
    for bit in encoded_data:
        curr_code += bit
        for symbol, code in codes.items():
            if code == curr_code:
                decoded_data += symbol
                curr_code = ''
                break
    return decoded_data


def on_submit():
    flag = mode_var.get()
    if flag:
        data = input_text.get()
        codes = {}
        if codes_entry.get():
            codes_list = codes_entry.get().split()
            for i in range(0, len(codes_list), 2):
                codes[codes_list[i]] = codes_list[i+1]
        decoded_data = decode(data, codes)
        output_label.config(text="Декодированное сообщение: " + decoded_data)
    else:
        data = input_text.get()
        encoded_data, codes = encode(data)
        output_label.config(text="Закодированное сообщение: " + encoded_data + "\nКод: " + str(codes))

root = tk.Tk()
root.title("Шифр Хаффмана")
root.configure(bg='pink')  # Розовый фон окна

mode_var = tk.IntVar()
mode_var.set(0)

mode_label = tk.Label(root, text="Выберите режим:", font=("Helvetica", 16), bg='pink')  # Увеличиваем размер и меняем шрифт
mode_label.pack()

mode_radio_encode = tk.Radiobutton(root, text="Кодирование", variable=mode_var, value=0, font=("Helvetica", 14), bg='pink')  # Увеличиваем размер и меняем шрифт
mode_radio_encode.pack()
mode_radio_decode = tk.Radiobutton(root, text="Декодирование", variable=mode_var, value=1, font=("Helvetica", 14), bg='pink')  # Увеличиваем размер и меняем шрифт
mode_radio_decode.pack()

input_label = tk.Label(root, text="Введите сообщение:", font=("Helvetica", 16), bg='pink')  # Увеличиваем размер и меняем шрифт
input_label.pack()
input_text = tk.Entry(root, font=("Helvetica", 14))
input_text.pack()

codes_label = tk.Label(root, text="Введите коды (через пробел):", font=("Helvetica", 16), bg='pink')  # Увеличиваем размер и меняем шрифт
codes_label.pack()
codes_entry = tk.Entry(root, font=("Helvetica", 14))
codes_entry.pack()

submit_button = tk.Button(root, text="Отправить", command=on_submit, font=("Helvetica", 14), bg='hot pink', fg='white')  # Увеличиваем размер и меняем шрифт, добавляем розовую кнопку
submit_button.pack()

output_label = tk.Label(root, text="", font=("Helvetica", 16), bg='pink')  # Увеличиваем размер и меняем шрифт
output_label.pack()

root.mainloop()
