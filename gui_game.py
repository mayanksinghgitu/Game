import tkinter as tk
import random

MYdec = {"S": 1, "W": -1, "G": 0}
REV = {1: "Snake", 0: "Gun", -1: "Water"}

root = tk.Tk()
root.title("Snake Water Gun Game")
root.geometry("500x650")
root.config(bg="#1e1e2f")

score = {"Win": 0, "Loss": 0, "Draw": 0}

result_label = tk.Label(root, text="", font=("Helvetica", 20, "bold"), fg="#f9f9f9", bg="#1e1e2f")
result_label.pack(pady=20)

choice_label = tk.Label(root, text="", font=("Helvetica", 14), fg="#dcdcdc", bg="#1e1e2f")
choice_label.pack(pady=10)

score_label = tk.Label(root, text="Wins: 0 | Losses: 0 | Draws: 0", font=("Helvetica", 14),
                       fg="#f1c40f", bg="#1e1e2f")
score_label.pack(pady=10)

def update_score():
    score_label.config(text=f"Wins: {score['Win']} | Losses: {score['Loss']} | Draws: {score['Draw']}")

def play(user_choice):
    you = MYdec[user_choice]
    result_label.config(text="Computer is thinking...", fg="#f1c40f")
    choice_label.config(text="")
    root.after(1000, lambda: show_result(you))

def show_result(you):
    computer = random.choice([-1, 0, 1])
    choice_text = f"Your Choice: {REV[you]}, Computer Choice: {REV[computer]}"
    choice_label.config(text=choice_text)
    if you == computer:
        result_label.config(text="DRAW !!!", fg="#3498db")
        score["Draw"] += 1
    elif (you == 1 and computer == -1) or \
         (you == -1 and computer == 0) or \
         (you == 0 and computer == 1):
        result_label.config(text="You WIN !!", fg="#2ecc71")
        score["Win"] += 1
        glow_animation(result_label)
    else:
        result_label.config(text="You LOSS !!", fg="#e74c3c")
        score["Loss"] += 1
    update_score()

def glow_animation(label):
    def flash(count=0):
        if count < 6:
            color = "#2ecc71" if count % 2 == 0 else "#1e1e2f"
            label.config(fg=color)
            root.after(150, lambda: flash(count+1))
        else:
            label.config(fg="#2ecc71")
    flash()

def create_round_button(canvas, x, y, r, text, color, cmd):
    circle = canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="white", width=3)
    label = canvas.create_text(x, y, text=text, fill="white", font=("Helvetica", 12, "bold"))

    def hover_on(event):
        canvas.itemconfig(circle, fill="#555", outline="#f1c40f")
    def hover_off(event):
        canvas.itemconfig(circle, fill=color, outline="white")

    canvas.tag_bind(circle, "<Button-1>", lambda e: cmd())
    canvas.tag_bind(label, "<Button-1>", lambda e: cmd())
    canvas.tag_bind(circle, "<Enter>", hover_on)
    canvas.tag_bind(label, "<Enter>", hover_on)
    canvas.tag_bind(circle, "<Leave>", hover_off)
    canvas.tag_bind(label, "<Leave>", hover_off)

canvas = tk.Canvas(root, width=450, height=250, bg="#1e1e2f", highlightthickness=0)
canvas.pack()

create_round_button(canvas, 80, 120, 50, "Snake", "#8e44ad", lambda: play("S"))
create_round_button(canvas, 225, 120, 50, "Water", "#16a085", lambda: play("W"))
create_round_button(canvas, 370, 120, 50, "Gun", "#c0392b", lambda: play("G"))

def reset_scores():
    score["Win"] = 0
    score["Loss"] = 0
    score["Draw"] = 0
    update_score()
    result_label.config(text="", fg="#f9f9f9")
    choice_label.config(text="")

reset_button = tk.Button(root, text="Reset Scores", font=("Helvetica", 12), width=15,
                         bg="#34495e", fg="white", command=reset_scores, relief="ridge")
reset_button.pack(pady=20)

developer_label = tk.Label(root, text="Developed by Mayank Singh",
                           font=("Helvetica", 12, "bold"), fg="#bdc3c7", bg="#1e1e2f")
developer_label.pack(side="bottom", pady=10)

root.mainloop()
