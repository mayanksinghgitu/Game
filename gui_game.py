import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
import json
import os
import threading

# --- Sound playback (optional, remove if not used) ---
try:
    from playsound import playsound
    SOUND_ENABLED = True
except ImportError:
    SOUND_ENABLED = False
    print("playsound library not found. Sounds will be disabled.")
    print("To enable sounds, run: pip install playsound")

# --- Constants ---
BG_COLOR = "#1e1e2f"
FONT_COLOR = "#f9f9f9"
STATS_FILE = "stats.json"

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.CHOICE_MAP = {"S": 1, "W": -1, "G": 0}
        self.REV_CHOICE_MAP = {1: "Snake", 0: "Gun", -1: "Water"}
        self.WINNING_COMBOS = {(1, -1), (-1, 0), (0, 1)}

        self.sounds = {
            "click": "sounds/click.wav",
            "win": "sounds/win.wav",
            "loss": "sounds/loss.wav"
        }

        self._load_stats()
        self._setup_ui()
        self.reset_game()

        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _play_sound(self, sound_name):
        if not SOUND_ENABLED:
            return
        try:
            threading.Thread(target=playsound, args=(self.sounds[sound_name],), daemon=True).start()
        except Exception as e:
            pass

    def _load_stats(self):
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r") as f:
                    self.all_time_stats = json.load(f)
            except (json.JSONDecodeError, IOError):
                 self.all_time_stats = {"Player_Wins": 0, "CPU_Wins": 0}
        else:
            self.all_time_stats = {"Player_Wins": 0, "CPU_Wins": 0}

    def _save_stats(self):
        try:
            with open(STATS_FILE, "w") as f:
                json.dump(self.all_time_stats, f, indent=4)
        except IOError:
            pass

    def _on_closing(self):
        self._save_stats()
        self.destroy()

    def _setup_ui(self):
        self.title("Snake Water Gun Game")
        self.geometry("500x800")
        self.config(bg=BG_COLOR)
        self.resizable(False, False)

        self.all_time_stats_label = tk.Label(self, text="", font=("Helvetica", 12), fg="#bdc3c7", bg=BG_COLOR)
        self.all_time_stats_label.pack(pady=(10,0))
        self.update_all_time_stats_label()

        self.match_score_label = tk.Label(self, text="", font=("Helvetica", 20, "bold"), fg="#f1c40f", bg=BG_COLOR)
        self.match_score_label.pack(pady=(5, 0))

        self.result_label = tk.Label(self, text="Choose your weapon!", font=("Helvetica", 14), fg=FONT_COLOR, bg=BG_COLOR)
        self.result_label.pack(pady=10)

        self.choice_label = tk.Label(self, text="", font=("Helvetica", 14), fg="#dcdcdc", bg=BG_COLOR)
        self.choice_label.pack(pady=10)

        self.round_label = tk.Label(self, text="", font=("Helvetica", 14), fg="#f1c40f", bg=BG_COLOR)
        self.round_label.pack(pady=10)

        self.button_canvas = tk.Canvas(self, width=450, height=200, bg=BG_COLOR, highlightthickness=0)
        self.button_canvas.pack()

        self._create_round_button(self.button_canvas, 80, 100, 50, "Snake", "#8e44ad", lambda: self.play("S"))
        self._create_round_button(self.button_canvas, 225, 100, 50, "Water", "#16a085", lambda: self.play("W"))
        self._create_round_button(self.button_canvas, 370, 100, 50, "Gun", "#c0392b", lambda: self.play("G"))

        log_frame = tk.Frame(self, bg=BG_COLOR)
        log_frame.pack(pady=10, padx=20, fill="x")
        log_label = tk.Label(log_frame, text="Game Log", font=("Helvetica", 12, "bold"), fg=FONT_COLOR, bg=BG_COLOR)
        log_label.pack()
        self.game_log = scrolledtext.ScrolledText(log_frame, height=5, width=50, bg="#2c3e50", fg="white", state="disabled")
        self.game_log.pack()

        developer_label = tk.Label(self, text="Developed by Mayank Singh", font=("Helvetica", 12, "bold"), fg="#bdc3c7", bg=BG_COLOR)
        developer_label.pack(side="bottom", pady=10)

    def add_to_log(self, message):
        self.game_log.config(state="normal")
        self.game_log.insert(tk.END, message + "\n")
        self.game_log.config(state="disabled")
        self.game_log.see(tk.END)

    def play(self, user_choice_str):
        self._play_sound("click")
        self._set_buttons_state("disabled")
        user_choice_num = self.CHOICE_MAP[user_choice_str]
        self.result_label.config(text="Computer is choosing...")
        self.choice_label.config(text="")
        self._animate_cpu_choice(15, user_choice_num)

    def _animate_cpu_choice(self, counter, user_choice):
        if counter > 0:
            temp_choice = random.choice([-1, 0, 1])
            self.choice_label.config(text=f"Computer: {self.REV_CHOICE_MAP[temp_choice]}")
            self.after(75, lambda: self._animate_cpu_choice(counter - 1, user_choice))
        else:
            self.show_result(user_choice)

    def show_result(self, user_choice):
        self.current_round += 1
        computer_choice = random.choice([-1, 0, 1])
        
        user_str = self.REV_CHOICE_MAP[user_choice]
        cpu_str = self.REV_CHOICE_MAP[computer_choice]
        
        self.choice_label.config(text=f"You: {user_str} | Computer: {cpu_str}")
        log_msg = f"Round {self.current_round}: You ({user_str}) vs CPU ({cpu_str}). "

        if user_choice == computer_choice:
            self.result_label.config(text="This Round is a DRAW!", fg="#3498db")
            log_msg += "Result: Draw."
        elif (user_choice, computer_choice) in self.WINNING_COMBOS:
            self.result_label.config(text="You WIN this Round!", fg="#2ecc71")
            self.match_score["Player"] += 1
            self._play_sound("win")
            log_msg += "Result: You Win!"
        else:
            self.result_label.config(text="You LOSE this Round!", fg="#e74c3c")
            self.match_score["CPU"] += 1
            self._play_sound("loss")
            log_msg += "Result: You Lose!"
        
        self.add_to_log(log_msg)
        self.update_score_labels()

        if self.match_score["Player"] == 3 or self.match_score["CPU"] == 3:
            self.game_over()
        else:
            self._set_buttons_state("normal")

    def update_all_time_stats_label(self):
        stats = self.all_time_stats
        self.all_time_stats_label.config(text=f"All-Time Record: Player {stats['Player_Wins']} - {stats['CPU_Wins']} CPU")

    def game_over(self):
        is_player_winner = self.match_score["Player"] == 3
        winner = "Player" if is_player_winner else "CPU"

        if is_player_winner:
            self.all_time_stats["Player_Wins"] += 1
        else:
            self.all_time_stats["CPU_Wins"] += 1
        self.update_all_time_stats_label()
        self._save_stats()

        answer = messagebox.askyesno("GAME OVER", f"{winner} wins the match!\n\nDo you want to play again?")
        if answer:
            self.reset_game()
        else:
            self._on_closing()

    def reset_game(self):
        self.match_score = {"Player": 0, "CPU": 0}
        self.current_round = 0
        self.update_score_labels()
        self.result_label.config(text="New Match! Best of 5.", fg=FONT_COLOR)
        self.choice_label.config(text="First to 3 wins.")
        
        self.game_log.config(state="normal")
        self.game_log.delete('1.0', tk.END)
        self.game_log.config(state="disabled")
        
        self.add_to_log("New match started. Good luck!")
        self._set_buttons_state("normal")
    
    def update_score_labels(self):
        self.match_score_label.config(text=f"Player: {self.match_score['Player']} | CPU: {self.match_score['CPU']}")
        self.round_label.config(text=f"Round {self.current_round} / 5")

    def _set_buttons_state(self, state):
        self.button_canvas.itemconfig("all", state=state)

    def _create_round_button(self, canvas, x, y, r, text, color, cmd):
        circle = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline="white", width=3)
        label = canvas.create_text(x, y, text=text, fill="white", font=("Helvetica", 12, "bold"))
        def on_hover(event): canvas.itemconfig(circle, fill="#555", outline="#f1c40f")
        def on_leave(event): canvas.itemconfig(circle, fill=color, outline="white")
        for item in (circle, label):
            canvas.tag_bind(item, "<Button-1>", lambda e: cmd())
            canvas.tag_bind(item, "<Enter>", on_hover)
            canvas.tag_bind(item, "<Leave>", on_leave)

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
