from csv import writer, reader
from os import rename

RESERVATIONS = "reservations.csv"
AUXILIAR = "auxiliar.csv"

APPEND = "a"
READ_ONLY = "r"
WRITE = "w"

DEFAULT_ID = 0

ID_INDEX = 0
NAME_INDEX = 1
PEOPLE_AMOUNT_INDEX = 2
HOUR_INDEX = 3
UBICATION_INDEX = 4

NAME = "name"
PEOPLE_AMOUNT = "amount"
HOUR = "hour"
UBICATION = "ubication"

MIN_PEOPLE = 1

MIN_HOUR = 0
MAX_HOUR = 23
MIN_MINUTE = 0
MAX_MINUTE = 59

OUTSIDE = "O"
INSIDE = "I"

NON_EXISTENT = -1
ERROR_OPENING_FILE = 0

HOUR_MINUTE_DIVISOR = ":"
HOUR_MINUTE_DIVISOR_INDEX = 2

CSV_DELIMITER = ";"

COMMAND = 0
VALUE = 1

CHANGE_LENGTH = 2

ID_EXIST = True
FILE_EXIST = True

# Tells the user that there was an error opening a file
def error_opening(file):
    print(f"Error opening file {file}.\n")
    
    print("Check that the files exist")
    print("File will be created once you add your first reservation")

# Tells the user that there was an error creating a file
def error_creating(file):
    print(f"Error creating/opening {file}")

# Returns the id of the last reservation as a numeric string
def determine_last_id():
    try:
        reservations = open(RESERVATIONS, READ_ONLY)
    except:
        error_opening(RESERVATIONS)
        return NON_EXISTENT
    
    reservations_reader = reader(reservations, delimiter = CSV_DELIMITER)
    
    last_id = DEFAULT_ID
    for reservation in reservations_reader:
        last_id = reservation[ID_INDEX]
    
    return int(last_id)

# Returns true if the amount of people is valid
def valid_people_amount(people_amount):
    return (people_amount.isnumeric() and int(people_amount) >= MIN_PEOPLE)

# Returns true if the hour format is hh:mm
def valid_hour_format(hour):
    return ( (HOUR_MINUTE_DIVISOR in hour and hour.index(HOUR_MINUTE_DIVISOR) == HOUR_MINUTE_DIVISOR_INDEX) and (hour[:hour.index(HOUR_MINUTE_DIVISOR)].isnumeric() and hour[hour.index(HOUR_MINUTE_DIVISOR) + 1:].isnumeric()) )

# Returns True if the hour value and the minute value are valid
def valid_hour_values(hour):
    return ( ( int(hour[:hour.index(HOUR_MINUTE_DIVISOR)]) >= MIN_HOUR and int(hour[:hour.index(HOUR_MINUTE_DIVISOR)]) <= MAX_HOUR ) and ( int(hour[hour.index(":") + 1:]) >= MIN_MINUTE and int(hour[hour.index(":") + 1:]) <= MAX_MINUTE ) )

# Returns true if the hour is between the 00:00 and the 23:59
def valid_hour(hour):
    return valid_hour_format(hour) and valid_hour_values(hour)

# Pre: ubication is a string
# Post: returns true if the ubication is valid (OUTSIDE or INSIDE)
def valid_ubication(ubication):
    return (ubication == OUTSIDE or ubication == INSIDE)

# Returns true if new_reservation_info has valid data
def valid_new_reservation_info(new_reservation_info):
        return valid_people_amount(new_reservation_info[PEOPLE_AMOUNT_INDEX]) and valid_hour(new_reservation_info[HOUR_INDEX]) and valid_ubication(new_reservation_info[UBICATION_INDEX])

# Pre: new_reservation_info is loaded with valid data
# Pos: adds a reservation
def add(new_reservation_info):
    new_reservation_info.insert(ID_INDEX,DEFAULT_ID)
    
    new_reservation_info[UBICATION_INDEX] = new_reservation_info[UBICATION_INDEX].upper()
    
    if not valid_new_reservation_info(new_reservation_info):
        print("\nTyped data is not valid.\n")
        
        print("Check that the amount of people is equal or greater than 0,")
        print("that the hour is in the format hh:mm and between 00:00 and 23:59,")
        print("that the ubication is OUTSIDE (O) or INSIDE (I),")
        print("and that the aguments are in the correct order (name | amount of people | hour | ubication)")
    else:
        try:
            reservations = open(RESERVATIONS,APPEND)
        except:
            error_creating(RESERVATIONS)
            return
        
        new_reservation_info[ID_INDEX] = determine_last_id() + 1
        
        if new_reservation_info[ID_INDEX] != ERROR_OPENING_FILE:
            reservations_writer = writer(reservations, delimiter = CSV_DELIMITER)
            reservations_writer.writerow(new_reservation_info)
            reservations.close()
            print(f"The reservations was succesfully added to the {RESERVATIONS} file")
    
# Pre: reservation_to_modify_id is a numeric string
# Pos: returns true if the searched id exist
def id_exist(reservation_to_modify_id):
    try:
        reservations = open(RESERVATIONS,READ_ONLY)
    except:
        error_opening(RESERVATIONS)
        return not ID_EXIST, not FILE_EXIST
    
    reservations_reader = reader(reservations, delimiter = CSV_DELIMITER)
    
    exist = False
    for reservation in reservations_reader:
        if reservation[ID_INDEX] == reservation_to_modify_id:
            exist = True
            
    reservations.close()
    
    return exist, FILE_EXIST

# Pre: field_to_modify is loaded with NAME, PEOPLE_AMOUNT, HOUR or UBICATION
# Post: returns the index of the field that is going to be modified
def determine_field_to_modify_index(field_to_modify):
    if(field_to_modify == NAME):
        return NAME_INDEX
    elif(field_to_modify == PEOPLE_AMOUNT):
        return PEOPLE_AMOUNT_INDEX
    elif(field_to_modify == HOUR):
        return HOUR_INDEX
    else:
        return UBICATION_INDEX

# Pre: id_reserva_a_modificar es un string numerico cargado con el id de una reserva existente
# Pos: modifica el campo campo_a_modificar de la reserva que tenga por id id_reserva_a_modificar
def modify_field(reservation_to_modify_id, field_to_modify, new_value):
    try:
        reservations = open(RESERVATIONS,READ_ONLY)
    except:
        error_opening(RESERVATIONS)
        return
    
    try:
        auxiliar = open(AUXILIAR,WRITE)
    except:
        reservations.close()
        error_creating(AUXILIAR)
        return
    
    reservations_reader = reader(reservations, delimiter = CSV_DELIMITER)
    auxiliar_writer = writer(auxiliar, delimiter = CSV_DELIMITER)
    
    for reservation in reservations_reader:
        if reservation[ID_INDEX] == reservation_to_modify_id:
            reservation[determine_field_to_modify_index(field_to_modify)] = new_value
        
        auxiliar_writer.writerow(reservation)
        
    reservations.close()
    auxiliar.close()
    
    rename(AUXILIAR,RESERVATIONS)
    
    print(f"The field {field_to_modify} from the reservation {reservation_to_modify_id} was sucesfully modified")

# Modifies a field from the reservation with id reservation_to_modify_id
def modify(reservation_to_modify_id):
    reservation_to_modify_id_exist, file_exist = id_exist(reservation_to_modify_id)
    changed = False

    if not reservation_to_modify_id_exist and file_exist:
        print("There's no reservation with that id")
    elif not file_exist:
        pass
    else:
        while not changed:
            change = input("What do you want to change?: ").split()
            if len(change) == CHANGE_LENGTH:
                command = change[COMMAND]
                value = change[VALUE]
    
                if command == NAME:
                    modify_field(reservation_to_modify_id, command, value)
                    changed = True
                elif command == PEOPLE_AMOUNT:
                    if valid_people_amount(value):
                        modify_field(reservation_to_modify_id, command, value)
                        changed = True
                    else:
                        print("People amount is invalid, check that it is greater than 0")
                elif command == HOUR:
                    if valid_hour(value):
                        modify_field(reservation_to_modify_id, command, value)
                        changed = True
                    else:
                        print("New hour is invalid, check that it is in the format hh:mm and that it is between 00:00 and 23:59")
                elif command == UBICATION:
                    if valid_ubication(value):
                        modify_field(reservation_to_modify_id, command, value)
                        changed = True
                    else:
                        print("Ubication is invalid, check that it is O (outside) or I (INSIDE)")
                else:
                    print("Command is invalid\n")
                    print("Commands are 'name', 'amount', 'hour' y 'ubication'")
            elif len(change) > CHANGE_LENGTH:
                print("Too much arguments\n")
                print("Recordá que debes ingresar el campo que querés cambiar y separado con un espacio el nuevo valor de ese campo")
                print("Remember that you have to type the field you want to modify and separated with an space, the new value for that field")
            else:
                print("Please, write your change leaving an space in between the command and the value")
        
# deletes the reservation that has the id reservation_to_eliminate_id
def delete(reservation_to_delete_id):
    reservation_to_delete_id_exists , file_exists = id_exist(reservation_to_delete_id)
    
    if not reservation_to_delete_id_exists and file_exists:
        print("There isn't a reservation with that id.")
    elif not file_exists:
        pass
    else:
        
        try:
            reservations = open(RESERVATIONS,READ_ONLY)
        except:
            error_opening(RESERVATIONS)
            return
    
        try:
            auxiliar = open(AUXILIAR,READ_ONLY)
        except:
            reservations.close()
            error_creating(AUXILIAR)
            return
    
        reservations_reader = reader(reservations, delimiter = CSV_DELIMITER)
        auxiliar_writer = writer(auxiliar, delimiter = CSV_DELIMITER)
    
        for reservations in reservations_reader:
            if reservations[ID_INDEX] != reservation_to_delete_id:
                auxiliar_writer.writerow(reservations)
        
        reservations.close()
        auxiliar.close()
    
        rename(AUXILIAR,RESERVATIONS)
    
        print(f"Reservation {reservation_to_delete_id} was deleted succesfuly")

# Returns true if the list range is valid
def valid_range(min_range, max_range):
    return (min_range.isnumeric() and max_range.isnumeric()) and ( int(min_range) >= 0 and int(max_range) >= 0 and int(max_range) >= int(min_range) )

# Pre: reservation is a list loaded with a reservation info
# Pos: prints the reservation on screen
def print_reservation(reservation):
    print(f"ID: {reservation[ID_INDEX]}")
    print(f"Name: {reservation[NAME_INDEX]}")
    print(f"Amount of people: {reservation[PEOPLE_AMOUNT_INDEX]}")
    print(f"Hour: {reservation[HOUR_INDEX]}")
    print(f"Ubication: {reservation[UBICATION_INDEX]}\n")

# Prints the reservations that want to be listed
def list(min_range, max_range):
    if valid_range(min_range, max_range):
        try:
            reservations = open(RESERVATIONS,READ_ONLY)
        except:
            error_opening(RESERVATIONS)
            return
        
        reservations_reader = reader(reservations, delimiter = CSV_DELIMITER)
        
        for reservation in reservations_reader:
            if(int(reservation[ID_INDEX]) >= int(min_range) and int(reservation[ID_INDEX]) <= int(max_range)):
                print_reservation(reservation)
    else:
        print("List range is invalid\n")
        
        print("Check that both range limits are integers greater than 0 and that max_range is greater than min_range")