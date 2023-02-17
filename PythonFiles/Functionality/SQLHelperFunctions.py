from datetime import datetime
from hashlib import sha512
from base64 import b64encode
import os


def displayUsers(cursor):
    select_querey = "select * from mailbox"
    cursor.execute(select_querey)
    results = cursor.fetchall()

    print("The total number of rows in Users is: ", cursor.rowcount)

    print("\nPrinting all entries:\n")

    for row in results:
        print("Username: ", row[0])
        print("Encrypted Password: ", row[1])
        print("name: ", row[2])

def createUser(cursor):
    # Asking the user to enter the email
    client_email = input("Please Enter the email addres you would like to add: ")
    confirm = input("Is " + client_email + " the email address you would like to add? ")
    if (confirm == "Yes"):
        # setting basic variables
        STORAGE_DIRECTORY = "/var/vmail"
        STORAGE_NODE = "vmail1"
        PASSWORD_SCHEME = "SSHA512"
        DEFAULT_QUOTA = '1024'

        # The directorys on the mail server are hashed for a specific format
        # directory format = "/privasurge.com/u/s/e/username/"
        username = client_email.split('@')[0]
        firstLetter = username[0]
        secondLetter = username[1]
        thirdLetter = username[2]
        filepath = 'privasurge.com/' + firstLetter + '/' + secondLetter + '/' + thirdLetter + '/' + username + '-' + hashDate() + '/'

        # checking to see if the client entered the correct password
        clientPassword = input('Please enter your chosen password: ')
        clientPasswordCheck = input('Please renter your chosen password: ')
        if clientPassword != clientPasswordCheck:
            print('ERROR: Passwords do not match')
        else:
            hashedPassword = hashPassword(clientPassword)
            hashedPassString = '{SSHA512}' + repr(hashedPassword)[2:-1]

        # F strings to format the SQL Querey correctly
        sqlQuereyMailBox = f"""
        USE vmail;
        INSERT INTO mailbox (username, password, name,
                     storagebasedirectory,storagenode, maildir,
                     quota, domain, active, passwordlastchange, created)
             VALUES ('{client_email}', '{hashedPassString}', '{username}',
                     '{STORAGE_DIRECTORY}','{STORAGE_NODE}', '{filepath}',
                     '{DEFAULT_QUOTA}', 'privasurge.com', '1', NOW(), NOW());
        """

        sqlQuereyForwardings = f"""
        INSERT INTO forwardings (address, forwarding, domain, dest_domain, is_forwarding)
                 VALUES ('{client_email}', '{client_email}','privasurge.com', 'privasurge.com', 1);
        """

        #combining the two rows for the sake of speed and simplicity - must append commit to sql querey
        sqlQuerey = sqlQuereyMailBox + sqlQuereyForwardings + '\nCOMMIT;'
        cursor.execute(sqlQuerey)

    else:
        print ('Quitting')

def removeUser (cursor): #DEBUG AND TESTING PURPOSES
    emailDeleteRequest = input("Please enter the email you would like to delete from the database: ")
    emailDeleteCheck = input("Is: " + emailDeleteRequest + " the email you would like to remove from the database?")
    if emailDeleteCheck == "Yes" or "yes" or "y":
        select_querey = "select * from mailbox"
        cursor.execute(select_querey)
        results = cursor.fetchall()
        checkList = []
        for row in results:
            username = row[0]
            checkList.append(username)
            if emailDeleteRequest == row[0]:
                sqlQuereyMailbox = "DELETE FROM mailbox WHERE address='" + emailDeleteRequest + "';"
                sqlQuereyForwarding = "DELETE FROM forwardings WHERE address='" + emailDeleteRequest + "';"
                sqlQuerey = 'USE vmail;\n' + sqlQuereyMailbox + '\n' + sqlQuereyForwarding + '\nCOMMIT;'
                print(sqlQuerey)

        if emailDeleteRequest not in checkList:
            print("That user is not in our database. Sorry!")
    else:
        print("Will not remove " + emailDeleteRequest)

















def hashDate():
    hashDate = str(datetime.now())
    year = hashDate[:4]
    month = hashDate[5:7]
    day = hashDate[8:10]
    hour = hashDate[11:13]
    minute = hashDate[14:16]
    second = hashDate[17:19]
    hashedDateString = year + '.' + month + '.' + day + '.' + hour + '.' + minute + '.' + second
    return hashedDateString

def hashPassword(password):
    password = bytes(password.encode('utf-8'))
    salt = os.urandom(8)
    pw = sha512(password)
    pw.update(salt)
    return b64encode(pw.digest() + salt)

