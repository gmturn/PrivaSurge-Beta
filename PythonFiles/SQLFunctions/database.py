import mysql.connector

# Operations that fail to execute will return False
# Operations that successfully execute will return True



class Database:
    def __init__(self, databaseName, hostname, username, passkey):  # must know the host, user, and pass to initialize a db object
        self.dbName = databaseName
        self.host = hostname
        self.user = username
        self.password = passkey

    # Initializes Database connection
    def connectToDB(self):
        status = False
        try:
            self.mydb = mysql.connector.connect(  # initializes a connection to the database with the passed arguments
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.dbName
            )
            status = True
            return status
        
        except:
            status = False
            print("ERROR FUCK TITTY SHIT ASS BITCHHHHH")
            return status


    # Closes Database connection
    def disconnectFromDB(self):
        status = False
        try:
            self.mydb.close()  # attempts to close connection and notifies if there is an error
            status = True
            return status
        
        except:
            status = False
            return status


    def createTable(self, tableName, columnList, datatypeList):
        status = False
        if len(columnList) != len(datatypeList):
            status = False
            return status
        else:
            pass
            cursor = self.mydb.cursor()
            cursor.execute("SHOW TABLES")  # runs a check to make sure the table does not already exist

            for tblList in cursor:
                for tbl in tblList:
                    if tbl == tableName:  # compares table name to pre-existing tables
                        status = False
                        return status

            

    
mailserver = Database("vmail", "96.126.122.182", "remote", "Nielsen7579")
mailserver.connectToDB()
mailserver.disconnectFromDB()
