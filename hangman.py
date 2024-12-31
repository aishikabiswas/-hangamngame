import random
import tkinter as tk
from tkinter import messagebox

# Word list for the game
WORD_LIST = ["python", "programming", "hangman", "challenge", "function","keygen"]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Colorful Hangman Game")
        self.root.geometry("500x650")
        self.root.config(bg="#ADD8E6")  # Light blue background

        # Game variables
        self.word = random.choice(WORD_LIST)
        self.word_display = ["_"] * len(self.word)
        self.guessed_letters = set()
        self.attempts_left = 6

        # Title
        self.label_title = tk.Label(root, text="🎨 Hangman Game 🎨", font=("Helvetica", 32, "bold"), bg="#ADD8E6", fg="#003366")
        self.label_title.pack(pady=20)

        # Word display
        self.label_word = tk.Label(root, text=" ".join(self.word_display), font=("Courier", 28, "bold"), bg="#ADD8E6", fg="#FFFFFF")
        self.label_word.pack(pady=20)

        # Status display
        self.label_status = tk.Label(root, text=f"Attempts Left: {self.attempts_left}", font=("Helvetica", 16), bg="#ADD8E6", fg="#FFD700")
        self.label_status.pack(pady=10)

        # Input and button
        self.entry_guess = tk.Entry(root, font=("Helvetica", 18), justify="center", width=3, bg="#FFFFFF", fg="#003366")
        self.entry_guess.pack(pady=10)

        self.button_guess = tk.Button(root, text="Guess", command=self.check_guess, font=("Helvetica", 16), bg="#FF4500", fg="#FFFFFF", activebackground="#FF6347", activeforeground="#FFFFFF", relief="flat")
        self.button_guess.pack(pady=20)

        # Hangman Canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg="#FFFFFF", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Draw the initial hangman scaffold
        self.draw_hangman()

    def draw_hangman(self):
        """Draws the hangman based on remaining attempts."""
        self.canvas.delete("all")
        # Scaffold
        self.canvas.create_line(50, 350, 350, 350, fill="#8B4513", width=4)  # Base
        self.canvas.create_line(100, 50, 100, 350, fill="#8B4513", width=4)  # Pole
        self.canvas.create_line(100, 50, 250, 50, fill="#8B4513", width=4)   # Top bar
        self.canvas.create_line(250, 50, 250, 100, fill="#8B4513", width=4)  # Rope

        # Hangman parts
        parts = [
            lambda: self.canvas.create_oval(225, 100, 275, 150, outline="#FF0000", width=3, fill="#FFB6C1"),  # Head
            lambda: self.canvas.create_line(250, 150, 250, 250, fill="#FF0000", width=3),                     # Body
            lambda: self.canvas.create_line(250, 180, 220, 220, fill="#FF0000", width=3),                     # Left arm
            lambda: self.canvas.create_line(250, 180, 280, 220, fill="#FF0000", width=3),                     # Right arm
            lambda: self.canvas.create_line(250, 250, 220, 300, fill="#FF0000", width=3),                     # Left leg
            lambda: self.canvas.create_line(250, 250, 280, 300, fill="#FF0000", width=3),                     # Right leg
        ]

        for i in range(6 - self.attempts_left):
            parts[i]()

    def check_guess(self):
        """Validates and processes the player's guess."""
        guess = self.entry_guess.get().lower()
        self.entry_guess.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single alphabetic character.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'.")
            return

        self.guessed_letters.add(guess)

        if guess in self.word:
            for i, letter in enumerate(self.word):
                if letter == guess:
                    self.word_display[i] = guess
            self.label_word.config(text=" ".join(self.word_display))

            if "_" not in self.word_display:
                messagebox.showinfo("You Win!", "Congratulations! You guessed the word!")
                self.reset_game()
        else:
            self.attempts_left -= 1
            self.label_status.config(text=f"Attempts Left: {self.attempts_left}")
            self.draw_hangman()

            if self.attempts_left == 0:
                messagebox.showerror("Game Over", f"You've been hanged! The word was '{self.word}'.")
                self.reset_game()

    def reset_game(self):
        """Resets the game for a new round."""
        self.word = random.choice(WORD_LIST)
        self.word_display = ["_"] * len(self.word)
        self.guessed_letters = set()
        self.attempts_left = 6

        self.label_word.config(text=" ".join(self.word_display))
        self.label_status.config(text=f"Attempts Left: {self.attempts_left}")
        self.draw_hangman()

# Main application
root = tk.Tk()
game = HangmanGame(root)
root.mainloop()
