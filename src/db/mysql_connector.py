import mysql.connector


class MySQLConnector:

    def __init__(self, host, port, user, password, database):
        self.port = port
        self.database = database
        self.password = password
        self.user = user
        self.host = host
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def select(self, select_query):
        print(f"Querying {select_query}")
        cur = self.connection.cursor()
        cur.execute(select_query)
        return cur.fetchall()

    def insert(self, insert_query):
        print(f"Querying {insert_query}")
        cur = self.connection.cursor()
        cur.execute(insert_query)
        self.connection.commit()
        return f'{cur.rowcount} records inserted.'
