import os
import sqlite3

""" Archivo de configuración de la base de datos de prueba.
Asegura que todas las pruebas se ejecuten en una base de datos temporal y limpia. """

# Obtener la ruta de la carpeta donde está este archivo (tests/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Subir un nivel y entrar en test_data/
TEST_DB = os.path.join(BASE_DIR, "..", "test_data", "test_library.db")


def get_test_connection():
    """ Retorna una conexión a la base de datos de prueba """
    return sqlite3.connect(TEST_DB)


def create_tables():
    """ Crea las tablas necesarias en la base de datos de prueba. """
    # Crear 'test_data' si no existe
    os.makedirs(os.path.dirname(TEST_DB), exist_ok=True)
    connection = get_test_connection()
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS user (user_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS author (author_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL);")

    cursor.execute("CREATE TABLE IF NOT EXISTS member (member_id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, address TEXT NOT NULL, email TEXT NOT NULL, phone_number TEXT NOT NULL);")

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS genre (genre_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);")

    cursor.execute("SELECT COUNT(*) FROM genre")
    count = cursor.fetchone()[0]

    if count == 0:

        GENRES_TO_LOAD = [
            # GÉNEROS DE NOVELA (Ficción)
            ("Fantasía",),
            ("Ciencia Ficción",),
            ("Cyberpunk",),
            ("Distopía",),
            ("Misterio",),
            ("Novela Psicológica",),
            ("Novela Negra / Policial",),
            ("Romance Histórico",),
            ("Romance Contemporáneo",),
            ("Terror",),
            ("Ficción Histórica",),
            ("Ficción Contemporánea",),
            ("Ficción Juvenil",),
            ("Aventura",),
            ("Western",),
            ("Sátira / Humor",),

            # NO FICCIÓN: CIENCIAS Y DISCIPLINAS
            ("Biografía / Autobiografía",),
            ("Ensayo",),
            ("Memoria",),
            ("Historia Antigua",),
            ("Historia Moderna",),
            ("Filosofía",),
            ("Psicología",),
            ("Sociología",),
            ("Economía",),
            ("Biología",),
            ("Física",),
            ("Matemáticas",),
            ("Medicina",),
            ("Divulgación científica",),
            ("Autoayuda / Desarrollo Personal",),
            ("Política",),
            ("Referencia (Diccionarios, etc.)",),

            # OTROS
            ("Poesía",),
            ("Teatro",),
            ("Cómic / Novela Gráfica",),
            ("Cuento Infantil",),
            ("Novela Infantil",),
            ("Viajes",),
            ("Crónicas",),
            ("Cocina / Gastronomía",),
            ("Arte",),
            ("Fotografía",),
            ("Tecnología",)
        ]

        insert_query = "INSERT INTO genre (name) VALUES (?)"
        cursor.executemany(insert_query, GENRES_TO_LOAD)

        cursor.execute("CREATE TABLE IF NOT EXISTS book (book_id INTEGER PRIMARY KEY, isbn TEXT NOT NULL, title TEXT NOT NULL, publisher TEXT NOT NULL, genre_id INTEGER NOT NULL, user_id INTEGER NOT NULL, status TEXT NOT NULL, inactive_reason TEXT NOT NULL, FOREIGN KEY (genre_id) REFERENCES genre(genre_id), FOREIGN KEY (user_id) REFERENCES user(user_id));")

        cursor.execute("CREATE TABLE IF NOT EXISTS book_author (book_id INTEGER, author_id INTEGER, FOREIGN KEY (book_id) REFERENCES book(book_id), FOREIGN KEY (author_id) REFERENCES author(author_id));")

        cursor.execute("CREATE TABLE IF NOT EXISTS book_genre (book_id INTEGER, genre_id INTEGER, FOREIGN KEY (book_id) REFERENCES book(book_id), FOREIGN KEY (genre_id) REFERENCES genre(genre_id));")

        cursor.execute("CREATE TABLE IF NOT EXISTS copy (copy_id INTEGER PRIMARY KEY, book_id INTEGER, isbn TEXT NOT NULL, copy_code TEXT UNIQUE NOT NULL,status_loan TEXT NOT NULL, unavailable_reason TEXT NOT NULL, user_id INTEGER, FOREIGN KEY (book_id) REFERENCES book(book_id), FOREIGN KEY (user_id) REFERENCES user(user_id));")

        cursor.execute("CREATE TABLE IF NOT EXISTS loan (loan_id INTEGER PRIMARY KEY, member_id INTEGER, copy_id INTEGER, loan_date DATE NOT NULL, due_date DATE NOT NULL, return_date DATE NOT NULL, user_id INTEGER, FOREIGN KEY (member_id) REFERENCES member(member_id), FOREIGN KEY (copy_id) REFERENCES copy(copy_id), FOREIGN KEY (user_id) REFERENCES user(user_id));")

        connection.commit()
        connection.close()


def clear_tables():
    """ Borra el contenido de las tablas antes de cada test. """
    connection = get_test_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM user;")
    cursor.execute("DELETE FROM author;")
    cursor.execute("DELETE FROM member;")
    # cursor.execute("DELETE FROM genre;")
    cursor.execute("DELETE FROM book;")
    cursor.execute("DELETE FROM book_author;")
    cursor.execute("DELETE FROM book_genre;")
    cursor.execute("DELETE FROM copy;")
    cursor.execute("DELETE FROM loan;")

    connection.commit()
    connection.close()


def drop_database():
    """ Elimina el archivo de base de datos de prueba al finalizar. """
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
