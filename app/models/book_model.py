import sqlite3
from . import db

CURRENT_USER_ID = 1

class Book():

    def __init__(
            self,
            book_id,
            isbn,
            title,
            publisher,
            genre_id,
            user_id,
            status,
            inactive_reason,
            copies=0):
        self.book_id = book_id
        self.isbn = isbn
        self.title = title
        self.publisher = publisher
        self.genre_id = genre_id
        self.user_id = user_id
        self.status = status
        self.inactive_reason = inactive_reason
        self.copies = copies

    @classmethod
    def get_book_by_id(cls, book_id):
        """
        Obtiene los datos del libro que coincide con el id ingresado
        Parametros: book_id(int) id del libro
        Retorna una tupla con los datos del libro si existe o None si no existe
        """

        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()

                # Obtener datos del libro segun su ID
                cursor.execute(
                    "SELECT book_id, isbn, title, publisher, genre_id, user_id, status, inactive_reason FROM book WHERE book_id = ?;",
                    (book_id,
                     ))

                book = cursor.fetchone()

                if book is not None:

                    # Extraer ID del género del libro
                    cursor.execute(
                        "SELECT genre_id FROM book WHERE book_id = ?;", (book_id, ))

                    genre_id = cursor.fetchone()

                    # Obtener nombre del género
                    cursor.execute(
                        "SELECT name FROM genre WHERE genre_id = ?;", (genre_id[0],))

                    genre_name = cursor.fetchone()

                    # Obtener ID del autor
                    cursor.execute(
                        "SELECT author_id FROM book_author WHERE book_id = ?;", (book_id,))

                    author_id = cursor.fetchone()

                    # Obtener nombre y apellido del autor
                    cursor.execute(
                        "SELECT first_name, last_name FROM author WHERE author_id = ?;", (author_id[0],))

                    author_name = cursor.fetchall()

                    # Obtener cantidad de copias
                    cursor.execute(
                        "SELECT copy_id, copy_code, status_loan, unavailable_reason FROM copy WHERE book_id = ?;",
                        (book_id,
                         ))

                    copies = cursor.fetchall()

                    return book, author_name, genre_name, copies

                else:
                    return book

        except sqlite3.Error as e:
            #print(e)
            return False, str(e)

    @classmethod
    def add_book(
            cls,
            title,
            authors,
            genre,
            isbn,
            publisher,
            copies,
            status,
            inactive_reason,
            user_id):
        """
        Inserta los datos de un nuevo libro en la base de datos
        Parametros:
        isbn(int) isbn del libro
        title(str) título del libro
        authors(str) nombre y apellido de los autores
        publisher(str) editorial
        genre(str) género al que pertenece el libro
        user_id(int) id del usuario que ingresó el libro
        copies(str) cantidad de copias ingresadas
        status(str) estado del libro en el inventario
        inactive_reason(str) motivo de inactivacion del libro
        """

        try:

            if copies <= 0:
                return False, "El libro ingresado debe tener al menos una copia.", []

            with db.get_db_connection() as connection:
                cursor = connection.cursor()

                # Verificar si el libro existe en la base de datos
                cursor.execute("SELECT * FROM book WHERE isbn = ?", (isbn,))

                if cursor.fetchone():
                    return False, f"El libro que intenta ingresar ISBN {isbn} ya se encuentra en la base de datos. \nUse el formulario de Edición para ajustar la cantidad de copias.", []

                else:

                    # Extraer genre_id o ingresar un nuevo género si no existe
                    cursor.execute(
                        "SELECT genre_id FROM genre WHERE name = ?", (genre,))

                    row = cursor.fetchone()

                    if row:
                        genre_id = row[0]
                    else:
                        cursor.execute(
                            "INSERT INTO genre (name) VALUES (?)", (genre,))
                        genre_id = cursor.lastrowid

                    # Insertar libro
                    cursor.execute(
                        "INSERT INTO book (isbn, title, publisher, genre_id, user_id, status, inactive_reason) VALUES(?, ?, ?, ?, ?, ?, ?);",
                        (isbn,
                         title,
                         publisher,
                         genre_id,
                         user_id,
                         status,
                         inactive_reason))
                    book_id = cursor.lastrowid

                    # Verificar / insertar autores y asociar tablas
                    for first_name, last_name in authors:
                        cursor.execute(
                            "SELECT author_id FROM author WHERE first_name = ? AND last_name = ?",
                            (first_name,
                             last_name))

                        row = cursor.fetchone()

                        if row:
                            author_id = row[0]
                        else:
                            cursor.execute(
                                "INSERT INTO author (first_name, last_name) VALUES (?, ?)",
                                (first_name,
                                 last_name))
                            author_id = cursor.lastrowid

                        cursor.execute(
                            "INSERT INTO book_author (book_id, author_id) VALUES (?, ?)",
                            (book_id,
                             author_id))

                    # Lista para guardar los copy_code que se mostrarán al
                    # usuario
                    list_copy_code = []

                    # Insertar copias
                    for i in range(copies):

                        copy_code = f"{isbn}-{i+1}"

                        list_copy_code.append(copy_code)

                        cursor.execute(
                            "INSERT INTO copy (book_id, isbn, copy_code, status_loan, unavailable_reason, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                            (book_id,
                             isbn,
                             copy_code,
                             "Disponible",
                             "---",
                             user_id))

                    connection.commit()

                    return True, "Libro ingresado exitosamente.", list_copy_code

        except sqlite3.Error as e:
            #print(f"\n--- ERROR DE SQLITE EN ADD_BOOK: {e} ---")
            return False, str(e)

    @classmethod
    def update_book(
            cls,
            book_id,
            title,
            authors,
            genre,
            isbn,
            publisher,
            user_id):
        """
        Actualiza los datos de un libro existente en la base de datos
        Parametros:
        book_id(int) id del libro
        title(str) título del libro
        authors(str) nombre y apellido de los autores
        genre(str) género al que pertenece el libro
        isbn(int) isbn del libro
        publisher(str) editorial
        user_id(int) id del usuario que ingresó el libro
        """

        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()

                # Validacion previa a la actualizacion para verificar que no se
                # edite el libro si el ISBN ingresando pertenece a otro libro.

                cursor.execute(
                    "SELECT * FROM book WHERE isbn = ? AND book_id != ?", (isbn, book_id))

                row = cursor.fetchone()

                if row:
                    return False, "El ISBN ingresado ya pertenece a otro libro.", []

                # Lista para guardar los copy_code que se mostrarán al usuario
                list_copy_code = []

                # Actualizar codigo de copias si cambia el isbn

                # Se captura el ISBN actual
                cursor.execute(
                    "SELECT isbn FROM book WHERE book_id = ?", (book_id,))
                row = cursor.fetchone()
                actual_isbn = row[0]

                if actual_isbn != isbn:

                    cursor.execute(
                        "SELECT copy_id, copy_code FROM copy WHERE book_id = ?", (book_id,))
                    row = cursor.fetchall()

                    for i in row:
                        id_copy = i[0]
                        # Extraemos el número del código actual (ej: de '123-2'
                        # extrae '2')
                        actual_index = i[1].split("-")[-1]

                        # Creamos el nuevo código con el ISBN actualizado
                        new_code = f"{isbn}-{actual_index}"

                        list_copy_code.append(new_code)

                        # Actualizamos usando el ID único de la copia
                        cursor.execute(
                            "UPDATE copy SET copy_code = ? WHERE copy_id = ?", (new_code, id_copy))

                        connection.commit()

                # Extraer genre_id o ingresar un nuevo género si no existe
                cursor.execute(
                    "SELECT genre_id FROM genre WHERE name = ?", (genre,))

                row = cursor.fetchone()

                if row:
                    genre_id = row[0]
                else:
                    cursor.execute(
                        "INSERT INTO genre (name) VALUES (?)", (genre,))
                    genre_id = cursor.lastrowid

                # Actualizar libro con los datos proporcionados
                cursor.execute(
                    "UPDATE book set isbn = ?, title = ?, publisher = ?, genre_id = ?, user_id = ? WHERE book_id = ?",
                    (isbn,
                     title,
                     publisher,
                     genre_id,
                     user_id,
                     book_id))

                # Resetear las asociaciones de libro-autor en la tabla
                # intermedia book_author antes de poner las nuevas
                cursor.execute(
                    "DELETE FROM book_author WHERE book_id = ?", (book_id,))

                # Insertar nuevos autores y asociar tablas
                for first_name, last_name in authors:
                    cursor.execute(
                        "SELECT author_id FROM author WHERE first_name = ? AND last_name = ?",
                        (first_name,
                         last_name))

                    row = cursor.fetchone()

                    if row:
                        author_id = row[0]
                    else:
                        cursor.execute(
                            "INSERT INTO author (first_name, last_name) VALUES (?, ?)",
                            (first_name,
                             last_name))
                        author_id = cursor.lastrowid

                    cursor.execute(
                        "INSERT INTO book_author (book_id, author_id) VALUES (?, ?)",
                        (book_id,
                         author_id))

                connection.commit()

                return True, "Libro actualizado correctamente", list_copy_code

        except sqlite3.Error as e:
            #print(f"\n--- ERROR DE SQLITE EN UPDATE_BOOK: {e} ---")
            return False,  f"\n--- ERROR DE SQLITE EN UPDATE_BOOK: {e} ---"

    @classmethod    
    def update_copies(cls, book_id, isbn, book_status, copies_to_add):
           
        """
        Añade cipos nuevas a un libro existente.
        Parametros:
        book_id(int) id del libro
        isbn(int) isbn del libro
        book_status(str) estado actual del libro
        copies_to_add(int) cantidad de copias a añadir
        """
        
        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()
        
            # Insertar copias
            if copies_to_add < 0:
                return False, "La cantidad de copias a añadir debe ser un número positivo o 0 si no desea añadir copias.", []

            if copies_to_add > 0:
                # Buscar el último `copy_code` existente para este book_id
                cursor.execute("SELECT copy_code FROM copy WHERE book_id = ?", (book_id,))
                row = cursor.fetchall()
                last_copy_code = row[-1][0]

                # Extraer el índice
                last_copy_code_split = last_copy_code.split('-')
                count_base = last_copy_code_split[-1]
                count_base_int = int(count_base)
                
                list_copy_code = []

                # Añadir copias
                for i in range(copies_to_add):
                    sum = count_base_int + i + 1
                    sum_str = str(sum)

                    new_copy_code = f"{isbn}-{sum_str}"

                    list_copy_code.append(new_copy_code)

                    cursor.execute(
                        "INSERT INTO copy (book_id, isbn, copy_code, status_loan, unavailable_reason, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                        (book_id,
                        isbn,
                        new_copy_code,
                        "Disponible",
                        "---",
                        CURRENT_USER_ID))
                
                if book_status == "Inactivo":
                    cursor.execute(
                    "UPDATE book set status = ?, inactive_reason = ? WHERE book_id = ?",
                    ("Activo",
                    "---",
                    book_id))

            connection.commit()
        
            return True, "Copias añadidas correctamente.", list_copy_code

        except sqlite3.Error as e:
            return False, str(e)

    @classmethod    
    def update_copy(cls, book_id, copy_id, status_loan, unavailable_reason):
                
        """
        Actualiza una copia individual de un libro.
        Parametros:
        book_id(int) id del libro
        copy_id(int) id de la copia
        status_loan(str) estado para préstamo de la copia
        unavailable_reason(str) motivo de no disponibilidad de la copia
        """    
        
        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()
                
                # Actualizar la copia con los nuevos datos
                cursor.execute(
                    "UPDATE copy set status_loan = ?, unavailable_reason = ? WHERE copy_id = ?",
                    (status_loan,
                    unavailable_reason,
                    copy_id))
                                        
                # Si hay, al menos, una copia con estado "Disponible" o "No disponible" pero con unavailable_reason "Prestado", el libro debe tener estado "Activo".
                
                # Obtener la cantidad de copias que determinan la condición de libro vivo.
                cursor.execute(
                        "SELECT COUNT (*) FROM copy WHERE book_id = ? AND (status_loan = ? OR unavailable_reason = ?)",
                        (book_id,
                        "Disponible",
                        "Prestado"))
                        
                copies_active_book = cursor.fetchone()[0]
     
                if copies_active_book:
                    
                    cursor.execute(
                        "UPDATE book set status = ?, inactive_reason = ? WHERE book_id = ?",
                        ("Activo",
                        "---",
                        book_id))
                
                else:
                    
                    cursor.execute(
                        "UPDATE book set status = ?, inactive_reason = ? WHERE book_id = ?",
                        ("Inactivo",
                        "Sin copias operativas",
                        book_id))
                    
            connection.commit()
        
            return True, "Copia actualizada correctamente."

        except sqlite3.Error as e:
            return False, str(e)

    @classmethod
    def get_all_books(cls):
        """
        Devuelve todos los libros registrados en la base de datos.
        No recibe parámetros.
        """

        try:
            with db.get_db_connection() as connection:

                cursor = connection.cursor()

                cursor.execute(
                    "SELECT book_id, isbn, title, publisher, status FROM book")

                rows = cursor.fetchall()

                rows_complete = []

                if rows == None:
                    return False, "No hay libros en el inventario", []
                
                if rows is not None:

                    for row in rows:

                        row = list(row)

                        # Obtener ID del autor
                        cursor.execute(
                            "SELECT author_id FROM book_author WHERE book_id = ?;", (row[0],))

                        author_id = cursor.fetchone()

                        # Obtener nombre y apellido del autor
                        cursor.execute(
                            "SELECT first_name, last_name FROM author WHERE author_id = ?;", (author_id[0],))

                        author_name = cursor.fetchall()

                        author = author_name[0]

                        author_complete = ""

                        for i in author:
                            author_complete = f"{author[0]} {author[1]}"

                        row.append(author_complete)

                        rows_complete.append(row)

                return True, "Inventario cargado con éxito", rows_complete

        except sqlite3.Error as e:
            return False, str(e)
