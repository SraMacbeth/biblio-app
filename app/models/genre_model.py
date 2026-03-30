import sqlite3
from . import db


class Genre():

    @classmethod
    def get_all_genres(cls):
        """
        Obtiene los géneros cargados en la base de datos.
        Retorna una tupla con los nombres de los géneros si hay o None si no hay
        """

        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM genre;")
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error en Genre.get_all_genres: {e}")
            return None
        finally:
            if connection:
                connection.close()
