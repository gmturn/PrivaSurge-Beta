from SQLFunctions import database

class User:
    def __init__(self):
        pass

    def createPermenantUser(self):
        pass
        # Would each time the create user function is called a DB object be created and creates own connection to sql server


    def createTempEmail(self):
        #TODO Random name generation
        #TODO Store the username and creation date of temp in separate table 
        self.createUser()

    def createSemiPermanentUser(self):
        # Maybe an option a user could pay for that would allow them the ability to choose the length of time they create this user for
        pass
    
    def deleteUser(self):
        pass
