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
    if (first_n == 0 or second_n == 0) or (first_n == 0 and second_n == 0):
        return "It's imposible to devide by zero."
    return int(first_n) / int(second_n)

#This function tryes to catch problem if there is any.
def main_calculator(operation):
    operation = operation.strip()

    number_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    symbol_list = ["+", "-", "*", "/"]
    user_input_actions_list = []

    for i in operation:
        if i in symbol_list:
            user_input_actions_list.append(i)

    number_of_item = len(user_input_actions_list)

    if number_of_item == 1:
        if "+" in operation:
            x,y = operation.split("+")
            print(f"{x} + {y} = {round(plus(x,y))}")

        elif "-" in operation:
            x,y = operation.split("-")
            print(f"{x} + {y} = {round(minus(x,y))}")

        elif "/" in operation:
            x,y = operation.split("/")
            print(f"{x} + {y} = {round(devide(x,y))}")

        elif "*" in operation:
            x,y = operation.split("*")
            print(f"{x} + {y} = {round(multiplicate(x,y))}")

        else:
            print("Invalid input.")
    else:
        print("Ivalid input")

if __name__ == "__main__":
    main_calculator(numbers())

