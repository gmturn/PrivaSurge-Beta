import mysql.connector  
from datetime import date, datetime
from mysql.connector.errors import Error

# the idea behind this file is to have it run as a cron job script on the database server once a day

def autoDeleteTempEmail():
    mysql.connector.connect(host="45.79.53.24", user="remote_test", password="Nielsen7579", database='vmail')
    # in Temp Email Data Table results[0] = first row | results[0][0] = web_id | results[0][1] = email_alias | results[0][2] = reference_email | results[0][3] = date_created | results[0][4] = file_path
    # import every date in the table from temp_email_data 
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM vmail.temp_email_data;"
    cursor.execute(query)
    results =  cursor.fetchall()
    cursor.close()
    for row in results:
        web_id = row[0]
        creationDate = row[3]
        creYear = int(creationDate[0:4])
        creMonth = int(creationDate[5:7])
        creDay = int(creationDate[8:])

        today = str(datetime.now())
        tDate = today[0:10]
        tYear = int(tDate[0:4])
        tMonth = int(tDate[5:7])
        tDay = int(tDate[8:])

        cre_date = date(creYear, creMonth, creDay)
        t_date = date(tYear, tMonth, tDay)

        delta = t_date - cre_date

        if delta.days > 15: 
            try:
                cursor = mysql.connection.cursor()
                query = f"DELETE FROM vmail.temp_email_data WHERE web_id='{web_id}';"
                query_commit = 'USE vmail;\n' +  query + '\nCOMMIT;'
                #print(query_commit)
                cursor.execute(query_commit, multi=True)
                mysql.connection.commit()
                cursor.close()
            except mysql.connection.Error as err:
                print(err)

            # delete entry in vmail & forwardings & temp_email_date