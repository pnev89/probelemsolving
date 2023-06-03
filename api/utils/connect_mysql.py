import mysql.connector

class ConfigureDBConnection:
    """Configuration of the database."""
    def __init__(self,
                host:str="localhost",
                port:str=3306,
                username:str="root",
                password:str="password",
                database:str="mysql"):
        """Initializes a connections.

        Parameters
        ----------
        host : str, optional
            Hostname, by default "localhost"
        port : str, optional
            Port, by default 3306
        username : str, optional
            Username, by default "root"
        password : str, optional
            Password, by default "password"
        database : str, optional
            Databse, by default "mysql"
        """
         # specify connection string
        self.host = host
        self.port = port
        self.user = username
        self.password = password
        self.database = database
            

        o_conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database)

        self.o_conn = o_conn

    def query(self, s_query):

        o_cursor = self.o_conn.cursor()

        o_cursor.execute(s_query)

        results = o_cursor.fetchall()

        o_cursor.close()

        return results

    def insert(self, s_query):

        o_cursor = self.o_conn.cursor()

        o_cursor.execute(s_query)
        i_inserted_row_count = o_cursor.rowcount

        # Make sure data is committed to the database
        self.o_conn.commit()

        return i_inserted_row_count

    def delete(self, s_query):

        o_cursor = self.o_conn.cursor()

        o_cursor.execute(s_query)
        i_deleted_row_count = o_cursor.rowcount

        # Make sure data is committed to the database
        self.o_conn.commit()

        return i_deleted_row_count


    def close(self):

        self.o_conn.close()