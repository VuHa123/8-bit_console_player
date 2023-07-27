import tkinter as tk
from tkinter import messagebox

def start_game(game_name):
    try:
        module = __import__('games.' + game_name, fromlist=['main'])
        module.main()
    except ImportError:
        messagebox.showerror("Error", f"Game {game_name} not found.")

def choose_game():
    root = tk.Tk()
    root.title("Game Selection")

    label = tk.Label(root, text="Select the game you want to play:", font=("Arial", 18))
    label.pack(pady=10)

    games = [
        ("Flappy Bird", "flappy_bird", "#e57373"),
        ("Snake", "snake", "#81c784"),
        ("Pong", "pong", "#ffcc80"),
        ("Tetris", "tetris", "#f48fb1")
        ("Pac-man", "pac_man", "#64b5f6"),

    ]

    button_font = ("Arial", 14)

    for game_title, game_name, button_color in games:
        button = tk.Button(root, text=game_title, font=button_font, bg=button_color, fg="white",
                           activebackground=button_color, activeforeground="white",
                           width=20, height=2, command=lambda name=game_name: start_game(name))
        button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    choose_game()
