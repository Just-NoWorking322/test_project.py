import sqlite3

class DatabaseManager:
     def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()  

     def create_tables(self):
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            );
        """)
        
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                vip_status TEXT
            );
        """)
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                work_class TEXT
            );
        """)

     def execute_query(self, query, params=()):
        self.cursor.execute(query, params)

     def close_conn(self):
        if self.connection:
            self.connection.close()

     def find_name(self, name):
        self.cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        return self.cursor.fetchone()

     def transaction(self, users):
        try:
            for name, email in users:
                self.execute_query("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            self.connection.commit() 
        except sqlite3.Error as error:
            self.connection.backup()
            print(f"Ошибка выполнения трансанкции: {error}")


class User(DatabaseManager):
    def __init__(self, db_name):
        super().__init__(db_name)

    def add_user(self, name, email):
        self.execute_query("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return self.cursor.fetchone()

    def delete_user(self, user_id):
        self.execute_query("DELETE FROM users WHERE id = ?", (user_id,))


class Admin(User):
    def __init__(self, db_name):
        super().__init__(db_name)

    def add_admin(self, name, vip_status):
        self.execute_query("INSERT INTO admins (name, vip_status) VALUES (?, ?)", (name, vip_status))


class Customer(User):
    def __init__(self, db_name):
        super().__init__(db_name)

    def add_customer(self, name, work_class):
        self.execute_query("INSERT INTO customers (name, work_class) VALUES (?, ?)", (name, work_class))


db_manager = DatabaseManager('useros.db')

users = [
    ('User1', 'user1@example.com'),
    ('User2', 'user2@example.com'),
    ('User3', 'user3@example.com')
]

db_manager.transaction(users)

user_data = db_manager.find_name('User1')
user_data1 = db_manager.find_name('User2')
user_data2 = db_manager.find_name('User3')

print(user_data,user_data1,user_data2)

db_manager.close_conn()

        
        
        
        
        
        
        
        
        
"""1. Создание класса для работы с базой данных

Напишите класс DatabaseManager, который будет использовать SQLite3 для подключения к базе данных. Реализуйте методы для открытия и закрытия соединения.
2. Класс для управления таблицей

Создайте класс User, который будет управлять таблицей users в SQLite3. Реализуйте методы для добавления нового пользователя, получения пользователя по ID и удаления пользователя.
3. Наследование и работа с несколькими таблицами

Реализуйте классы Admin и Customer, которые будут наследовать от класса User. Добавьте дополнительные поля для каждой роли и методы для работы с соответствующими таблицами admins и customers.
4. Поиск данных в базе

Напишите метод в классе DatabaseManager, который будет принимать имя пользователя и возвращать его данные из таблицы users. Используйте SQL-запросы для поиска данных.
5. Работа с транзакциями

Добавьте в класс DatabaseManager метод, который будет выполнять несколько операций с базой данных в одной транзакции. Реализуйте простую логику для добавления нескольких записей в таблицу и откат транзакции в случае ошибки.
"""