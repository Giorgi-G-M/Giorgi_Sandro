import requests

#This fucntion is to take data of currencyes.
def get_data():
    url = f"https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/ka/json/?date=2024-03-31"
    response = requests.get(url)
    data = response.json()
    return data

#this function collects all curencies in list
def get_currencies():
    currencie_list = ["GEL"]
    for a in get_data()[0]["currencies"]:
        currencie_list.append(a["code"])
    return currencie_list

#this function collects all currency rates in list
def get_rate():
    rate_list = []
    for b in get_data()[0]["currencies"]:
        temp = {}
        temp[b["code"]] = b["rate"]
        rate_list.append(temp)
    return rate_list

#this function takes user inputs
def input_taker():
    money = input("Enter the currency you want to exchange and enter the currency in which you want to exchange: ")
    money = money.strip()
    return money

#this is main function where happen currency exchange.
def main_currency(money):
    while True:
        rate_getter = get_rate()

        user_input_actions_list = []

        for i in money:
            if i == "-":
                user_input_actions_list.append(i)

        number_of_item = len(user_input_actions_list)
        if number_of_item == 1:
            first_currency, second_currency = money.split("-")
            if first_currency in get_currencies() and second_currency in get_currencies():
                try:
                    amount_of_money = float(input(f"Enter the amount of money what you want to exchange: "))
                    if first_currency != "GEL" and second_currency != "GEL":
                        for c in rate_getter:
                            if first_currency == list(c.items())[0][0]:
                                exchanged_money_in_gel = amount_of_money * list(c.items())[0][1]
                                for d in rate_getter:
                                    if second_currency == list(d.items())[0][0]:
                                        exchanged_money_in_second_currency = exchanged_money_in_gel / list(d.items())[0][1]
                                        print(f"{first_currency} in {second_currency} = {exchanged_money_in_second_currency:.2f}")


                    else:
                        for e in rate_getter:
                            if first_currency == list(e.items())[0][0]:
                                exchanged_money_in_gel = amount_of_money * list(e.items())[0][1]
                            elif second_currency == list(e.items())[0][0]:
                                exchanged_money_in_gel = amount_of_money / list(e.items())[0][1]
                        print(f"{first_currency} in {second_currency} = {exchanged_money_in_gel:.2f}")

                except ValueError:
                    print("Invalid input.")
                    continue
            else:
                print("You entered invalid cuurency")
                continue

        another_try = input("You want to try again? YES/NO ").lower()
        if another_try == "yes":
            pass
        else:
            print("the proggram is over")
            break

if __name__ == "__main__":
    main_currency(input_taker())