from tkinter import *
from PIL import Image, ImageTk
import pandas
import random

# ---------------- CONSTANT -----------------------
BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    with open("data/words_to_learn.csv", mode="w") as new_file:
        data = pandas.read_csv("data/japanese_words.csv")
        new_file.write(str(data))

data_dict = data.to_dict(orient="records")
print(data_dict)
current_card = {}

# ----------------- DISPLAY NEXT CARD --------------

def show_next_card():
    global current_card, after_timer
    current_card = random.choice(data_dict)
    canvas.itemconfig(word, text=current_card["Kanji"], fill="black")
    canvas.itemconfig(title, text="Kanji", fill="black")
    canvas.itemconfig(canvas_image, image=card_front_image)
    after_timer = window.after(3000, flip_card)

def flip_card():

    canvas.itemconfig(word, text=current_card["English"], fill="white")
    canvas.itemconfig(title, text="Translation", fill="white")
    canvas.itemconfig(canvas_image, image=card_back_image)

# ----------- WORDS TO LEARN FOR NEXT USE ----------

def know_the_word():
    data_dict.remove(current_card)
    show_next_card()
    data = pandas.DataFrame(data_dict)
    data.to_csv(path_or_buf="data/words_to_learn.csv", index=False)

# ----------------- UI SET-UP ---------------------


window = Tk()
window.title("Flash Cards Portfolio")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
after_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_image = ImageTk.PhotoImage(Image.open("images/Small-Square-Card-Blank-Spring-Green.png"))
card_back_image = ImageTk.PhotoImage(Image.open("images/Large-Square-Card-Blank-Dark-Green.png"))
canvas_image = canvas.create_image(400, 263, image=card_front_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Arial", 52, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

cancel_image= ImageTk.PhotoImage(Image.open("images/wrong.png"))
cancel_button = Button(image=cancel_image, highlightthickness=0, command=show_next_card)
cancel_button.grid(row=1, column=0)

ok_image= ImageTk.PhotoImage(Image.open("images/right.png"))
ok_button = Button(image=ok_image, highlightthickness=0, command=know_the_word)
ok_button.grid(row=1, column=1)

show_next_card()



window.mainloop()