from .datahandling_functions import hashPassword, hashDate

class User:
    def __init__(self, client_username, client_email, client_password, client_id):
        pass
        self.username = client_username
        self.email = client_email
        self.password = client_password
        self.uid = client_id

    def createUser(self, database_object):
         # setting basic variables
        STORAGE_DIRECTORY = "/var/vmail"
        STORAGE_NODE = "vmail1"
        PASSWORD_SCHEME = "SSHA512"
        DEFAULT_QUOTA = "1024"

        # The directorys on the mail server are hashed for a specific format
        # directory format = "/privasurge.com/u/s/e/username/"
        firstLetter = self.username[0]
        secondLetter = self.username[1]
        thirdLetter = self.username[2]

        #dont forget to change privasurge.com to privasurge.net
        filepath = 'privasurge.net/' + firstLetter + '/' + secondLetter + '/' + thirdLetter + '/' + self.username + '-' + hashDate() + '/'


        # checking to see if the client entered the correct password
        hashedPassword = hashPassword(self.password)
        hashedPassString = '{SSHA512}' + repr(hashedPassword)[2:-1]
        


        #creation of the column and value list for SQL query generation
        


    def generateTempEmail(self, database_object):
        pass
