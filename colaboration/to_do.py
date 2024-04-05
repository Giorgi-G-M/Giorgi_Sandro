def main_to_do():
    user_data = get_user_input()
    write_data(user_data)
    task_content()

    while True:
        current_data = get_data()
        if len(current_data) == 0:
            print("Exiting. Tasks saved.")
            break
        close = input("Enter task number to remove, or press 'C' to add another task, or press 'ENTER' to exit: ")

        if not close:
            task_content()
            print("Exiting. Tasks saved.")
            break
        elif close.isdigit():
            if int(close) <= len(current_data):
                remove_data(int(close))
                task_content()
        elif close.lower() == "c":
            change = input("Enter the task: ")
            if change:
                change_data(change)
                task_content()

# This function is to change data in the txt file
def change_data(data):
    with open("task.txt", "a") as file:
        file.write(data + "\n")

# This function writes things what user want to do
def write_data(data):
    with open("task.txt", "w") as file:
        for item in data:
            file.write(item + "\n")

# This function asks the user if they want to add more tasks.
def get_user_input():
    user_list = []
    while True:
        user_task = input("Enter a task or press ENTER to finish: ").strip()
        if user_task:
            user_list.append(user_task)
        else:
            return user_list

# This function reads file and gets data
def get_data():
    with open("task.txt", "r") as file:
        data = file.readlines()
    return [item.strip() for item in data if item.strip()]  # Ensure no empty lines are returned

# This function enumerates "to do" things.
def task_content():
    data = get_data()
    print("Your tasks:")
    for i, j in enumerate(data, start=1):
        print(f"{i}. {j}")

# With this function, the user can remove their goal.
def remove_data(id):
    data = get_data()
    if id <= len(data):
        del data[id - 1]  # Adjusting index since user input starts from 1
        write_data(data)

if __name__ == "__main__":
    main_to_do()
