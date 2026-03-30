import sqlite3
from models import db


class User():

    def __init__(self, user_id, first_name, last_name, email, password):
        self_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    @classmethod
    def check_user_by_email(cls, email):
        """
        Verifica si el usuario se encuentra en la base de datos utilizando su email
        Parametros:
        email(str) direccion de correo del usuario
        Retorna (1,0) si el usuario existe, de lo contrario devuelve None
        """

        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT 1 FROM user WHERE email = ?", (email, ))
                return cursor.fetchone()

        except sqlite3.Error as e:
            print(e)

    @classmethod
    def get_user_by_email(cls, email, event=None):
        """
        Obtiene los datos del usuario que coincide con el email registrado
        Parametros: email(str) direccion de correo del usuario
        Retorna una tupla con los datos del usuario si existe y None si no existe
        """

        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM user WHERE email = ?", (email, ))
                return cursor.fetchone()

        except sqlite3.Error as e:
            print(e)

    @classmethod
    def get_all_users(cls):
        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM user")
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(e)

    @classmethod
    def insert_user(cls, firstName, lastName, email, password):
        """
        Inserta los datos de un nuevo usuario en la base de datos
        Parametros:
        firstName(str) nombre del usuario
        lastName(str) apellido del usuario
        email(str) direccion de correo del usuario
        password(str) contraseña creada por el usuario
        """

        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO user (first_name, last_name, email, password) VALUES(?, ?, ?, ?)",
                    (firstName,
                     lastName,
                     email,
                     password))
                connection.commit()
        except sqlite3.Error as e:
            print(e)

    @classmethod
    def update_password(cls, email, new_password):
        """
        Actualiza la contraseña en la base de datos
        Parametros:
        email(str) direccion de correo del usuario
        new_password(str) nueva contraseña creada por el usuario
        """

        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE user SET password = ? WHERE email = ?", (new_password, email))
                connection.commit()
        except sqlite3.Error as e:
            print(e)
