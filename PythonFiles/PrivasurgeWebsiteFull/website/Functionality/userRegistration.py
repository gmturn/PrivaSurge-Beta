# from database import Database
from website.database import mysql
import random
from datetime import datetime
from hashlib import sha512
from base64 import b64encode
import os

class User:
    def __init__(self, username):
        self.username = username

    def createWebUser(self, email, passkey, firstName, lastName):
        

        
            
        sql = f"""

            INSERT INTO web_data.users (email, password, first_name, last_name)
                VALUES ({email}, "{passkey}", "{firstName}", "{lastName}")
        """
        try:
            cursor = mysql.connection.cursor()
            cursor.execute(sql)
            mysql.connection.commit()
            cursor.close() 
        except mysql.connection.Error as err:
            print(err)
     

    def createPermenantUser(self, username, client_email, password, web_id):
            # setting basic variables
            STORAGE_DIRECTORY = "/var/vmail"
            STORAGE_NODE = "vmail1"
            PASSWORD_SCHEME = "SSHA512"
            DEFAULT_QUOTA = "1024"

            # The directorys on the mail server are hashed for a specific format
            # directory format = "/privasurge.com/u/s/e/username/"
            firstLetter = username[0]
            secondLetter = username[1]
            thirdLetter = username[2]

            #dont forget to change privasurge.com to privasurge.net
            filepath = 'privasurge.net/' + firstLetter + '/' + secondLetter + '/' + thirdLetter + '/' + username + '-' + hashDate() + '/'


            # checking to see if the client entered the correct password
            hashedPassword = hashPassword(password)
            hashedPassString = '{SSHA512}' + repr(hashedPassword)[2:-1]
            


            #creation of the column and value list for SQL query generation
            sqlQuereyMailBox = f"""
                    USE vmail;
                    INSERT INTO mailbox (username, password, name,
                     storagebasedirectory,storagenode, maildir,
                     quota, domain, active, passwordlastchange, created, web_id)
                    VALUES ({client_email}, '{hashedPassString}', '{username}',
                     '{STORAGE_DIRECTORY}','{STORAGE_NODE}', '{filepath}',
                     '{DEFAULT_QUOTA}', 'privasurge.net', '1', NOW(), NOW(), '{web_id}');
                    """

            sqlQuereyForwardings = f"""
                    INSERT INTO forwardings (address, forwarding, domain, dest_domain, is_forwarding)
                            VALUES ({client_email}, {client_email},'privasurge.net', 'privasurge.net', 1);
                    """
            
            #combining the two rows for the sake of speed and simplicity - must append commit to sql querey
            
            sqlQuerey = sqlQuereyMailBox + sqlQuereyForwardings + '\nCOMMIT;'
            try:
                cursor = mysql.connection.cursor()
                print(sqlQuerey)
                cursor.execute(sqlQuerey)
                mysql.connection.commit()
                cursor.close()
            except mysql.connect.Error as err:
                print(err)
            #mailserver = database.Database
            #mailserver.connectToDB()
            #mailserver.insertData('vmail', 'mailbox', mailboxColumnList, mailboxValueList)
            #mailserver.insertData('vmail', 'forwarding', forwardingColumnList, forwardingValueList)
            #mailserver.disconnectFromDB()
            






        # Would each time the create user function is called a DB object be created and creates own connection to sql server


    def createTempEmail(self, password1, password2, forwardingAddress, web_uid):
        #TODO Random name generation
        alias = generateEmailAlias()
        aliasEmail = alias + '@privasurge.net' # DONT FORGET TO CHANGE TO .com
        forwardingDomain = forwardingAddress.split('@', 1)[1]

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
        # checking to see if the client entered the correct password
        if password1 != password2:
            print('ERROR: Passwords do not match')
        else:
            hashedPassword = hashPassword(password1)
            hashedPassString = '{SSHA512}' + repr(hashedPassword)[2:-1]


            db = mysql.connector.connect(host="45.79.53.24", user="remote_test", password="Nielsen7579", database='vmail')


            columnListMailbox = ['username', 'password', 'name', 
                        'storagebasedirectory', 'storagenode', 'maildir'
                        'quota', 'domain', 'active', 'passwordlastchange', 'created']

            valueListMailbox = [aliasEmail, hashedPassString, alias, STORAGE_DIRECTORY, 
                        STORAGE_NODE, filepath, DEFAULT_QUOTA, 
                        'privasurge.net', '1'] # CHANGE DOMAIN HERE

            valueListMailbox2 = ['NOW()', 'NOW()']

            columnListForwarding = ['address', 'forwarding', 'domain', 'dest_domain', 'is_forwarding', 'active']
            valueListForwarding = [aliasEmail, forwardingAddress, 'privasurge.net', forwardingDomain, '1', '1']
            sqlQuereyMailBox = f"""
                    USE vmail;
                    INSERT INTO mailbox (username, password, name,
                     storagebasedirectory,storagenode, maildir,
                     quota, domain, active, passwordlastchange, created)
                    VALUES ('{aliasEmail}', '{hashedPassString}', '{alias}',
                     '{STORAGE_DIRECTORY}','{STORAGE_NODE}', '{filepath}',
                     '{DEFAULT_QUOTA}', 'privasurge.net', '1', NOW(), NOW());
                    """

            sqlQuereyForwardings = f"""
                    INSERT INTO forwardings (address, forwarding, domain, dest_domain, is_forwarding)
                            VALUES ('{aliasEmail}', '{forwardingAddress}','privasurge.net', '{forwardingDomain}', 1);
                    """
            
            #combining the two rows for the sake of speed and simplicity - must append commit to sql querey
            if (db):
                sqlQuerey = sqlQuereyMailBox + sqlQuereyForwardings + '\nCOMMIT;'
                cursor = db.cursor()
                print('executed successfully')
                #cursor.execute(sqlQuerey, multi=True)
                cursor.close()
                return aliasEmail
            else:
                (print("error connecting to database"))


    def createSemiPermanentUser(self):
        # Maybe an option a user could pay for that would allow them the ability to choose the length of time they create this user for
        pass
    
    def deleteUser(self):
        pass


def generateEmailAlias():
    colorWord = ['red', 'blue', 'green', 'orange', 'black', 'brown', 'white', 'pink', 'purple']
    animalWord = ['lion', 'tiger', 'bear', 'fox', 'zebra', 'giraffe', 'elephant', 'mouse', 'dog', 'cat']
    numbers = [0,1,2,3,4,5,6,7,8,9]

    emailAlias = random.choice(colorWord) + random.choice(animalWord) + str(random.choice(numbers)) + str(random.choice(numbers))
    return emailAlias

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



if __name__ == '__main__':
    user1 = User()
    user1.createPermenantUser('jnielsen1919', 'jnielsen1919@privasurge.net', 'Nielsen7579')
