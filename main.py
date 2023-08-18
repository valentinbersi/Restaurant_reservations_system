from sys import argv
from reservations import add, modify, delete, list, determine_last_id

COMMAND = 1

ADD_COMMAND_LENGTH = 6
MODIFY_COMMAND_LENGHT = 3
DELETE_COMMAND_LENGHT = 3
LIST_COMMAND_LENGHT_WITHOUT_RANGE = 2
LIST_COMMAND_LENGHT_WITH_RANGE = 4

COMMAND_MIN_LENGHT = 2

NAME_INDEX = 2

MIN_RANGE_INDEX = 2
MAX_RANGE_INDEX = 3

RESERVATION_TO_MODIFY_ID_INDEX = 2
RESERVATION_TO_DELETE_ID_INDEX = 2

ADD = "add"
MODIFY = "modify"
DELETE = "delete"
LIST = "list"

START = "1"

ERROR_OPENING_FILE = "-1"

# Reads the arguments and runs the commands introducted by the user
def run_command(command):
    if command == ADD:
        if len(argv) == ADD_COMMAND_LENGTH:
            new_reservation_info = argv[NAME_INDEX:]
            add(new_reservation_info)
        elif len(argv) < ADD_COMMAND_LENGTH:
            print("Not enought arguments for command 'add'")
            print("Remember that the arguments are: name, amount of peope, hour and ubication")
        else:
            print("Too many arguments for command 'add'.")
            print("Remember that the arguments are: name, amount of peope, hour and ubication")
            
    elif command == MODIFY:
        if len(argv) == MODIFY_COMMAND_LENGHT:
            reservation_to_modify_id = argv[RESERVATION_TO_MODIFY_ID_INDEX]
            modify(reservation_to_modify_id)
        elif len(argv) < MODIFY_COMMAND_LENGHT:
            print("Not enought arguments for modify command.")
            print("Remember that the arguments are the id of the reservation you want to modify")
        else:
            print("Too many arguments for modify command.")
            print("Remember that the arguments are the id of the reservation you want to modify")
            
    elif command == DELETE:
        if len(argv) == DELETE_COMMAND_LENGHT:
            reservation_to_delete_id = argv[RESERVATION_TO_DELETE_ID_INDEX]
            delete(reservation_to_delete_id)
        elif len(argv) < DELETE_COMMAND_LENGHT:
            print("Not enought arguments for command 'delete'.")
            print("Remember that the arguments are the id of the reservation you want to delete")
        else:
            print("Too many arguments for command 'delete'.")
            print("Remember that the arguments are the id of the reservation you want to delete")
        
    elif command == LIST:
        if len(argv) == LIST_COMMAND_LENGHT_WITH_RANGE:
            list(argv[MIN_RANGE_INDEX], argv[MAX_RANGE_INDEX])

        elif len(argv) == LIST_COMMAND_LENGHT_WITHOUT_RANGE:
            last_id = str(determine_last_id())
            if last_id != ERROR_OPENING_FILE:
                list(START, last_id)
        elif len(argv) > LIST_COMMAND_LENGHT_WITH_RANGE:
            print("Too many arguments for command 'list'.")
            print("Remember that the arguments are the id range, if you want to list every reservation you can just type 'list'")
        else:
            print("Please write both range limits")
    else:
        print("Invalid command. Commands are 'add', 'modify', 'delete' or 'list'")
        
def main():
    if(len(argv) >= COMMAND_MIN_LENGHT):
        command = argv[COMMAND].lower()
        run_command(command)
    else:
        print("No command has been typed")

if __name__ == "__main__":
    main()
