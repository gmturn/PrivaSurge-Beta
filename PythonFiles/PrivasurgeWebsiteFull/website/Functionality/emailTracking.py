import mysql.connector  
from datetime import date, datetime


def autoDeleteTempEmail():
    # import every date in the table from temp_email_data 
    db_session = mysql.connector.connect(host="45.79.53.24", user="remote_test", password="Nielsen7579", database='vmail')
    cursor = db_session.cursor()
    query = "SELECT date_created FROM vmail.temp_email_data;"
    cursor.execute(query)
    datesList =  cursor.fetchall()
    cursor.close()

    for curr_date in datesList:

        TEST_DATE = "2023-02-10"
        creYear = int(TEST_DATE[0:4])
        creMonth = int(TEST_DATE[5:7])
        creDay = int(TEST_DATE[8:])

        today = str(datetime.now())
        tDate = today[0:10]
        tYear = int(tDate[0:4])
        tMonth = int(tDate[5:7])
        tDay = int(tDate[8:])

        cre_date = date(creYear, creMonth, creDay)
        t_date = date(tYear, tMonth, tDay)

        delta = t_date - c_date

        if delta.days > 15: 
            # delete entry in vmail & forwardings & temp_email_date
            cursor = db_session.cursor()
            query = f"DELETE FROM vmail.temp_email.data WHERE date_created='{curr_date}'"
            query_commit = query + '\nCOMMIT;'
            cursor.execute(query_commit, multi=True)
            cursor.close()


            # delete entry in the files - need to rehash email
            





if __name__ == '__main__':
    autoDeleteTempEmail()