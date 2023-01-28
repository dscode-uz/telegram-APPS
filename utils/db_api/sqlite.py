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

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            full_name varchar(255) NOT NULL,
            savat varchar(255),
            location varchar(50),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def add_user(self, id: int, name: str, savat: str = None, location: str=None):

        sql = """
        INSERT INTO Users(id, full_name, savat, location) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, savat, location), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def to_adding_box(self, savat, id):

        sql = f"""
        UPDATE Users SET savat=? WHERE id=?
        """
        return self.execute(sql, parameters=(savat, id), commit=True)

    def update_location(self,location,id):
        sql = f"""
                UPDATE Users SET location=? WHERE id=?
                """
        return self.execute(sql, parameters=(location, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def delete_user(self,id):
        sql = f"""
        DELETE FROM Users WHERE id=?
        """
        return self.execute(sql,(id,), commit=True)



    def create_table_categories(self):
            sql = """
            CREATE TABLE Categories (
                id int NOT NULL,
                category_name varchar(255) NOT NULL,
                PRIMARY KEY (id)
                );
    """
            self.execute(sql, commit=True)

    def add_category(self, id: int, name: str):
            sql = """
            INSERT INTO Categories(id, category_name) VALUES(?, ?)
            """
            self.execute(sql, parameters=(id, name), commit=True)

    def select_all_categories(self):
            sql = """
            SELECT * FROM Categories
            """
            return self.execute(sql, fetchall=True)

    def select_category(self, **kwargs):
        sql = "SELECT * FROM Categories WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def delete_categories(self):
        self.execute("DELETE FROM Categories WHERE TRUE", commit=True)

    def delete_category(self, id):
        sql = f"""
        DELETE FROM Categories WHERE id=?
        """
        return self.execute(sql, (id,), commit=True)




    def create_table_products(self):
        sql = """
        CREATE TABLE Products (
            photo_id varchar(255) NOT NULL,
            public_id int,
            category int,
            product_name varchar(255),
            coin int,
            PRIMARY KEY (photo_id)
            );
    """
        self.execute(sql, commit=True)

    def add_product(self, photo_id: str, public_id: int = 0, category: int = 0, product_name: str = None,coin: int = 0):
        sql = """
        INSERT INTO Products(photo_id, public_id, category, product_name, coin) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(photo_id, public_id, category, product_name, coin), commit=True)

    def select_all_products(self):
        sql = """
        SELECT * FROM Products
        """
        return self.execute(sql, fetchall=True)

    def select_product(self, **kwargs):
        sql = "SELECT * FROM Products WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_product(self):
        return self.execute("SELECT COUNT(*) FROM Products;", fetchone=True)

    def update_product_public_id(self, photo_id, public_id):
        sql = f"""
        UPDATE Products SET public_id=? WHERE photo_id=?
        """
        return self.execute(sql, parameters=(photo_id, public_id), commit=True)

    def update_product_name(self, photo_id, product_name):
        sql = f"""
        UPDATE Products SET product_name=? WHERE photo_id=?
        """
        return self.execute(sql, parameters=(photo_id, product_name), commit=True)

    def update_product_coin(self, photo_id, coin):
        sql = f"""
        UPDATE Products SET coin=? WHERE photo_id=?
        """
        return self.execute(sql, parameters=(photo_id, coin), commit=True)

    def delete_products(self):
        self.execute("DELETE FROM Products WHERE TRUE", commit=True)

    def delete_product(self, photo_id):
        sql = f"""
        DELETE FROM Products WHERE photo_id=?
        """
        return self.execute(sql, (photo_id,), commit=True)




def logger(statement):
    a=f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
"""
