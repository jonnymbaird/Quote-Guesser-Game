import requests
from bs4 import BeautifulSoup
from random import choice
from csv import DictReader

BASE_URL = "http://quotes.toscrape.com/"


def read_quotes(filename):
    with open(filename, "r", encoding='utf-8') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)


def start_game(quotes):
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here is a quote: ")
    print(quote["text"])
    guess = ''
    while guess.lower() != quote["author"].lower() and remaining_guesses > 0:
        guess = input(f"Who wrote this quote? Guesses remainging: {remaining_guesses}\n")
        if guess.lower() == quote["author"].lower():
            print("You got it right!")
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(f"{BASE_URL}{quote['bio-link']}")
            soup = BeautifulSoup(res.text, "html.parser")
            birth_date = soup.find(class_="author-born-date").get_text()
            birth_location = soup.find(
                class_="author-born-location").get_text()
            print(f"Here is a hint: The author was born on {birth_date} {birth_location}")
        elif remaining_guesses == 2:
            print(f"Here is a hint: The author's name starts with {quote['author'][0]}")
        elif remaining_guesses == 1:
            last_initial = quote['author'].split(" ")[-1][0]
            print(f"Here is a hint: The author's last name starts with {last_initial }")
        else:
            print(f"Sorry you ran out of guesses. The author was: {quote['author']}")
    again = ''
    while again.lower() not in ("y", "yes", "n", "no"):
        again = input("Would you like to play again (y/n)?\n")
    if again.lower() in ("y", "yes"):
        return start_game(quotes)
    else:
        print("OK, Goodbye!")


quotes = read_quotes("quotes_data.csv")
start_game(quotes)
