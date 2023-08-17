from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"
vocab = {}

try:
    language_df = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    starting_data = pd.read_csv("data/french_words.csv")
    to_learn = starting_data.to_dict("records")
else:
    to_learn = language_df.to_dict("records")


def next_card():
    global vocab, flip_timer
    window.after_cancel(flip_timer)
    vocab = random.choice(to_learn)
    print(vocab)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfigure(title_text, text="French", fill="black")
    canvas.itemconfigure(vocab_text, text=vocab.get("French"), fill="black")
    flip_timer = window.after(3000, card_flip)


def card_flip():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(vocab_text, text=vocab.get("English"), fill="white")

def word_learned():
    global vocab
    to_learn.remove(vocab)
    learn_df = pd.DataFrame.from_dict(to_learn)
    learn_df.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.title("Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=card_flip)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="", font=(FONT_NAME, 40, "italic"))
vocab_text = canvas.create_text(400, 263, text="", font=(FONT_NAME, 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# language_label = Label(text="Language", bg="white", font=(FONT_NAME, 40, "italic"))
# language_label.place(x=280, y=150)
#
# vocab_label = Label(text="Word", bg="white", font=(FONT_NAME, 60, "bold"))
# vocab_label.place(x=280, y=263)

wrong = PhotoImage(file="./images/wrong.png")
right = PhotoImage(file="./images/right.png")

x_button = Button(image=wrong, bd=0, highlightthickness=0, command=next_card)
x_button.grid(column=0, row=1)

check_button = Button(image=right, bd=0, highlightthickness=0, command=word_learned)

check_button.grid(column=1, row=1)

next_card()

window.mainloop()