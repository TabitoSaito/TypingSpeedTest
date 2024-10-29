import tkinter as tk
import time
import random

NUMBER_OF_WORDS: int = 15


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.height: int = 600
        self.width: int = 600
        self.geometry(f"{self.width}x{self.height}")
        self.title("Typing Speed Test")

        self.cur_word: str = "word"
        self.cur_i_letter: int = 0
        self.cur_i_word: int = 0
        self.cur_word_start: float = time.time()
        self.start: float = time.time()

        with open("wordlist.txt") as f:
            wordslist: list[str] = [word.strip() for word in f]
        self.words: list[str] = random.choices(wordslist, k=NUMBER_OF_WORDS)

        self.end: bool = False
        self.time_dict: dict = {}
        self.duration: float = 0

        title_label = tk.Label(self, text="Typing Speed Test", font=("Arial", 20, "bold"))
        title_label.pack(side="top", anchor="center")

        self.word_text = tk.Text(self, font=("Arial", 24, "bold"), bg="grey", height=1)
        self.word_text.insert("1.0", "Press any key to start")
        self.word_text.tag_configure("center", justify='center')
        self.word_text.tag_add("center", 1.0, "end")
        self.word_text.config(state=tk.DISABLED)
        self.word_text.pack(side="top", anchor="center", pady=self.height / 3)

        self.word_words_label = tk.Label(self, text="", font=("Arial", 10))
        self.word_words_label.pack(side="bottom", anchor="center")

        self.seconds_label = tk.Label(self, text="0 sec", font=("Arial", 10))
        self.seconds_label.pack(side="right", anchor="se")

        self.bind("<KeyPress>", self.start_run)

    def start_run(self, event):
        self.unbind("<KeyPress>")
        self.countdown(3)
        self.after(1000, func=lambda: self.countdown(2))
        self.after(2000, func=lambda: self.countdown(1))
        self.after(3000, func=self.start_timer)
        self.after(3000, func=lambda: self.bind("<KeyPress>", self.check_word))
        self.after(3000, func=self.new_word)

    def countdown(self, number):
        self.word_text.config(state=tk.NORMAL)
        self.word_text.delete(1.0, tk.END)
        self.word_text.insert("1.0", str(number))
        self.word_text.tag_configure("center", justify='center')
        self.word_text.tag_add("center", 1.0, "end")
        self.word_text.config(state=tk.DISABLED)

    def new_word(self) -> None:
        end: float = time.time()
        duration = end - self.cur_word_start
        self.time_dict[self.cur_word] = duration
        self.cur_word_start = time.time()

        if not self.cur_i_word > len(self.words) - 1:
            self.cur_word: str = self.words[self.cur_i_word]
            self.count_word()
            self.cur_i_word += 1

            self.cur_i_letter: int = 0

            self.word_text.config(state=tk.NORMAL)
            self.word_text.delete(1.0, tk.END)
            self.word_text.insert("1.0", self.cur_word)
            self.word_text.tag_configure("center", justify='center')
            self.word_text.tag_add("center", 1.0, "end")
            self.word_text.config(state=tk.DISABLED)

            self.tag_word()
        else:
            self.end_of_run()

    def tag_word(self) -> None:
        word = self.word_text.get("1.0", "end")
        for i in range(len(word)):
            self.word_text.tag_configure(str(i), foreground="red")
            self.word_text.tag_add(str(i), f"1.{i}")

    def check_letter(self, event) -> bool:
        if event.char == self.cur_word[self.cur_i_letter]:
            return True
        else:
            return False

    def check_word(self, event) -> None:
        if self.check_letter(event):
            self.make_green()
            self.cur_i_letter += 1
            if self.cur_i_letter > len(self.cur_word) - 1:
                self.new_word()

    def make_green(self) -> None:
        self.word_text.tag_configure(str(self.cur_i_letter), foreground="green")

    def end_of_run(self) -> None:
        self.end: bool = True
        del self.time_dict["word"]
        sheet = StatSheet(self.time_dict, self.duration)
        sheet.mainloop()

    def count_word(self) -> None:
        self.word_words_label.config(text=f"{self.cur_i_word + 1}/{len(self.words)}")

    def start_timer(self):
        self.start: float = time.time()
        self.timer()

    def timer(self) -> None:

        if not self.end:
            self.duration = time.time() - self.start
            self.seconds_label.config(text=f"{self.duration:.2f} sec")
            self.after(10, self.timer)


class StatSheet(tk.Tk):

    def __init__(self, time_dict: dict, duration: float):
        super().__init__()

        self.height: int = 600
        self.width: int = 600
        self.geometry(f"{self.width}x{self.height}")
        self.title("Statsheet")

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.time_dict = time_dict

        title_label = tk.Label(self, text="Your Stats", font=("Arial", 20, "bold"))
        title_label.grid(column=2, row=1)

        row: int = 1

        for item in self.time_dict:
            row += 1

            key_label = tk.Label(self, text=f"{item}", font=("Arial", 14))
            key_label.grid(column=1, row=row)

            value_label = tk.Label(self, text=f"{self.time_dict[item]:.2f} sec", font=("Arial", 14))
            value_label.grid(column=3, row=row)

        sum_label = tk.Label(self, text="Sum", font=("Arial", 14))
        sum_label.grid(column=1, row=(row + 2), pady=20)

        duration_label = tk.Label(self, text=f"{duration:.2f} sec", font=("Arial", 14))
        duration_label.grid(column=3, row=(row + 2))
