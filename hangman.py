import tkinter as tk
from tkinter import messagebox
import math


class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#2E2E2E")

        self.expression = ""
        self.memory = 0
        self.input_var = tk.StringVar()

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        entry = tk.Entry(self.root, textvariable=self.input_var, font=('Arial', 24), bd=10, insertwidth=2, width=14, borderwidth=4, justify='right', bg="#FFFFFF")
        entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

        # Frame for buttons
        button_frame = tk.Frame(self.root, bg="#2E2E2E")
        button_frame.grid(row=1, column=0, columnspan=5)

        # Button layout
        buttons = [
            '7', '8', '9', '/', 'sqrt',
            '4', '5', '6', '*', 'pow',
            '1', '2', '3', '-', 'log',
            '0', '.', '=', '+', 'sin',
            'cos', 'tan', '(', ')', 'C',
            'M+', 'MR', 'MC', '!', '%'
        ]

        row_val = 0
        col_val = 0

        for button in buttons:
            btn = tk.Button(button_frame, text=button, padx=20, pady=20, font=('Arial', 18), command=lambda b=button: self.on_button_click(b), bg="#4CAF50", fg="#FFFFFF", activebackground="#45A049")
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=5, pady=5)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1

        for i in range(5):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)

    def bind_keys(self):
        self.root.bind('<Key>', self.key_press)

    def key_press(self, event):
        key = event.char
        if key in '0123456789+-*/.()':
            self.on_button_click(key)
        elif key == 'Enter':
            self.on_button_click('=')
        elif key == '\x08': 
            self.on_button_click('C')

    def on_button_click(self, char):
        if char == '=':
            try:
                self.expression = self.evaluate_expression(self.expression)
                self.input_var.set(self.expression)
                self.expression = ""  
            except Exception as e:
                messagebox.showerror("Error", "Invalid Input")
                self.clear()
        elif char == 'C':
            self.clear()
        elif char == 'M+':
            try:
                self.memory += float(self.input_var.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid Input for Memory")
        elif char == 'MR':
            self.input_var.set(self.memory)
        elif char == 'MC':
            self.memory = 0
        elif char == '!':
            try:
                num = int(self.input_var.get())
                self.expression = str(math.factorial(num))
                self.input_var.set(self.expression)
            except Exception as e:
                messagebox.showerror("Error", "Invalid Input for Factorial")
                self.clear()
        elif char == '%':
            try:
                self.expression = str(float(self.input_var.get()) / 100)
                self.input_var.set(self.expression)
            except ValueError:
                messagebox.showerror("Error", "Invalid Input for Percentage")
                self.clear()
        else:
            self.expression += str(char)
            self.input_var.set(self.expression)

    def evaluate_expression(self, expr):
        expr = expr.replace('sqrt', 'math.sqrt')
        expr = expr.replace('pow', '**')
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace('sin', 'math.sin(math.radians')
        expr = expr.replace('cos', 'math.cos(math.radians')
        expr = expr.replace('tan', 'math.tan(math.radians')

        # Add closing parentheses for trigonometric functions
        expr = self.add_closing_parentheses(expr)

        return str(eval(expr))

    def add_closing_parentheses(self, expr):
        count = expr.count('math.sin(math.radians') + expr.count('math.cos(math.radians') + expr.count('math.tan(math.radians')
        expr += ')' * count  # Append required closing parentheses
        return expr

    def clear(self):
        self.expression = ""
        self.input_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    calculator = ScientificCalculator(root)
    root.mainloop()
