from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
guess_word = {}

# Importing data
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/words_data.csv")

data = data.to_dict(orient="records")

# Choosing a word and displayig it
def pick_word():
    global guess_word, timer
    window.after_cancel(timer)
    guess_word = random.choice(data)
    f_lang = list(guess_word.keys())[0]
    f_word = guess_word[f_lang]
    canvas.itemconfig(title_text, text=f_lang, fill="black")
    canvas.itemconfig(word_text, text=f_word, fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)

    timer = window.after(3000, func=show_word)

# Showing a translation of a word
def show_word():
    global guess_word
    main_lang = list(guess_word.keys())[1]
    main_word = guess_word[main_lang]
    canvas.itemconfig(title_text, text=main_lang, fill="white")
    canvas.itemconfig(word_text, text=main_word, fill="white")
    canvas.itemconfig(canvas_image, image=card_back_img)

# If know word button is pressed, the word is deleting from the list, updated list is writing to another file
def know_word():
    global guess_word
    new_data = data
    for item in new_data:
        if item == guess_word:
            new_data.remove(item)
    df = pandas.DataFrame(new_data)
    df.to_csv("data/words_to_learn.csv", index=False)

    pick_word()



# UI
window = Tk()
window.title("Flashy - Learn words by flash cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
title_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 34, "italic"))
word_text = canvas.create_text(400, 265, text="word", font=("Ariel", 46, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(window, image=cross_image, highlightthickness=0, borderwidth=0, command=pick_word)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
know_button = Button(window, image=check_image, highlightthickness=0, borderwidth=0, command=know_word)
know_button.grid(row=1, column=1)

#Start the app logic
timer = window.after(3000, func=show_word)
pick_word()

window.mainloop()