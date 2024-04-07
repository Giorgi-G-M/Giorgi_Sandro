def numbers():
    user_input = input("Enter the numbers: ")
    return user_input

#The next four function is for math actions.
def plus(first_n, second_n):
    return int(first_n) + int(second_n)

def minus(first_n, second_n):
    return int(first_n) - int(second_n)

def multiplicate(first_n, second_n):
    return int(first_n) * int(second_n)

def devide(first_n, second_n):
    if int(first_n) == 0 or int(second_n) == 0:
       raise ZeroDivisionError
    else:
        return int(first_n) / int(second_n)
def square_root(number):
    result = round(float(number) ** 0.5, 2)
    return f"\u221A{number} = {result}"

#This function tries to catch problems if there are any, if not, it prints the real output.
def main_calculator(operation):
    operation = operation.strip()

    symbol_list = ["+", "-", "*", "/", "s"]
    user_input_actions_list = []

    for i in operation:
        if i in symbol_list:
            user_input_actions_list.append(i)

    number_of_item = len(user_input_actions_list)

    if number_of_item == 1:
        if "+" in operation:
            x,y = operation.split("+")
            print(f"{x} + {y} = {round(plus(x,y),2)}")

        elif "-" in operation:
            x,y = operation.split("-")
            print(f"{x} - {y} = {round(minus(x,y),2)}")

        elif "*" in operation:
            x,y = operation.split("*")
            print(f"{x} * {y} = {round(multiplicate(x,y),2)}")

        elif "/" in operation:
            x,y = operation.split("/")
            try:
                print(f"{x} / {y} = {round(devide(x,y),2)}")
            except ZeroDivisionError:
                print("It's impossible to divide by zero.")

        elif "s" in operation:
            if operation.startswith("s"):
                if operation[1:].isdigit():
                    print(square_root(operation[1:]))

        else:
            print("Invalid input.")
    else:
        print("Invalid input")


if __name__ == "__main__":
    while True:
        main_calculator(numbers())
        again = input("Do you want another calculations? yes/no: ")
        if again.lower() == "y" or again.lower() == "yes":
            pass
        elif again.lower() == "n" or again.lower() == "no":
            print("The proggram calculator was complete. Thank you to use it.")
            break
        else:
            print("Enter 'yes' or 'y' to contniue or enter 'no' or 'n' to end the proggram.")