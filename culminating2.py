import random
import sys

cards = {"2": 4, "3": 4, "4":4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "Jack": 4, "Queen": 4, "King": 4, "Ace": 4}
value = 0
cards_left = 52
score = 0

#questions:
questions = {
    "Which ancient civilization is credited with building the famed city of Machu Picchu?": [
        "The Inca",
        "The Aztecs",
        "The Maya",
        "The Olmecs"
    ],
    "In what year did the Berlin Wall officially fall, symbolizing the end of the Cold War division in Europe?": [
        "1989",
        "1987",
        "1991",
        "1985"
    ],
    "Who was the monarch of England during the Spanish Armada's attempted invasion in 1588?": [
        "Queen Elizabeth I",
        "Queen Victoria",
        "King Henry VIII",
        "Queen Mary I"
    ],
    "The 'Mandate of Heaven' was a philosophical concept central to the governance of which ancient civilization?": [
        "Ancient China",
        "Mesopotamia",
        "Ancient Egypt",
        "The Gupta Empire"
    ],
    "Which 19th-century nurse became famous for her work during the Crimean War and founded modern nursing?": [
        "Florence Nightingale",
        "Clara Barton",
        "Mary Seacole",
        "Dorothea Dix"
    ],
    "The series of 1950s-60s protests and acts of civil disobedience against racial segregation in the U.S. is known as what?": [
        "The Civil Rights Movement",
        "The Suffrage Movement",
        "The Abolitionist Movement",
        "The Progressive Movement"
    ],
    "Which of these empires was NOT a major participant in the 'Triple Entente' at the start of World War I?": [
        "The Ottoman Empire",
        "The British Empire",
        "The French Republic",
        "The Russian Empire"
    ],
    "Which explorer is generally credited with leading the first expedition to circumnavigate the globe?": [
        "Ferdinand Magellan",
        "Christopher Columbus",
        "Vasco da Gama",
        "Amerigo Vespucci"
    ],
    "What was the primary writing system of ancient Egypt called?": [
        "Hieroglyphics",
        "Cuneiform",
        "Sanskrit",
        "Linear B"
    ],
    "The ancient city of Troy, site of the legendary Trojan War, is located in modern-day which country?": [
        "Turkey",
        "Greece",
        "Italy",
        "Egypt"
    ]
}

def startUp():
    print("Welcome to \033[4mBlack Jack Style History Trivia\033[0m")
    print("This game is Black Jack with a twist, the twist being, \033[2mIf you answer it right, you get to affect your value of your card by 1\033[0m. Try Your best\n")
def actualGameplay():
    global value
    print(f"You currently have {value} value, try and keep your score as close to 21 without busting.")
    choice = input("[1] Hit | [2] Stand\n")
    choice = choice.lower()
    global index
    if index >= len(questions):
        global score
        stand()
        print(f"Your final score was {score}")
        sys.exit(1)

    if choice == "1" or choice == "hit":
        hit()
        return
    elif choice == "2" or choice == "stand":
        stand()
        return
    else:
        print("\033[91mInvalid Choice\033[0m")
        actualGameplay()
        return
def hit():
    global value
    global cards_left
    index = random.randint(0, len(cards))
    currind = 0
    card = ""
    for key, val in cards.items():
        if currind == index:
            card = key
            val -= 1
            cards_left-=1
            break
        if val > 0:
            currind += 1
    if card.isdigit():
        card = int(card)
        print(f"You got a {card}")
    elif card == "Ace":
        while True:
            print(f"You got a {card}")
            print(f"What value do you want the Ace to have: ")
            Ace = input("[1] 1 | [2] 11\n")
            if Ace == "1":
                card = 1
                break
            elif Ace == "2":
                card = 11
                break
            else:
                print("\033[91mInvalid Choice\033[0m")
                continue
    else:
        print(f"You got a {card}")
        card = 10
    card = change(card)
    print(f"Your final value is {card}")
    value += card
    if value > 21:
        print("You \033[4bBUSTED\033[0m")
        sys.exit(-1)
    else:
        print(f"Your current Value is \033[4b{value}\033[0m")
    if cards_left <= 52*0.25:
        reshuffle()
    return
index = 0
def change(card: int):
    global index
    ind = 0
    res = card
    for question, answers in questions.items():
        if(ind == index):
            print(f"\n{question}")

            shuffled_answers = answers.copy()
            random.shuffle(shuffled_answers)

            correct_answer = answers[0]
            correctInd = 0
            for i, answer in enumerate(shuffled_answers, 1):
                if(answer == correct_answer):
                    correctInd = i
                print(f"  {i}. {answer}")
            UserAns = input("Choose the index of the correct answer: ")
            if(int(UserAns) == correctInd):
                UserInp = input("You got it RIGHT, would you like to increase, decrease or keep your value? (i/d/k)")
                if UserInp.lower().__contains__("i"):
                    res+=1
                elif UserInp.lower().__contains__("d"):
                    res-=1
                elif UserInp.lower().__contains__("k"):
                    res = res
            else:
                print(f"You were WRONG, the correct answer was {correct_answer}, the value is kept\n")
        ind+=1
    index+=1
    return res


def stand():
    global value
    global score
    print(f"You ended with {value}, adding it to your score.")
    score += value
    print(f"Your current score is {score}\n")

def reshuffle():
    for key, val in cards:
        val = 4
startUp()
while(True):
    actualGameplay()