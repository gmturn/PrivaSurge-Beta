from .datahandling_functions import hashPassword, hashDate, generateEmailAlias, fetchDate
from .sql_functions import Database

class User:
    def __init__(self, client_username, client_email, client_password):
        pass
        self.username = client_username
        self.email = client_email
        self.password = client_password

    def createUser(self, database_object, uid):
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
        
    
        columnListMailbox = ["username", "password", "name", "storagebasedirectory", "storagenode", "maildir", "quota", "domain", 
                                "active", "passwordlastchange", "created", "web_id" ]
        valueListMailbox = [f"'{self.email}'", f"'{hashedPassString}'", f"'{self.username}'", f"'{STORAGE_DIRECTORY}'", 
                            f"'{STORAGE_NODE}'", f"'{filepath}'", f"'{DEFAULT_QUOTA}'", "'privasurge.net'", "'1'", "NOW()",
                            "NOW()", f"'{uid}'"]

        columnListForwardings = ['address', 'forwarding', 'domain', 'dest_domain', 'is_forwarding']
        valueListForwardings = [f"'{self.email}'", f"'{self.email}'", "'privasurge.net'", "'privasurge.net'", "1"]



        db_session = Database(database_object)
        db_session.insertData("vmail", "mailbox", columnListMailbox, valueListMailbox)
        db_session.insertData("vmail", "forwardings", columnListForwardings, valueListForwardings)
        
           

    def createWebUser(self, database_object, first_name, last_name):
        columnListUsers = ['email', 'password', 'first_name', 'last_name']
        valueListUsers = [f"'{self.email}'", f"'{self.password}'", f"'{first_name}'", f"'{last_name}'"]
        
        db_session = Database(database_object)
        db_session.insertData('web_data', 'users', columnListUsers, valueListUsers)            



    def generateTempEmail(self, database_object, uid):
        #TODO Random name generation
        alias = generateEmailAlias()
        aliasEmail = alias + '@privasurge.net' # DONT FORGET TO CHANGE TO .com
        forwardingDomain = self.email.split('@', 1)[1]

        # setting basic variables
        STORAGE_DIRECTORY = "/var/vmail"
        STORAGE_NODE = "vmail1"
        PASSWORD_SCHEME = "SSHA512"
        DEFAULT_QUOTA = '1024'
         
        # The directorys on the mail server are hashed for a specific format
        # directory format = "/privasurge.com/u/s/e/username/"
        firstLetter = alias[0]
        secondLetter = alias[1]
        thirdLetter = alias[2]

        #need to remember to delete actual file path not just the SQL row
        filepath = 'privasurge.net/' + firstLetter + '/' + secondLetter + '/' + thirdLetter + '/' + alias + '-' + hashDate() + '/' #ALSO NEED TO CHANGE DOMAIN HERE


        hashedPassword = hashPassword(self.password)
        hashedPassString = '{SSHA512}' + repr(hashedPassword)[2:-1]

        creationDate = fetchDate()

        columnListMailbox = ['username', 'password', 'name', 
                        'storagebasedirectory', 'storagenode', 'maildir'
                        'quota', 'domain', 'active', 'passwordlastchange', 'created']

        
        valueListMailbox = [f"'{aliasEmail}'", f"'{hashedPassString}'", f"'{alias}'", f"'{STORAGE_DIRECTORY}'", 
                            f"'{STORAGE_NODE}'", f"'{filepath}'", f"'{DEFAULT_QUOTA}'", "'privasurge.net'", "'1'", "NOW()",
                            "NOW()", f"'{uid}'"]# CHANGE DOMAIN HERE


        columnListForwardings = ['address', 'forwarding', 'domain', 'dest_domain', 'is_forwarding', 'active']
        valueListForwardings = [f"'{aliasEmail}'", f"'{self.email}'", "'privasurge.net'", f"'{forwardingDomain}'", "1", "1"]

        columnListTempEmailData = ['web_id', 'email_alias', 'reference_email', 'date_created', 'file_path']
        valueListTempEmailData = [f"'{uid}'", f"'{aliasEmail}'", f"'{self.email}'", f"'{creationDate}'", f"'{filepath}'"]


        db_session = Database(database_object)
        db_session.insertData("vmail", "mailbox", columnListMailbox, valueListMailbox)
        db_session.insertData("vmail", "forwardings", columnListForwardings, valueListForwardings)
        db_session.insertData("vmail", "temp_email_data", columnListTempEmailData, valueListTempEmailData)



if __name__ == '__main__':
    pass