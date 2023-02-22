import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_contacts(self):
        sql = """
           CREATE TABLE Contacts (
               id int NOT NULL,
               username varchar NOT NULL,
               contact_name varchar,
               is_control int,
               writer_id int,
               PRIMARY KEY (id)
               );"""
        self.execute(sql, commit=True)

    def create_table_passwords(self):
        sql = """
           CREATE TABLE Passwords (
               pass1 varchar NOT NULL,
               pass2 varchar NOT NULL,
               PRIMARY KEY (pass1)
               );"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())


    def add_contact(self, id: int, username: str, contact_name=None, is_control: int=0, writer_id:int=0):
        sql = """
        INSERT INTO Contacts(id, username, contact_name, is_control, writer_id) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, username, contact_name,is_control, writer_id), commit=True)

    def select_contact(self, **kwargs):
        sql = "SELECT * FROM Contacts WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_contacts(self):
        sql = """
        SELECT * FROM Contacts
        """
        return self.execute(sql, fetchall=True)

    def add_contact_name(self, contact_name, id):
        sql="""
        UPDATE Contacts SET contact_name=? WHERE id=?
        """
        return self.execute(sql, parameters=(contact_name, id), commit=True)

    def all_control_break(self):
        sql="""
        UPDATE Contacts SET is_control=0 WHERE TRUE
        """
        return self.execute(sql, commit=True)

    def all_wirter_break(self):
        sql = """
        UPDATE Contacts SET writer_id=0 WHERE TRUE
                """
        return self.execute(sql, commit=True)

    def control_break(self,id):
        sql="""
        UPDATE Contacts SET is_control=0 WHERE id=?
        """
        return self.execute(sql, parameters=(id),commit=True)

    def add_controller(self,id):
        sql = """
        UPDATE Contacts SET is_control=? WHERE id=?
                """
        return self.execute(sql, parameters=(1, id), commit=True)

    def connect_write(self,id,writer_id):
        sql = """
        UPDATE Contacts SET writer_id=? WHERE id=?
        """
        return self.execute(sql, parameters=(writer_id,id), commit=True)

    def add_password(self, pass1: str, pass2: str = "20060729"):
        sql = """
        INSERT INTO Passwords(pass1,pass2) VALUES(?,?)
        """
        self.execute(sql, parameters=(pass1, pass2), commit=True)

    def select_password(self, **kwargs):
        sql = "SELECT * FROM Passwords WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_passwords(self):
        sql = """
        SELECT * FROM Passwords
        """
        return self.execute(sql, fetchall=True)

    def delete_password(self, pass1):
        sql = f"""
        DELETE FROM Passwords WHERE pass1=?
        """
        return self.execute(sql, (pass1,), commit=True)


def logger(statement):
    a = (f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
