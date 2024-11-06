import sql
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import random
import string


class Lingo:
    def __init__(self, master):
        self.master = master
        self.mode = 1
        self.word_to_guess: str
        self.input_string = ""
        self.create_widgets()

    def create_widgets(self):
        # Play button
        self.play_button = tk.Button(self.master, text="Play", font=("Arial", 24), command=self.play_game)
        self.play_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Settings button
        self.settings_button = tk.Button(self.master, text="⚙️", font=("Arial", 12), command=self.open_settings_menu)
        self.settings_button.place(relx=0.95, rely=0.05, anchor=tk.NE)

    def check_letter(self, letter):
        if len(self.input_string) < 5:  # Assume the word length is 5
            self.input_string += letter
            self.display_input_string()
            self.highlight_key(letter)

    def play_game(self):
        self.play_button.place_forget()
        self.word_to_guess = random.choice(self.get_words_from_database())
        self.remaining_attempts = 5
        self.tip = sql.get_tips_from_database(self.word_to_guess)

        if self.remaining_attempts == 2:
            self.tip_label = tk.Label(self.master, text="Tip: " + self.tip, font=("Arial", 12), bg="white")
            self.tip_label.place(relx=0.8, rely=0.1, anchor=tk.NE)

        keyboard_frame = tk.Frame(self.master)
        keyboard_frame.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        self.input_string = ""
        self.display_input_string()

        self.alphabet_buttons = []
        row = 0
        col = 0
        for letter in "QWERTYUIOPASDFGHJKLZXCVBNM":  # creating screen keyboard
            button = tk.Button(keyboard_frame, text=letter, font=("Arial", 12), width=3, height=2,
                               command=lambda l=letter: self.check_letter(l))
            button.grid(row=row, column=col, padx=5, pady=5)
            self.alphabet_buttons.append(button)
            col += 1
            if (col == 10 and row == 0) or (col == 9 and row == 1):
                col = 0
                row += 1
                if row == 3:
                    break

        enter_button = tk.Button(keyboard_frame, text="Enter", font=("Arial", 12), width=3, height=2,
                                 command=self.check_guess)
        enter_button.grid(row=row, column=col, padx=5, pady=5)
        self.alphabet_buttons.append(enter_button)

        backspace_button = tk.Button(keyboard_frame, text="⌫", font=("Arial", 12), width=3, height=2,
                                     command=self.handle_backspace)
        backspace_button.grid(row=row, column=col+1, padx=5, pady=5)
        self.alphabet_buttons.append(backspace_button)

        for button in self.alphabet_buttons:
            button.grid(in_=keyboard_frame)

        self.master.bind('<KeyPress>', self.handle_key_press)

    def open_settings_menu(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("300x400")

        scrollbar = tk.Scrollbar(settings_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        word_listbox = tk.Listbox(settings_window, yscrollcommand=scrollbar.set, font=("Arial", 12))
        word_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=word_listbox.yview)

        words = self.get_words_from_database()

        for word in words:
            word_listbox.insert(tk.END, word)

    def get_words_from_database(self):  # getting all words feom databases from other file
        words = sql.get_words_from_database()
        return words

    def display_input_string(self):  # showing entering word above the keyboard
        if hasattr(self, "input_string_label"):
            self.input_string_label.destroy()
        self.input_string_label = tk.Label(self.master, text=self.input_string, font=("Arial", 12))
        self.input_string_label.place(relx=0.5, rely=0.59, anchor=tk.CENTER)

    def handle_key_press(self, event):  # showing entering word after typing
        key = event.char.uqwpper()
        if key in string.ascii_uppercase:
            if len(self.input_string) < 5:
                self.input_string += key
            self.highlight_key(key)  # Highlight the corresponding key on the on-screen keyboard
        elif key == '\x08':  # Backspace key
            self.input_string = self.input_string[:-1]
            self.highlight_backspace()  # Highlight the backspace key on the on-screen keyboard
        elif key == '\r':  # Enter key
            self.check_guess()
        self.display_input_string()

    def highlight_key(self, key):  # highlighting screen keyboard after typing
        for button in self.alphabet_buttons:
            if button['text'] == key:
                button.config(bg='gray')
            elif button['text'] != 'Enter' and button['text'] != '⌫':
                button.config(bg='SystemButtonFace')

    def highlight_backspace(self):
        for button in self.alphabet_buttons:
            if button['text'] == '⌫':
                button.config(bg='green')
            elif button['text'] != 'Enter':
                button.config(bg='SystemButtonFace')

    def check_guess(self):  # checkong words after Enter
        self.remaining_attempts -= 1
        guess_label = tk.Label(self.master, text=self.input_string, font=("Arial", 24))
        guess_label.place(relx=0.5, rely=(5-self.remaining_attempts)*0.1, anchor=tk.CENTER)

        if self.input_string == self.word_to_guess.upper():
            messagebox.showinfo("Congratulations", "You guessed the word!")
            self.play_game()  # Start a new game
            return

        if self.remaining_attempts == 0:
            messagebox.showinfo("Game Over", f"The word was: {self.word_to_guess}")
            self.play_game()  # Start a new game
            return

        colored_text = ""
        for i in range(len(self.input_string)):
            if self.input_string[i] == self.word_to_guess.upper()[i]:
                colored_text += self.input_string[i]
            elif self.input_string[i] in self.word_to_guess.upper():
                colored_text += "*"
            else:
                colored_text += "-"

        guess_label.configure(text=colored_text)
        self.input_string = ""
        self.display_input_string()

    def handle_backspace(self):  # changing input_word after Backspace button
        self.input_string = self.input_string[:-1]
        self.display_input_string()
        self.highlight_backspace()


root = tk.Tk()
root.title("Lingo(best version ever)")
root.geometry("720x480")
app = Lingo(root)
root.bind("<Key>", app.handle_key_press)
root.mainloop()