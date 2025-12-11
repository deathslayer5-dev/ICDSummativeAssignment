import time

# Structured menu broken down by categories (foods, drinks, soups)
items = [
    #Foods
    {
        "Food" : -1,
        "Baguette" : 0.99,
        "Croissant" : 1.25,
        "Grilled Cheese" : 3.5,
        "Beans on Toast" : 0.99,
        "Toast" : 0.99,
        "French Bread" : 1.25,
        "Pain au Chocolat" : 2,
        "6x Chocolate chip cookie" : 3.5,
        "Loaf of Sourdough" : 8,
        #Rmove this
        "Egg Sandwich" : 2,
        "Vincent's Eggs" : 2

    },
    #Drinks
    {
        "Drinks" : -1,
        "Tea": 0.25,
        "Hot Water": 0.12,
        "Black Coffee" : 1,
        "Mint Tea" : 1.25
    },
    #Soup
    {
        "Soup" : -1,
        "French Onion Soup" : 21,
        "Mushroom Soup" : 6.7,
        "Chicken Soup" : 3,
        "Egg Soup" : 2.00

    }
]
restaurantName = "Baguette Cuisine"
order = {}
# margin is used to keep text-based layouts aligned in terminal output
margin = 30


def format_menu_line(index: int, name: str, price: float) -> str:
    """Return a neatly formatted menu line with consistent padding."""
    padding = max(margin - (len(str(index)) + 3 + len(name)), 0)
    return f"\t#{index} \033[4m{name}\033[0m {' ' * padding}${price:.2f}"


def format_order_line(index: int, name: str, qty: int, price: float) -> str:
    """Return formatted text for items shown in the order summary/receipt."""
    item_total = price * qty
    left = f"\t#{index} \033[4m{name}\033[0m"
    qty_text = f"Qty: {qty}"
    padding = max(margin - len(left) - len(qty_text), 0)
    return f"{left} {' ' * padding}{qty_text}{' ' * (margin - len(qty_text))}${item_total:.2f}"


def format_receipt_line(index: int, name: str, qty: int, price: float) -> str:
    """Return the formatted line used exclusively for the receipt view."""
    total_price = price * qty
    item_label = f"#{index}\t\033[4m{name}\033[0m"
    padding = max(margin - len(item_label), 0)
    return f"{item_label} {' ' * padding}${price:.2f}   Qty: {qty}   ${total_price:.2f}"


def get_numeric_choice(prompt: str, min_value: int, max_value: int) -> int:
    """Prompt until the user supplies a valid integer within the given range."""
    while True:
        user_input = input(prompt)
        try:
            choice = int(user_input)
        except ValueError:
            print("Please enter a valid number")
            continue
        if choice < min_value or choice > max_value:
            print("Please enter a value within range")
            continue
        return choice


def menu():
    """Display menu categories with formatted pricing."""
    print(f"\nWelcome to \033[1m\033[4m{restaurantName}\033[0m!")
    # Walk through each category dictionary and display the items
    print("Here is your menu.\n")
    for item in items:
        name = [k for k, v in item.items() if v == -1]
        name = name[0]
        print(f"\033[1m{name}\033[0m(")
        index = 0
        for content in item:
            if index != 0:
                print(format_menu_line(index, content, item[content]))
            index += 1
        print(")")
def ordering():
    """Handle taking orders from the user with menu and validation controls."""
    menu()
    global order
    print("Order by typing a index key along with the category, you could also type out the full name of the item you would like to order")
    while True:
        print("Press \033[4mQ\033[0m to quit")
        print("Press \033[4mM\033[0m to see menu")
        print("Press \033[4mO\033[0m to see order")
        # Expect either "index, category" or "full item name" input formats
        userInput = input("What would you like to order? (\033[4mIndex\033[0m, \033[4mCategory\033[0m) or (\033[4mFull name\033[0m)\n").split(", ")
        if userInput[0].upper() == "Q":
            print("Quitting Operation...")
            break
        if userInput[0].upper() == "M":
            print("Opening Menu...")
            menu()
            continue
        if userInput[0].upper() == "O":
            print("Viewing Order...")
            viewOrder()
            continue
        orderNo = 0
        category = ""
        name = False
        if len(userInput) > 1:
            # Normalize category input (capitalize first letter)
            userInput[1] = userInput[1][0].upper() + userInput[1][1:].lower()
            category = userInput[1]
            name =[]
            index = -1
            for item in items:
                index+=1
                temp = [k for k, v in item.items() if v == -1]
                name.extend(temp)
            if category not in name:
                print("\033[4mPlease enter a valid category!\033[0m")
                continue
            try:
                orderNo = int(userInput[0])
            except ValueError:
                # Index must be numeric in this branch
                print("\033[4mPlease enter a valid index!\033[0m")
                continue
            if orderNo >= len(items[index]) or orderNo < 1:
                print("\033[4mPlease enter a valid index in range!\033[0m")
                continue
        elif len(userInput) == 1:
            # Convert free text into title case to match menu entries
            list = userInput[0].split(" ")
            for i in range (len(list)):
                list[i] = list[i][0].upper()+list[i][1:].lower()
            userInput[0] = ""
            for item in list:
                userInput[0] += item + " "
            userInput[0] = userInput[0][:-1]

            name = True
            # Build a flattened list of all item names for validation
            allItems =[]
            for item in items:
                temp = [k for k, v in item.items() if v != -1]
                allItems.extend(temp)
            if userInput[0] not in allItems:
                print("\033[4mPlease enter a valid item!\033[0m")
                continue
        else:
            # Any other format is considered invalid
            print("\033[4mPlease enter a valid input!\033[0m")
        if name == True:
            order[userInput[0]] = order.get(userInput[0],0)+1
            print(f"{userInput[0]} has been added to your order")
        else:
            for item in items:
                # Locate the requested category dictionary and map index -> item name
                if item.get(userInput[1]) is not None:
                    index = 0
                    name ="a"
                    for it in item:
                        if index == orderNo:
                            name = it
                            break
                        index+=1
                    order[name] = order.get(name,0)+1
                    print(f"{name} has been added to your order")
                    break
def viewOrder():
    """Display the current order with quantities and running total."""
    global order
    index = 1
    print("\nHere is your order: ")
    total = 0
    for key in order:
        for item in items:
            # Match the ordered item name back to its price
            if item.get(key) is not None:
                print(format_order_line(index, key, order[key], item[key]))
                total +=item[key]*order[key]
                break
        index+=1
    print(f"Total before tax: ${total}")
    print("End of Order\n")
def editOrder():
    """Allow the user to adjust the quantity of items already in the order."""
    global order, key
    viewOrder()
    print("Press \033[4mQ\033[0m to quit")
    while True:

        userInput = input(f"What would you like to change (1-{len(order)}, Qty)(ex1: 1, -2)(ex2: 1, 2)? ").split(", ")
        if userInput[0].upper() == "Q":
            print("Quitting Operation...")
            break
        index = -1
        qty = 0
        try:
            index = int(userInput[0])
            qty = int(userInput[1])
        except ValueError:
            print("\033[4mPlease enter a valid index or quantity!\033[0m")
            continue
        if qty == 0 or (index > len(order) or index < 1):
            print("\033[4mPlease enter a valid index or quantity!\033[0m")
            continue
        # Iterate through the ordered keys based on their displayed index
        curr = 1
        for key in order:
            if curr == index:
                order[key] += qty
                break
            curr +=1
        if order[key] <= 0:
            # Remove entries when quantity drops to zero or below
            del order[key]
        viewOrder()
tip = -1
total = 0
def showReceipt():
    """Print detailed receipt with subtotal, taxes, tips and totals."""
    global restaurantName
    print(f"\n\033[1m\033[4m{restaurantName}\033[0m")
    print('-'*47)
    print(f"#   Name{' '*16}Price{' ' * 3}Qty{' ' * 5} Total")
    print('-' * 47)
    global total
    total = 0
    index =1
    for key in order:
        for item in items:
            # Find the matching price for each ordered item and display receipt row
            if item.get(key) is not None:
                print(format_receipt_line(index, key, order[key], item[key]))
                total += item[key] * order[key]
                break
        index += 1
    if index == 1:
        print("Nothing in order")
    print('-' * 47)
    print(f"Sub-Total: {' '*30}${total:.2f}")
    print(f"Tax(HST @ 13%): {' ' * 25}${0.13*total:.2f}")
    global tip
    if tip > -1:
        padding = (31 if tip == 0 else 30)
        print(f"Tips({tip}%): {' ' * padding}${(tip/100)*total:.2f}")
        print(f"Final Total: {' ' * 28}${(tip/100)*total + 1.13 * total:.2f}")
    else:
        print(f"Final Total: {' '*28}${1.13*total:.2f}")
    print('-' * 47)

    print("Thank You for coming to Baguette Cuisine\n")
def pay():
    """Process payment workflow including tips, method selection and card validation."""
    showReceipt()
    global tip
    global total
    while True:
        userInput = get_numeric_choice("Choose a tip you would like to pay ([1] 10%) ([2] 15%) ([3] 20%) ([4] 0%): ", 1, 4)
        match userInput:
            case 1:
                tip = 10
                break
            case 2:
                tip = 15
                break
            case 3:
                tip = 18
                break
            case 4:
                tip = 0
                break
    showReceipt()
    while True:
        method = get_numeric_choice("Will you be paying with cash or credit card ([1] Cash) ([2] Credit Card): ", 1, 2)
        if method == 1:
            # Simple cash flow: validate amount covers totals before giving change
            amount = input("How much cash will you be paying: ")
            try:
                amount = int(amount)
            except ValueError:
                print("Please give valid number")
                continue
            if amount < total:
                print("Please give more than or equal to total cost")
                continue
            print(f"Your change is ${amount-((tip/100)*total + 1.13 * total):.2f}")
            break
        elif method == 2:
            company = input("Are you using Visa, Mastercard or American Express (1. Visa) (2. Mastercard) (3. American Express): ")
            # Basic mock validation for card workflow
            try:
                company = int(company)
            except ValueError:
                print("Please give valid number")
                continue
            if company <1 or company > 3:
                print("Please give valid number in range")
                continue
            cardNum = input("Please give a valid card number: ").replace(" ", "").replace("-","")
            if not(cardNum.isdigit()):
                print("Please give a valid card number")
                continue
            if len(cardNum) >19 or len(cardNum) <13:
                print("Please give a valid card number")
                continue
            pin = input("Insert PIN: ")
            if len(pin) > 4 or len(pin) < 4:
                print("Please give a valid PIN")
                continue
            break
    global restaurantName
    print("Your payment was successful")
    print(f"Thank You for coming to \033[1m\033[4m{restaurantName}\033[0m\n")
    exit(1)
            
        
def controls():
    """Main command loop allowing the user to navigate the application."""
    print("\033[4mM\033[0m to view menu")
    # Prompt user for a single-letter command and route to the correct function
    print("\033[4mO\033[0m to Order")
    print("\033[4mE\033[0m to Edit Order")
    print("\033[4mV\033[0m to View Order")
    print("\033[4mP\033[0m to Pay")
    print("\033[4mR\033[0m to Preview Order Checkout")
    print("\033[4mQ\033[0m to Quit")
    userInput = input("Please choose an Option: ")
    if 'M' in userInput.upper():
        return menu()
    if 'O' in userInput.upper():
        return ordering()
    if 'E' in userInput.upper():
        return editOrder()
    if 'V' in userInput.upper():
        return viewOrder()
    if 'P' in userInput.upper():
        return pay()
    if 'R' in userInput.upper():
        return showReceipt()
    if 'Q' in userInput.upper():
        print(f"Thank You for coming to \033[1m\033[4m{restaurantName}\033[0m\n")
        exit(0)
    return None

while True:
    controls()