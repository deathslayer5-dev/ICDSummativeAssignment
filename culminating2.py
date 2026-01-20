"""Blackjack-Style History Trivia Game

This code blends a simplified blackjack experience with a multiple-choice
history quiz. Players draw cards to build their hand toward 21 without busting.
For every card draw, they must answer a trivia question; a correct answer gives
an opportunity to adjust the card's numeric value by ±1 before it is applied.

"""

import random
import sys
from typing import Dict, List, Tuple

# ---------------------------------------------------------------------------
# Configuration constants
# ---------------------------------------------------------------------------
# Number of copies for each card face in a standard 52-card deck. We store this
# separately so that rebuilding the deck is as simple as duplicating these
# values and shuffling them.
CARD_TEMPLATE: Dict[str, int] = {
    "2": 4,
    "3": 4,
    "4": 4,
    "5": 4,
    "6": 4,
    "7": 4,
    "8": 4,
    "9": 4,
    "10": 4,
    "Jack": 4,
    "Queen": 4,
    "King": 4,
    "Ace": 4,
}

# Blackjack values for non-ace cards. Aces are handled separately because they
# can represent either 1 or 11 depending on the player's choice.
CARD_VALUE_LOOKUP: Dict[str, int] = {
    **{str(n): n for n in range(2, 11)},
    "Jack": 10,
    "Queen": 10,
    "King": 10,
}

# How low the deck is allowed to get (as a percentage of the original size)
# before an automatic reshuffle occurs.
LOW_DECK_THRESHOLD = 0.25

# ANSI color helpers to keep console output readable yet vibrant.
class Style:
    HEADER = "\033[95m"
    INFO = "\033[94m"
    SUCCESS = "\033[92m"
    WARNING = "\033[93m"
    ERROR = "\033[91m"
    UNDERLINE = "\033[4m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


# ---------------------------------------------------------------------------
# Trivia question bank – correct answer is always the first entry. We shuffle
# the order before presenting choices so the index changes every time.
# ---------------------------------------------------------------------------
QUESTIONS: Dict[str, List[str]] = {
    "Which ancient civilization is credited with building the famed city of Machu Picchu?": [
        "The Inca",
        "The Aztecs",
        "The Maya",
        "The Olmecs",
    ],
    "In what year did the Berlin Wall officially fall, symbolizing the end of the Cold War division in Europe?": [
        "1989",
        "1987",
        "1991",
        "1985",
    ],
    "Who was the monarch of England during the Spanish Armada's attempted invasion in 1588?": [
        "Queen Elizabeth I",
        "Queen Victoria",
        "King Henry VIII",
        "Queen Mary I",
    ],
    "The 'Mandate of Heaven' was a philosophical concept central to the governance of which ancient civilization?": [
        "Ancient China",
        "Mesopotamia",
        "Ancient Egypt",
        "The Gupta Empire",
    ],
    "Which 19th-century nurse became famous for her work during the Crimean War and founded modern nursing?": [
        "Florence Nightingale",
        "Clara Barton",
        "Mary Seacole",
        "Dorothea Dix",
    ],
    "The series of 1950s-60s protests and acts of civil disobedience against racial segregation in the U.S. is known as what?": [
        "The Civil Rights Movement",
        "The Suffrage Movement",
        "The Abolitionist Movement",
        "The Progressive Movement",
    ],
    "Which of these empires was NOT a major participant in the 'Triple Entente' at the start of World War I?": [
        "The Ottoman Empire",
        "The British Empire",
        "The French Republic",
        "The Russian Empire",
    ],
    "Which explorer is generally credited with leading the first expedition to circumnavigate the globe?": [
        "Ferdinand Magellan",
        "Christopher Columbus",
        "Vasco da Gama",
        "Amerigo Vespucci",
    ],
    "What was the primary writing system of ancient Egypt called?": [
        "Hieroglyphics",
        "Cuneiform",
        "Sanskrit",
        "Linear B",
    ],
    "The ancient city of Troy, site of the legendary Trojan War, is located in modern-day which country?": [
        "Turkey",
        "Greece",
        "Italy",
        "Egypt",
    ],
}


# ---------------------------------------------------------------------------
# Mutable game state (globals kept minimal and well-documented)
# ---------------------------------------------------------------------------
deck: List[str] = []
value: int = 0
score: int = 0
turns: int = 1
cards_left: int = sum(CARD_TEMPLATE.values())
question_order: List[str] = list(QUESTIONS.keys())
random.shuffle(question_order)
question_index: int = 0


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------
def banner(text: str, color: str = Style.HEADER) -> None:
    """Prints a stylized banner with surrounding separators."""

    separator = f"{color}{'-' * max(len(text) + 4, 30)}{Style.RESET}"
    print(separator)
    print(f"{color}| {text.center(len(text) + 2)} |{Style.RESET}")
    print(separator)


def prompt(message: str) -> str:
    """Wrapper around input() that trims whitespace for consistent handling."""

    try:
        return input(message).strip()
    except EOFError:
        # If the input stream is closed (e.g., Ctrl+D), exit gracefully.
        print(f"\n{Style.ERROR}Input stream closed. Exiting the game...{Style.RESET}")
        sys.exit(0)


# ---------------------------------------------------------------------------
# Deck management
# ---------------------------------------------------------------------------
def build_deck() -> None:
    """Builds a full 52-card deck and shuffles it in place."""

    global deck, cards_left
    deck = [card for card, count in CARD_TEMPLATE.items() for _ in range(count)]
    random.shuffle(deck)
    cards_left = len(deck)


def ensure_deck() -> None:
    """Checks deck size and rebuilds when either empty or below threshold."""

    global deck
    total_cards = sum(CARD_TEMPLATE.values())
    if not deck:
        print(f"{Style.WARNING}Deck is empty. Reshuffling...{Style.RESET}")
        build_deck()
    elif len(deck) <= total_cards * LOW_DECK_THRESHOLD:
        print(f"{Style.WARNING}Low on cards ({len(deck)} left). Reshuffling for fairness.{Style.RESET}")
        build_deck()


def draw_card() -> str:
    """Pops one card from the deck after ensuring it is available."""

    ensure_deck()
    card = deck.pop()
    global cards_left
    cards_left -= 1
    return card


# ---------------------------------------------------------------------------
# Trivia handling
# ---------------------------------------------------------------------------
def get_next_question() -> Tuple[str, List[str]]:
    """Cycles through questions in a shuffled order, reshuffling when exhausted."""

    global question_index
    if question_index >= len(question_order):
        random.shuffle(question_order)
        question_index = 0
    key = question_order[question_index]
    question_index += 1
    return key, QUESTIONS[key]


def ask_trivia(card_value: int) -> int:
    """Asks a trivia question and optionally adjusts the provided card value."""

    question, answers = get_next_question()

    print(f"\n{Style.UNDERLINE}{question}{Style.RESET}")
    shuffled_answers = answers.copy()
    random.shuffle(shuffled_answers)

    correct_answer = answers[0]
    correct_index = shuffled_answers.index(correct_answer) + 1

    for idx, answer in enumerate(shuffled_answers, start=1):
        print(f"  {idx}. {answer}")

    while True:
        response = prompt(f"Choose the index of the correct answer (1-{len(shuffled_answers)}): ")
        if not response.isdigit():
            print(f"{Style.ERROR}Please enter a number.{Style.RESET}")
            continue

        chosen_index = int(response)
        if not 1 <= chosen_index <= len(shuffled_answers):
            print(f"{Style.ERROR}Choice out of range. Try again.{Style.RESET}")
            continue

        if chosen_index == correct_index:
            print(f"{Style.SUCCESS}Correct! You may tweak the card's value by 1.{Style.RESET}")
            return adjust_card_value(card_value)
        else:
            print(f"{Style.ERROR}Incorrect. The correct answer was '{correct_answer}'. Value unchanged.{Style.RESET}")
            return card_value


def adjust_card_value(card_value: int) -> int:
    """Allows the player to increase, decrease, or keep the drawn card's value."""

    print(
        f"Current card value: {Style.BOLD}{card_value}{Style.RESET}. "
        "Enter 'i' to increase by 1, 'd' to decrease by 1, or 'k' to keep it."
    )

    while True:
        choice = prompt("(i/d/k): ").lower()
        if choice.startswith("i"):
            return card_value + 1
        if choice.startswith("d"):
            # Guard against reducing below 1, which would make no sense for blackjack.
            return max(1, card_value - 1)
        if choice.startswith("k"):
            return card_value
        print(f"{Style.ERROR}Invalid choice. Please enter i, d, or k.{Style.RESET}")


# ---------------------------------------------------------------------------
# Card value handling
# ---------------------------------------------------------------------------
def resolve_card_value(card_name: str) -> int:
    """Translates a drawn card's face into a numerical Blackjack value."""

    if card_name == "Ace":
        while True:
            print(
                f"You drew an {Style.BOLD}Ace{Style.RESET}. "
                "Would you like it to count as 1 or 11?"
            )
            ace_choice = prompt("[1] → 1 | [2] → 11: ")
            if ace_choice == "1":
                return 1
            if ace_choice == "2":
                return 11
            print(f"{Style.ERROR}Invalid choice. Please select 1 or 2.{Style.RESET}")

    # Numbered cards are stored as strings; convert when possible.
    if card_name.isdigit():
        return int(card_name)

    # Face cards default to 10, handled via lookup.
    return CARD_VALUE_LOOKUP[card_name]


# ---------------------------------------------------------------------------
# Gameplay functions
# ---------------------------------------------------------------------------
def start_up() -> None:
    """Displays the welcome banner and explains the rules."""

    banner("Black Jack Style History Trivia")
    print(
        f"This game plays like simplified blackjack, but with a twist!\n"
        f"Answer a history question for each card draw. If you're right, you can "
        f"{Style.DIM}adjust the card's value by ±1 before it applies to your hand{Style.RESET}.\n"
        f"Try to keep your hand as close to 21 as possible without busting.\n"
    )


def display_status() -> None:
    """Provides the player with their current status in the game."""

    print(
        f"Current hand value: {Style.BOLD}{value}{Style.RESET} | "
        f"Cumulative score: {Style.BOLD}{score}{Style.RESET} | "
        f"Cards remaining in deck: {cards_left} | "
        f"Current turn in deck: {turns}"
    )


def actual_gameplay() -> None:
    """Handles the player's decision to hit or stand for the current round."""
    global score
    global turns
    display_status()

    if score >= 100:
        print(f"{Style.SUCCESS}{Style.BOLD}{Style.UNDERLINE}YOU WIN{Style.RESET}")

    print("Choose your next move:")
    print("  [1] Hit  → Draw another card")
    print("  [2] Stand → Bank your current hand into the total score")

    turns+=1

    while True:
        choice = prompt("Selection: ").lower()
        if choice in {"1", "hit", "h"}:
            handle_hit()
            return
        if choice in {"2", "stand", "s"}:
            handle_stand()
            return
        print(f"{Style.ERROR}Invalid choice. Type 1/Hit or 2/Stand.{Style.RESET}")


def handle_hit() -> None:
    """Executes the logic for drawing a card, answering trivia, and updating the hand."""

    global value

    card = draw_card()
    print(f"\nYou drew: {Style.INFO}{card}{Style.RESET}")
    card_value = resolve_card_value(card)
    card_value = ask_trivia(card_value)

    value += card_value
    print(f"Adjusted card value applied: {Style.SUCCESS}{card_value}{Style.RESET}")

    if value > 21:
        print(f"{Style.ERROR}{Style.UNDERLINE}BUST!{Style.RESET} Your hand exceeded 21.")
        print(f"Final cumulative score: {Style.BOLD}{score}{Style.RESET}")
        sys.exit(0)
    elif value == 21:
        print(f"{Style.ERROR}{Style.UNDERLINE}21!{Style.RESET} YOU HIT 21")
        handle_stand()
    else:
        print(f"Your updated hand value is {Style.BOLD}{value}{Style.RESET}. Keep going!\n")


def handle_stand() -> None:
    """Banks the player's current hand into the cumulative score and resets the hand."""

    global value, score
    print(
        f"Standing with {Style.BOLD}{value}{Style.RESET}. "
        "Adding it to your cumulative score."
    )
    score += value
    value = 0
    print(f"Your new cumulative score: {Style.BOLD}{score}{Style.RESET}\n")


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
def main() -> None:
    """Entrypoint for the game."""

    build_deck()
    start_up()

    # Keep the game running indefinitely until the user quits (Ctrl+C/D) or busts.
    while True:
        try:
            actual_gameplay()
        except KeyboardInterrupt:
            print(f"\n{Style.WARNING}Game interrupted by user. Goodbye!{Style.RESET}")
            sys.exit(0)


if __name__ == "__main__":
    main()
