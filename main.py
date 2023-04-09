import tkinter as tk
import random
from tkinter import filedialog
import time


class TypingTrainer:
    def __init__(self, master):
        self.errors_label = None
        self.accuracy_label_s = None
        self.master = master
        master.title("Typing Trainer")
        master.geometry("400x400")

        # список дефолтных слов для тренировки
        self.words = ['apple', 'banana', 'cherry', 'orange', 'kiwi', 'pear', 'grape', 'pineapple', 'lemon', 'peach']

        # отслеживание уровня
        self.level = 1
        self.step = 1

        # для проверки вводимого символа
        check = (root.register(self.check_letter), "%P")

        # Создание виджетов
        self.label = tk.Label(master, text="Для проверки слова нажмите Enter")
        self.textbox = tk.Entry(master, validate="key", validatecommand=check)
        self.display_word = tk.Label(master, text="")
        self.accuracy_label = tk.Label(master, text="")
        self.wpm_label = tk.Label(master, text="")
        self.button_stat = tk.Button(text="Показать статистику", command=self.click)
        self.level_label = tk.Label(master, text=f"Уровень: {self.level}")
        self.button_words = tk.Button(text="Загрузить задание", command=self.upload)
        self.button_def = tk.Button(text="Использовать встроенный словарь", command=self.default_file)
        self.quit = tk.Button(root, text="Выйти", command=self.quit)

        # Упаковка виджетов
        self.button_words.pack(pady=10)
        self.button_def.pack(pady=10)
        self.quit.pack(pady=10)

        # Настройка клавиатуры
        self.textbox.bind("<Return>", self.check_word)
        self.textbox.focus_set()

        # Запуск программы
        self.current_word = ""
        self.correct_chars = 0
        self.total_chars = 0
        self.wpm = 0
        self.accuracy = 0
        self.i = 0
        self.mistakes = 0
        self.start_time = None

    def upload(self):
        filepath = filedialog.askopenfilename()
        if filepath != "":
            with open(filepath, "r") as file:
                text = file.read()
                self.words = list(text.split(' '))

        self.new_word()
        self.label.pack(pady=10)
        self.textbox.pack(pady=10)
        self.display_word.pack(pady=10)
        self.accuracy_label.pack(pady=10)
        self.wpm_label.pack(pady=10)
        self.button_stat.pack(pady=10)
        self.level_label.pack(anchor="center")

        self.button_def.pack_forget()
        self.button_words.pack_forget()

        self.start_time = time.time()

    def quit(self):
        with open("statistics.txt", "a") as file:
            file.write(f"Скорость печати: {round(self.wpm, 2)} символов в секунду, Количество ошибок: {self.mistakes}, уровень: {self.level} \n")
        root.destroy()

    def default_file(self):
        self.new_word()
        self.label.pack(pady=10)
        self.textbox.pack(pady=10)
        self.display_word.pack(pady=10)
        self.accuracy_label.pack(pady=10)
        self.wpm_label.pack(pady=10)
        self.button_stat.pack(pady=10)
        self.level_label.pack(anchor="center")
        self.button_def.pack_forget()
        self.button_words.pack_forget()

        self.start_time = time.time()

    def click(self):
        ps = time.time()

        window = tk.Tk()
        window.title("Статистика")
        window.geometry("400x300")

        self.accuracy_label_s = tk.Label(window, text="")
        self.errors_label = tk.Label(window, text="")

        self.accuracy_label_s.pack(pady=10)
        self.errors_label.pack(pady=20)

        self.errors_label.config(text=f"Количество ошибок: {self.mistakes}")
        self.accuracy_label_s.config(text=f"Точность: {round(self.accuracy, 2)}%")

        self.start_time += time.time() - ps  # не учитываем время, потраченное на меню

    def check_letter(self, newval):
        if newval == '':
            self.i = 0
            return True

        if self.i < min(len(self.current_word), len(newval)) and self.current_word[self.i] == newval[self.i]:
            self.i += 1
            self.label.config(text="Отлично!")
            return True
        else:
            self.label.config(text="Неправильно!")
            self.mistakes += 1
            self.total_chars += 1
            return False

    def new_word(self):
        # выбор случайных слов из списка
        self.current_word = ' '.join(random.choices(population=self.words, k=self.level))

        self.display_word.config(text=self.current_word)

    def check_word(self, event):
        # проверка правильности введенного слова
        self.level_label.config(text=f"Уровень: {self.level}")

        if self.textbox.get() == self.current_word:
            self.label.config(text="Отлично!")
            self.new_word()
            self.correct_chars += len(self.current_word)
            self.total_chars += len(self.current_word)
            self.textbox.delete(0, tk.END)

            self.step += 1  # следующий шаг
            self.level = self.step // 5 + 1  # новый уровень
        else:
            self.label.config(text="Неправильно!")
            self.mistakes += 1
            self.total_chars += 1

        # обновление точности и скорости печати
        self.accuracy = (self.correct_chars / self.total_chars) * 100
        self.accuracy_label.config(text=f"Точность: {round(self.accuracy, 2)}%")
        if self.start_time:
            elapsed_time = (time.time() - self.start_time) # секунд
            self.wpm = self.total_chars / elapsed_time
            self.wpm_label.config(text=f"Скорость печати: {round(self.wpm, 2)} символов в секунду")


root = tk.Tk()
typing_trainer = TypingTrainer(root)
root.mainloop()