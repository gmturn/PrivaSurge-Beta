class Database:
    def __init__(self, database_object):
        self.mysql = database_object

    def insertData(self, database_name, table_name, columnList, valueList):
        status = False
        try:
            cursor = self.mysql.connection.cursor()
            status = False  
            query = f"""
                USE {database_name};
                INSERT INTO {table_name} ({", ".join(str(x) for x in columnList)})
                VALUES ({", ".join(str(x) for x in valueList)});
                COMMIT;
            """
            cursor.execute(query)
            cursor.close()
        except self.mysql.Error as e:
            print(e)