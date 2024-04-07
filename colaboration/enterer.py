from calculator import main_calculator, numbers
from to_do import main_to_do
from money import main_currency
from weather import weather_main
from settings import *
from register import *
from contact import *



def main():
      register_main()
      printer()
      choice = enter_program()
      orderer(choice)


def printer():
      print("Hello, Welcome to our platform this is a program where you can choose a task you need help with:")
      print(f"1. TO DO" +"\n"
            f"2. Calculator" +"\n"
            f"3. Currency exchange" +"\n"
            f"4. Weather forecast" +"\n"
            f"5. contact information" + "\n"
            f"6. settings" + "\n")

def enter_program():
      choice = input("Now choose from 1 to 6 which one you want to use. or just click 'ENTER' to edn program will end: ")
      return choice

def orderer(choice):
      if len(choice) == 1:
            if choice.isdigit():
                  if choice == "1":
                        print("You are in 'TO DO' application")
                        main_to_do()
                        printer()
                        choice = enter_program()
                        orderer(choice)

                  elif choice == "2":
                        print("You are in 'Calculator' application")
                        main_calculator(numbers())
                        printer()
                        choice = enter_program()
                        orderer(choice)

                  elif choice == "3":
                        print("You are in currency 'Currency exchange' application")
                        main_currency()
                        printer()
                        choice = enter_program()
                        orderer(choice)

                  elif choice == "4":
                        print("You are in 'Weather forecast' application")
                        weather_main()
                        printer()
                        choice = enter_program()
                        orderer(choice)

                  elif choice == "5":
                        print("You are in 'contact' application")
                        contact_main()
                        print()
                        choice = enter_program()
                        orderer(choice)

                  elif choice == "6":
                        print("You are in 'settings' application")
                        settings_main()
                        print()
                        choice = enter_program()
                        orderer(choice)

                  elif not choice:
                        print("End proggram.")

                  else:
                        print("Something went wrong in your input.")

if __name__ == "__main__":
      main()
