from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
Objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    """
    TODO: Part 1
    """
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user. Please follow the correct format: create_patient <username> <password>")
        return

    # retrieve the username and password from the user input
    username = tokens[1]
    password = tokens[2]

    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    # check 3: check if the password is strong
    if not is_strong_password(password):
        return

    # generate the salt and hash for the password
    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    patient = Patient(username, salt=salt, hash=hash)

    # save patient information to our database
    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_patient(username):
    # create a connection to the database
    cm = ConnectionManager()
    conn = cm.create_connection()

    # create the queries to be used in the try statement
    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        # create a cursor to query the database
        cursor = conn.cursor(as_dict=True)

        # check to see if the given username is already in the database
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user. Please follow the correct format: create_caregiver <username> <password>")
        return

    # retrieve the username and password from the user input
    username = tokens[1]
    password = tokens[2]

    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    # check 3: check if the password is strong
    if not is_strong_password(password):
        return

    # generate the salt and hash for the password
    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_caregiver(username):
    # create a connection to the database
    cm = ConnectionManager()
    conn = cm.create_connection()

    # create the queries to be used in the try statement
    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        # create a cursor to query the database
        cursor = conn.cursor(as_dict=True)

        # check to see if the given username is already in the database
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    """
    TODO: Part 1
    """
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed. Please follow the correct format: login_patient <username> <password>")
        return

    # retrieve the username and password from the user input
    username = tokens[1]
    password = tokens[2]

    # initialize a variable to be used for checking if the login was successful
    patient = None

    # log the patient in using the given username and password
    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if patient is None:
        print("Login failed. Username or password is incorrect.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed. Please follow the correct format: login_caregiver <username> <password>")
        return

    # retrieve the username and password from the user input
    username = tokens[1]
    password = tokens[2]

    # initialize a variable to be used for checking if the login was successful
    caregiver = None

    # log the caregiver in using the given username and password
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed. Username or password is incorrect.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    """
    TODO: Part 2
    """
    # search_caregiver_schedule <date>
    # check 1: if nobody's logged-in, they need to log in first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    
    # check 2: the length for tokens needs to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again! Please follow the correct format: search_caregiver_schedule <date>")
        return
    
    # retrieve date from user input
    date = tokens[1]

    # check 3: make sure the length of the date is 3 after splitting on - to ensure (loosely) that the date is correctly formatted
    date_tokens = date.split("-")
    if len(date_tokens) != 3:
        print("Please try again! Please follow the correct date format: MM-DD-YYYY")
        return
    
    # retrieve the month, day, and year from the date tokens
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    # create a connection to the database
    cm = ConnectionManager()
    conn = cm.create_connection()

    # create the queries to be used in the try statement
    select_usernames = "SELECT Username FROM Availabilities WHERE Time=%s ORDER BY Username"
    select_vaccines = "SELECT * FROM Vaccines"
    try:
        # turn the date tokens into a datetime value
        d = datetime.datetime(year, month, day)

        # create a cursor to query the database
        cursor = conn.cursor(as_dict=True)

        # find and display the usernames of the available caregivers
        cursor.execute(select_usernames, d)
        print("Caregiver Usernames:")
        for row in cursor:
            print(row['Username'])

        # print a blank line for aesthetic reasons
        print()

        # find and display the available vaccines and their corresponding doses
        cursor.execute(select_vaccines)
        print("Vaccine Names and Availible Doses:")
        for row in cursor:
            print(row['Name'], row['Doses'])

    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()


def reserve(tokens):
    """
    TODO: Part 2
    """
    # reserve <date> <vaccine>
    # check 1: if nobody's logged-in, they need to log in first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    
    # check 2: check if the current logged-in user is a patient
    if current_patient is None:
        print("Please login as a patient!")
        return

    # check 3: the length for tokens needs to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again! Please follow the correct format: reserve <date> <vaccine>")
        return
    
    # retrieve date from user input
    date = tokens[1]

    # check 4: make sure the length of the date is 3 after splitting on - to ensure (loosely) that the date is correctly formatted
    date_tokens = date.split("-")
    if len(date_tokens) != 3:
        print("Please try again! Please follow the correct date format: MM-DD-YYYY")
        return
    
    # retrieve the month, day, and year from the date tokens
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])

    # retrieve vaccine name from user input
    vaccine_name = tokens[2]

    # initialize a variable used to represent a Vaccine object instance
    vaccine = None

    # create a connection to the database
    cm = ConnectionManager()
    conn = cm.create_connection()

    # create the queries to be used in the try statement
    select_caregiver = "SELECT TOP 1 Username FROM Availabilities WHERE Time=%s ORDER BY Username"
    vaccine_doses = "SELECT * FROM Vaccines WHERE Name=%s"
    add_appointment = "INSERT INTO Appointments VALUES (%s, %s, %s, %s)"
    select_aid = "SELECT TOP 1 Aid from Appointments ORDER BY Aid DESC"
    select_app = "SELECT Cuname FROM Appointments WHERE Cuname=%s AND Date=%s"
    try:
        # turn the date tokens into a datetime value
        d = datetime.datetime(year, month, day)

        # create a cursor to query the database
        cursor = conn.cursor(as_dict=True)

        # find the caregiver who will administer the vaccine appointment
        cursor.execute(select_caregiver, d)
        caregiver = None
        for row in cursor:
            caregiver = row['Username']

        # check 5: check if there are any available caregivers on this date
        if caregiver is None:
            print("No Caregiver is available!")
            return

        # check and see if the avaibale caregiver already has an appointment on this date
        cursor.execute(select_app, (caregiver, d))
        temp_caregiver = None
        for row in cursor:
            temp_caregiver = row['Cuname']

        # check 6: make sure the caregiver doesn't already have an appointment on this date
        if temp_caregiver is not None:
            print("{} already has an appointment on this date. The availability has been removed.".format(temp_caregiver))
            
            # remove the administering caregivers availability from the availability schedule
            Caregiver(caregiver).remove_availability(d)
            return

        # find the name of the vaccine the user wants in the database
        cursor.execute(vaccine_doses, vaccine_name)
        real_vaccine = None
        for row in cursor:
            real_vaccine = row['Name']

        # check 7: check if the vaccine is in the database
        if real_vaccine is None:
            print("Vaccine is not in the database!")
            return

        # since the vaccine exists, set the vaccine variable to the Vaccine object instance
        vaccine = Vaccine(real_vaccine, 1).get()

        # check 8: check if there are any available doses
        if vaccine.get_available_doses() == 0:
            print("Not enough available doses!")
            return
        else:
            vaccine.decrease_available_doses(1)

        # add the appointment to the appointment schedule
        cursor.execute(add_appointment, (d, current_patient.get_username(), caregiver, vaccine_name))

        # obtain the appointment id for displaying to the patient
        cursor.execute(select_aid)
        for row in cursor:
            aid = row['Aid']

        # remove the administering caregivers availability from the availability schedule
        Caregiver(caregiver).remove_availability(d)
    
        # commit/save the changes to the database
        conn.commit()

    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()
    
    # display the appointment confirmation to the patient
    print("Appointment ID: {}, Caregiver username: {}".format(aid, caregiver))
    

def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again! Please follow the correct format: upload_availability <date>")
        return

    # retrieve date from user input
    date = tokens[1]

    # check 3: make sure the length of the date is 3 after splitting on - to ensure (loosely) that the date is correctly formatted
    date_tokens = date.split("-")
    if len(date_tokens) != 3:
        print("Please try again! Please follow the correct date format: MM-DD-YYYY")
        return
    
    # retrieve the month, day, and year from the date tokens
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        # turn the date tokens into a datetime value
        d = datetime.datetime(year, month, day)

        # add the caregiver's availability to the availability schedule
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra Credit
    """
    # cancel <appointment_id>
    # check 1: if nobody's logged-in, they need to log in first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    
    # check 2: the length for tokens needs to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again! Please follow the correct format: cancel <appointment_id>")
        return
    
    # retrieve the aid from user input
    aid = tokens[1]

    # create a connection to the database
    cm = ConnectionManager()
    conn = cm.create_connection()

    # create the queries to be used in the try statement
    get_appointment = "SELECT * FROM Appointments WHERE Aid=%s"
    cancel_appointment = "DELETE FROM Appointments WHERE Aid=%s"
    get_uname_date = "SELECT Cuname, Vname, Date FROM Appointments WHERE Aid=%s"
    add_availability = "INSERT INTO Availabilities VALUES (%s , %s)"
    try:
        # create a cursor to query the database
        cursor = conn.cursor(as_dict=True)

        # check 3: make sure the user trying to cancel the appointment is apart of the scehduled appointment
        
        # if the logged in user is a caregiver run this
        if current_caregiver is not None:
            
            # obtain the caregivers username
            caregiver = current_caregiver.get_username()

            # see if the caregiver is administering this given appoitnemnt
            cursor.execute(get_appointment, aid)
            for row in cursor:
                if caregiver != row['Cuname']:
                    print("You are not apart of this appointment. Please try again!")
                    return
        
        # if the logged in user is a patient run this
        else:
            # obtain the patients username
            patient = current_patient.get_username()

            # see if the patient is apart of this given appointment
            cursor.execute(get_appointment, aid)
            for row in cursor:
                if patient != row['Puname']:
                    print("You are not apart of this appointment. Please try again!")
                    return

        # obtain the appointment id that the user is trying to cancel
        cursor.execute(get_appointment, aid)
        temp_id = None
        for row in cursor:
            temp_id = row['Aid']
        
        # check 4: make sure the appointment id is a valid appointment
        if temp_id is None:
            print("Appointment {} does not exist. Please try again!".format(aid))
            return

        # obtain the cargiver username, vaccine name, and date of appointment that is getting cancelled
        cursor.execute(get_uname_date, aid)
        output = cursor.fetchone()
        cuname = output["Cuname"]
        vaccine_name = output["Vname"]
        date = output["Date"]

        # cancel the appointment and remove it from the appointment schedule
        cursor.execute(cancel_appointment, aid)
        print("Appointment cancelled successfully!")

        # add the caregiver's availability back into the availability schedule
        cursor.execute(add_availability, (date, cuname))
        print("Caregiver availability successfully added back!")

        # add the vaccine dose back
        vaccine = Vaccine(vaccine_name, 1).get()
        vaccine.increase_available_doses(1)
        print("{} doses successfully added back!".format(vaccine_name))

        # commit/save the changes to the database
        conn.commit()

    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again! Please follow the correct format: add_doses <vaccine> <number>")
        return

    # obtain vaccine name from user input
    vaccine_name = tokens[1]

    # obtain number of vaccine doses from user input
    doses = int(tokens[2])

    # initialize a variable used to represent a Vaccine object instance
    vaccine = None

    try:
        # attempt to set the vaccine variable to the Vaccine object instance
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    '''
    TODO: Part 2
    '''
    # show_appointments
    # check 1: if nobody's logged-in, they need to log in first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    
    # check 2: the length for tokens needs to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 1:
        print("Please try again! Please follow the correct format: show_appointments")
        return
    
    # create a connection to the database
    cm = ConnectionManager()
    conn = cm.create_connection()

    try:
        # create a cursor to query the database
        cursor = conn.cursor(as_dict=True)

        # if the logged in user is a caregiver do this
        if current_caregiver is not None:

            # create the query to be used in the try statement
            select_appointments = "SELECT * FROM Appointments WHERE Cuname=%s ORDER BY Aid"

            # find and display the appointments that this caregiver is administering
            cursor.execute(select_appointments, current_caregiver.get_username())
            print("Appointments Scheduled For {}:".format(current_caregiver.get_username()))
            for row in cursor:
                print("Appointment ID: {}, Vaccine name: {}, Date: {}, Patient name: {}".format(row['Aid'],
                                                                                                row['Vname'],
                                                                                                row['Date'],
                                                                                                row['Puname']))
        
        # if the logged in user is a patient do this
        else:
            # create the query to be used in the try statement
            select_appointments = "SELECT * FROM Appointments WHERE Puname=%s ORDER BY Aid"

            # find and display the appointments that this patient is apart of
            cursor.execute(select_appointments, current_patient.get_username())
            print("Appointments Scheduled For {}:".format(current_patient.get_username()))
            for row in cursor:
                print("Appointment ID: {}, Vaccine name: {}, Date: {}, Caregiver name: {}".format(row['Aid'],
                                                                                                  row['Vname'],
                                                                                                  row['Date'],
                                                                                                  row['Cuname']))

    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please try again!")
        return
    except Exception as e:
        print("Please try again!")
        print("Error:", e)
        return
    finally:
        cm.close_connection()


def logout(tokens):
    """
    TODO: Part 2
    """
    # logout
    # check 1: if nobody's logged-in, they need to log in first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first.")
        return
    
    # check 2: the length for tokens needs to be exactly 1 to include all information (with the operation name)
    if len(tokens) != 1:
        print("Please try again! Please follow the correct format: logout")
        return

    # If the two checks are passed, log the user out
    print("Successfully logged out!")
    current_caregiver = None
    current_patient = None


def is_strong_password(password):
    # initialize variables that track the existence of specific types of characters
    letter = False
    numeric = False
    special = False

    # check 1: the length of the password must be 8 charcaters or greater
    if len(password) < 8:
        print("Your password must be at least 8 charcaters long.")
        return False
    
    # go through every charcacter in the intended password and check for the existence of certain types of characters
    for character in password:
        if character.isalpha():
            letter = True
        if character.isnumeric():
            numeric = True
        if character in ["!", "@", "#", "?"]:
            special = True

    # check 2: the password must contain letters
    if not letter:
        print("Your password must contain letters.")
        return False
    
    # check 3: the password must contain numbers
    if not numeric:
        print("Your password must contain at least one numeric character.")
        return False
    
    # check 4: the password must contain special characters
    if not special:
        print("Your password must contain at least one special character, from “!”, “@”, “#”, “?”.")
        return False
    
    # check 5: the password must contain lowercase and uppercase letters
    if password.isupper() or password.islower():
        print("Your password must contain uppercase and lowercase letters.")
        return False
    
    # if the intended password contains all of these features, it is strong
    return True


def list_commands():
    # list the commands that the user can perform
    print()
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")  # // TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> Quit")
    print()


def start():
    stop = False
    while not stop:
        list_commands()
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0].lower()
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start the command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
    