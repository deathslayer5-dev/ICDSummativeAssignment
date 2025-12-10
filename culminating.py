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
        "6x Chocolate chip cookie" : 3.5
    },
    #Drinks
    {
        "Drinks" : -1,
        "Tea": 0.25,
        "Hot Water": 0.12,
        "Black Coffee" : 1,
        "Mint Tea" : 1.25
    }
]
restaurantName = "Baguette cuisine"
order = {}
margin = 30
def menu():
    print(f"\nWelcome to \033[1m\033[4m{restaurantName}\033[0m!")
    print("Here is your menu.\n")
    for item in items:
        name = [k for k, v in item.items() if v == -1]
        name = name[0]
        print(f"\033[1m{name}\033[0m(")
        index = 0
        for content in item:
            if index != 0:
                print(f"\t#{index} \033[4m{content}\033[0m {" "*(margin-(len(str(index))+3+len(content)))}${f"{item[content]:.2f}"}")
            index += 1
        print(")")
def ordering():
    menu()
    global order
    print("Order by typing a index key along with the category, you could also type out the full name of the item you would like to order")
    while True:
        print("Press \033[4mQ\033[0m to quit")
        print("Press \033[4mM\033[0m to see menu")
        userInput = input("What would you like to order? (\033[4mIndex\033[0m, \033[4mCategory\033[0m) or (\033[4mFull name\033[0m)\n").split(", ")
        if userInput[0].upper() == "Q":
            print("Quitting Operation...")
            break
        if userInput[0].upper() == "M":
            print("Opening Menu...")
            menu()
            continue
        orderNo = 0
        category = ""
        name = False
        if(len(userInput) > 1):
            category = userInput[1]
            name =[]
            for item in items:
                temp = [k for k, v in item.items() if v == -1]
                name.extend(temp)
            if category not in name:
                print("\033[4mPlease enter a valid category!\033[0m")
                continue
            try:
                orderNo = int(userInput[0])
            except ValueError:
                print("\033[4mPlease enter a valid index!\033[0m")
                continue
            if orderNo >= len(items) or orderNo < 1:
                print("\033[4mPlease enter a valid index!\033[0m")
                continue
        elif (len(userInput) == 1):
            name = True
            allItems =[]
            for item in items:
                temp = [k for k, v in item.items() if v != -1]
                allItems.extend(temp)
            if userInput[0] not in allItems:
                print("\033[4mPlease enter a valid item!\033[0m")
                continue
        else:
            print("\033[4mPlease enter a valid input!\033[0m")
        if name == True:
            order[userInput[0]] = order.get(userInput[0],0)+1
            print(f"{userInput[0]} has been added to your order")
        else:
            for item in items:
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
    global order
    index = 1
    print("\nHere is your order: ")
    total = 0
    for key in order:
        for item in items:
            if item.get(key) is not None:
                print(f"\t#{index} \033[4m{key}\033[0m {" " * (margin-10 - (len(str(index)) + 4 + len(key)))}Qty: {order[key]}{" " * (margin+20-len(f"\t#{index} \033[4m{key}\033[0m {" " * (margin-10 - (len(str(index)) + 4 + len(key)))}Qty: {order[key]}"))}${f"{item[key]*order[key]:.2f}"}")
                total +=item[key]*order[key]
                break
        index+=1
    print(f"Total before tax: ${total}")
    print("End of Order\n")
def editOrder():
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
        if qty == 0 or (index >= len(order) or index < 1):
            print("\033[4mPlease enter a valid index or quantity!\033[0m")
            continue
        curr = 1
        for key in order:
            if curr == index:
                order[key] += qty
                break
            curr +=1
        if order[key] == 0:
            del order[key]
tip = -1
def showReceipt():
    global restaurantName
    print(f"\n\033[1m\033[4m{restaurantName}\033[0m")
    print('-'*42)
    total = 0
    index =1
    for key in order:
        for item in items:
            if item.get(key) is not None:
                print(f"\t#{index} \033[4m{key}\033[0m {' ' * (margin - 10 - (len(str(index)) + 4 + len(key)))}${item[key]:.2f} Qty: {order[key]} {' ' * (margin - len(f'\t#{index} \033[4m{key}\033[0m {' ' * (margin - 20 - (len(str(index)) + 4 + len(key)))}${item[key]:.2f} Qty: {order[key]}'))}${item[key] * order[key]:.2f}")
                total += item[key] * order[key]
                break
        index += 1
    if index == 1:
        print("Nothing in order")
    print('-' * 42)
    print(f"Sub-Total: {' '*25}${total:.2f}")
    print(f"Tax(HST @ 13%): {' ' * 20}${0.13*total:.2f}")
    global tip
    if tip > -1:
        print(f"Tips({tip}%): {' ' * 25}${(tip/100)*total:.2f}")
        print(f"Final Total: {' ' * 23}${(tip/100)*total + 1.13 * total:.2f}")
    else:
        print(f"Final Total: {' '*23}${1.13*total:.2f}")
    print('-' * 42)

    print("Thank You for coming to Baguette Cuisine\n")
def pay():
    showReceipt()
    global tip
    global total
    while True:
        userInput = input("Choose a tip you would like to pay (1. 10%) (2. 15%) (3. 20%) (4. 0%): ")
        try:
            userInput = int(userInput)
        except ValueError:
            print("Please give valid number")
            continue
        if userInput < 1 or userInput > 4:
            print("Please give valid number in range")
            continue
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
        method = input("Will you be paying with cash or credit card (1. Cash) (2. Credit Card): ")
        try:
            method = int(method)
        except ValueError:
            print("Please give valid number")
            continue
        if(method < 1 or method > 2):
            print("Please give valid number in range")
            continue
        if(method == 1):
            amount = input("How much cash will you be paying: ")
            try:
                method = int(method)
            except ValueError:
                print("Please give valid number")
                continue
            if amount < total:
                print("Please give more than or equal to total cost")
                continue
            print(f"Your change is ${total-amount:.2f}")
            break
        elif method == 2:
            company = input("Are you using Visa, Mastercard or American Express (1. Visa) (2. Mastercard) (3. American Express): ")
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

    print("Your payment was successful")
    SystemExit(1)
            
        
def controls():
    print("\033[4mM\033[0m to view menu")
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
        return None
    return None
while True:
    controls()