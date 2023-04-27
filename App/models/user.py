from datetime import datetime
import mysql.connector

class User:
    def __init__(self, uid, username, password, email):
        self.uid = uid
        self.username = username
        self.password = password
        self.email = email

    # def to_dict(self):
    #     return {
    #         "uid": self.uid,
    #         "username": self.username,
    #         "password": self.password,
    #         "email": self.email,
    #     }

    # @classmethod
    # def from_dict(cls, data):
    #     return cls(
    #         uid=data.get("uid"),
    #         username=data.get("username"),
    #         password=data.get("password"),
    #         email=data.get("email"),
    #     )

        @property
        def uid(self):
            return self._uid

        @uid.setter
        def uid(self, new_uid):
            self._uid = new_uid

        @property
        def username(self):
            return self._username

        @username.setter
        def username(self, new_username):
            self._username = new_username

        @property
        def password(self):
            return self._password

        @password.setter
        def password(self, new_password):
            self._password = new_password
        
        @property
        def email(self):
            return self._email

        @email.setter
        def email(self, new_email):
            self._email = new_email
    
class UserDB:
    def __init__(self, db_conn, db_cursor):
        self.conn = db_conn
        self.cursor = db_cursor
        # self.create_table()

    # def create_table(self):
    #     self.cursor.execute("""
    #         CREATE TABLE IF NOT EXISTS users (
    #             username TEXT PRIMARY KEY,
    #             email TEXT NOT NULL,
    #             password TEXT NOT NULL
    #         );
    #     """)
        # self.conn.commit()

    def add_user(self, user):
        self.cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (user.username, user.email, user.password))
        self.conn.commit()

    def get_user_by_username(self, username):
        self.cursor.execute("""
            SELECT username, email, password FROM users WHERE username = ?
        """, (username,))
        user_data = self.cursor.fetchone()
        if user_data:
            return User(*user_data)
        else:
            return None

    def close(self):
        self.conn.close()