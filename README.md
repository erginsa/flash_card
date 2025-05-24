# 🧠 Flashcard Language Learning App (Tkinter)

This is a desktop-based flashcard app built using Python and Tkinter. It helps you learn common phrases between different language pairs using timed flashcards. The app supports progress saving, undo, and reset features.

---

## 🚀 Features

- Choose between multiple language pairs (e.g. Spanish-English, English-Turkish)
- Front/back flashcard flip after 3 seconds
- Track learning progress in a CSV file
- Undo and Reset functionality
- Clean and responsive UI

---

## 📂 Folder Structure
````bash
project
│   main.py
│   README.md
│
├───data
│       spanish_english.csv
│       english_turkish.csv
│       to_learn_spanish_english.csv
│       to_learn_english_turkish.csv
│
├───images
│       card_front.png
│       card_back.png
│       right.png
│       wrong.png
````

---

---

## 🧪 How to Run

```bash
    python main.py
```

You must have pandas installed. If not, install it via:

```bash
    pip install pandas
```

---

## 🌍 Add Your Own Language Pair

To add a new language pair (e.g., French - German):

1. Create a new CSV file inside the data/ folder. It should follow this format:
```python-repl
French,German
Bonjour,Hello
Merci,Thanks
...
```

2. Add a new PATH constant at the top of main.py:
```python
FRENCH_GERMAN_PATH = "data/french_german.csv"
TO_LEARN_FRENCH_GERMAN_PATH = "data/to_learn_french_german.csv"
```

3. Update the set_language() function with a new elif block:
```python
elif choice == "French - German":
    SELECTED_CSV_PATH = FRENCH_GERMAN_PATH
    TO_LEARN_PATH = TO_LEARN_FRENCH_GERMAN_PATH
    SOURCE_COLUMN = "French"
    TARGET_COLUMN = "German"
```

4. Add a new button inside lang_select() for the new language pair.

That's it! You're good to go!

---

## 📌 Dependencies
- Python 3.7+

- pandas

- tkinter (built-in with Python)

---

## 📄 License
MIT License – free to use and modify.

---

## 🙌 Credits
Built with love using Python and Tkinter
Made by ERGIN SABANCI ✨

