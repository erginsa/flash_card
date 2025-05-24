from tkinter import *
from tkinter import messagebox
import random
import pandas as pd
from pandas.errors import EmptyDataError
import os


# ---------------------------- CONSTANTS ---------------------------- #
BACKGROUND_COLOR = "#95b6c6"

# CSV file paths for different language pairs
SPANISH_ENGLISH_PATH = "data/spanish_english.csv"
ENGLISH_TURKISH_PATH = "data/english_turkish.csv"
TO_LEARN_SPANISH_ENGLISH_PATH = "data/to_learn_spanish_english.csv"
TO_LEARN_ENGLISH_TURKISH_PATH = "data/to_learn_english_turkish.csv"

# These will be dynamically set based on user's language choice
SELECTED_CSV_PATH = ""
TO_LEARN_PATH = ""
SOURCE_COLUMN = ""
TARGET_COLUMN = ""

# Globals for current sentence, remaining cards, undo history, and timer
current_sentence = {}
all_sentences = {}
undo_stack = []
timer = None


# Initialize main window (hidden at first to avoid early appearance)
window = Tk()
window.overrideredirect(True)   # Disable window decorations temporarily
window.withdraw()               # Hide the window while language selection is active
window.title("Loading...")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.resizable(False, False)


# ---------------------------- ALL FUNCTIONS ---------------------------- #
def set_language():
    """
    Ask the user to choose a language pair and set global variables accordingly.
    """
    global SELECTED_CSV_PATH, TO_LEARN_PATH, SOURCE_COLUMN, TARGET_COLUMN

    choice = lang_select()

    if choice == "Spanish - English":
        SELECTED_CSV_PATH = SPANISH_ENGLISH_PATH
        TO_LEARN_PATH = TO_LEARN_SPANISH_ENGLISH_PATH
        SOURCE_COLUMN = "Spanish"
        TARGET_COLUMN = "English"
    elif choice == "English - Turkish":
        SELECTED_CSV_PATH = ENGLISH_TURKISH_PATH
        TO_LEARN_PATH = TO_LEARN_ENGLISH_TURKISH_PATH
        SOURCE_COLUMN = "English"
        TARGET_COLUMN = "Turkish"
    else:
        messagebox.showerror("Error", "No language selected. Exiting.")
        exit()


def lang_select():
    """
    Display a modal popup for user to choose the language pair.
    """
    result = {"choice": None}

    def choose(label):
        result["choice"] = label
        lang_window.destroy()   # Block interaction with the main window


    lang_window = Toplevel()
    lang_window.title("Select Language")
    lang_window.geometry("300x150+600+400")
    lang_window.grab_set()

    lang_choice_label = Label(lang_window, text="Choose a language to learn: ", font=("Arial", 15))
    lang_choice_label.grid(row=0, column=0, pady=10, padx=35)

    lang_choice_button1 = Button(lang_window, text="Spanish - English", width=25, command=lambda: choose("Spanish - English"))
    lang_choice_button1.grid(row=1, column=0, padx=35)

    lang_choice_button2 = Button(lang_window, text="English - Turkish", width=25, command=lambda: choose("English - Turkish"))
    lang_choice_button2.grid(row=2, column=0, padx=35)

    lang_window.wait_window()   # Wait here until the selection window is closed

    return result["choice"]


# Set language selection, then show the main window
set_language()
window.deiconify()
window.overrideredirect(False)

try:
    data = pd.read_csv(TO_LEARN_PATH)
except (FileNotFoundError, EmptyDataError):
    data = pd.read_csv(SELECTED_CSV_PATH)

# Convert data to list of dictionaries
all_sentences = data.to_dict(orient="records")


def generate_card():
    """
    Select a random card and display the front side (source language).
    """
    global current_sentence, timer

    if len(all_sentences) == 0:
        # All cards are learned
        canvas.itemconfig(title, text="Good Job!", fill="black")
        canvas.itemconfig(sentence, text="You learned all sentences!!", fill="black")
        canvas.itemconfig(canvas_background, image=front_image)
        return

    if timer is not None:
        window.after_cancel(timer)

    current_sentence = random.choice(all_sentences)

    canvas.itemconfig(title, text=SOURCE_COLUMN, fill="black")
    canvas.itemconfig(sentence, text=current_sentence[SOURCE_COLUMN], fill="black")
    canvas.itemconfig(canvas_background, image=front_image)

    # Schedule flip to back side after 3 seconds
    timer = window.after(3000, func=flip_card)

    window.title(f"{SOURCE_COLUMN} {TARGET_COLUMN} Common Sentences ({len(all_sentences)} left)")


def flip_card():
    """Flip the card to show the target language side."""
    canvas.itemconfig(title, text=TARGET_COLUMN, fill="white")
    canvas.itemconfig(sentence, text=current_sentence[TARGET_COLUMN], fill="white")
    canvas.itemconfig(canvas_background, image=back_image)


def right_clicked():
    """Mark card as learned and save progress."""
    undo_stack.append(current_sentence)
    all_sentences.remove(current_sentence)
    generate_card()
    pd.DataFrame(all_sentences).to_csv(TO_LEARN_PATH, index=False)


def wrong_clicked():
    generate_card()


def reset_application():
    """
        Resets the user's progress by deleting the 'to learn' file
    and reloading the original dataset. Shows a confirmation message.
    """
    global all_sentences
    try:
        if os.path.exists(TO_LEARN_PATH):
            os.remove(TO_LEARN_PATH)    # Delete saved progress

        messagebox.showinfo(title="Reset", message="All progress reset")

        # Reload full dataset
        reset_data = pd.read_csv(SELECTED_CSV_PATH)
        all_sentences = reset_data.to_dict(orient="records")
        generate_card()    # Show a new card
    except (FileNotFoundError, EmptyDataError):
        messagebox.showinfo(title="Reset", message="All progress has already been reset.")


def undo_clicked():
    """
        Restores the most recently removed card using the undo stack.
    Re-adds it to the list and updates the progress file.
    """
    if undo_stack:
        restored_card = undo_stack.pop()
        all_sentences.append(restored_card)

        # Save updated progress
        pd.DataFrame(all_sentences).to_csv(TO_LEARN_PATH, index=False)

        generate_card()    # Show next card
        messagebox.showinfo("Undo", "Last card has been restored.")
    else:
        messagebox.showwarning("Undo", "Nothing to undo.")



# ---------------------------- UI SETUP ---------------------------- #
# Load card images
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")

# Create canvas for flashcard
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_background = canvas.create_image(400, 263, image=front_image)
canvas.grid(row=0, column=0, columnspan=4)

# Add texts
title = canvas.create_text(400, 150, text="Title", font=("Arial", 50, "italic"))
sentence = canvas.create_text(400, 263, text="Sentence", font=("Arial", 35, "bold"), width=730)


# Add buttons
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=wrong_clicked)
wrong_button.grid(row=1, column=0, pady=5)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image,highlightthickness=0, command=right_clicked)
right_button.grid(row=1, column=3, pady=5)

reset_button = Button(text="Reset", highlightthickness=0, bg="yellow", font=("Arial", 10), command=reset_application)
reset_button.grid(row=2, column=1, pady=10)

undo_button = Button(text="Undo", bg="#e0e0e0", font=("Arial", 10), command=undo_clicked)
undo_button.grid(row=2, column=2)

# Show the first card
generate_card()

# Start the Tkinter event loop
window.mainloop()
