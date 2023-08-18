# Restaurant_reservations_system
This is a task that was part of a subject in 1st year of university, it lets the user use 4 commands to add, modify, delete or list reservations that will be saved in a .csv file.

Commands:
- Add:
    Run the program with the following line: python3 main.py add -name- -amount of people- -hour- -ubication-. The hour must be in hh:mm format and the possible ubications are O (outside) and I (inside). The
  program will tell the user if the reservations was added succesfuly or if there was an error and something has to be changed.

- Modify:
    Run the program with the following line: python3 main.py modify -ID of the reservation user wants to modify-. Then the program will ask what field of the reservation the user wants to modify, possible answers: name -new name- | amount -new amount of people- | hour -new hour- | ubication -new ubication-. The program will tell the user if the reservations was modified succesfuly or if there was an error and something has to be changed.

- Delete:
    Run the program with the following line: python3 main.py delete -ID of the reservation user wants to delete-. The program will tell the user if the reservations was deleted succesfuly or if there was an error and something has to be changed.

- List:
    Run the program with the following line: python3 main.py list -first element ID- -last element ID-. The range values are optional, if the user doesn't type them, the program wiil list every reservation. The program will tell the user if there was an error and something has to be changed. If the first element is greater than the greatest ID, then nothing is listed.

The program was tested on Linux.
