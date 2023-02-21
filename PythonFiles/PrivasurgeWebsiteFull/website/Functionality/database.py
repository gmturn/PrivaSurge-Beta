import mysql.connector
from mysql.connector.errors import Error


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
            if self.mydb.is_connected():
                status = True
                print(f"Connection to Database {self.dbName} on {self.host} with user: {self.user} is successful")
                return status
            else: 
                status = False
                print("ERROR: CANNOT CONNECT TO SERVER")
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

    def createUserCursor(self):
        user_cursor = self.mydb.cursor()
        return user_cursor


    def insertData(self, database, table, columnList, valueList):
        try:
            status = False  
            query = f"""
            USE {database};
            INSERT INTO {table} ({", ".join(str(x) for x in columnList)})
            VALUES ({", ".join(str(x) for x in valueList)});
            COMMIT;
            """
            cursor = self.mydb.cursor()
            print(query)
            cursor.execute(query, multi=True)
            self.mydb.commit()
            cursor.close()
            status = True
            return status
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err.msg))




