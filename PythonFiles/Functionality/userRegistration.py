from SQLFunctions import database

class User:
    def __init__(self):
        pass

    def createPermanantUser(self):
        # prompt user to enter the email they would like to create
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

                #creation of the column and value list for SQL query generation
                mailboxColumnList = ["username", "password", "name", "storagebasedirectory", "storagenode", "maildir", 
                                    "quota", "domain", "active", "passwordlastchange", "created"]
                mailboxValueList = [client_email, hashedPassString, username, STORAGE_DIRECTORY, 
                                    STORAGE_NODE, filepath, DEFAULT_QUOTA, 'privasurge.com', '1', 'NOW()', 'NOW()']

                forwardingColumnList = ["address", "forwarding", "domain", "dest_domain", "is_forwarding"]
                forwardingValueList = [client_email, client_email, 'privasurge.com', 'privasurge.com', '1' ]

                mailserver = database.Database
                mailserver.connectToDB()
                mailserver.insertData('vmail', 'mailbox', mailboxColumnList, mailboxValueList)
                mailserver.insertData('vmail', 'forwarding', forwardingColumnList, forwardingValueList)
                mailserver.disconnectFromDB()
              






        # Would each time the create user function is called a DB object be created and creates own connection to sql server


    def createTempEmail(self):
        #TODO Random name generation
        #TODO Store the username and creation date of temp in separate table 
        pass

    def createSemiPermanentUser(self):
        # Maybe an option a user could pay for that would allow them the ability to choose the length of time they create this user for
        pass
    
    def deleteUser(self):
        pass
