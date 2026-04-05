import sqlite3
from . import db

STATUS_LOAN_AVAILABLE = "Disponible"
STATUS_LOAN_LOANED = "Prestado"
STATUS_LOAN_UNAVAILABLE = "No disponible"
STATUS = "Activo"
INACTIVE_REASON = ""


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
            print(e)

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
                    return False, f"El libro que intenta ingresar ISBN {isbn} ya se encuentra en la base de datos. \nUse el formulario de Edición para ajustar la cantidad de copias.", [
                    ]

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
                             STATUS_LOAN_AVAILABLE,
                             INACTIVE_REASON,
                             user_id))

                    connection.commit()

                    return True, "Libro ingresado exitosamente.", list_copy_code

        except sqlite3.Error as e:
            print(f"\n--- ERROR DE SQLITE EN ADD_BOOK: {e} ---")
            return False

    @classmethod
    def update_book(
            cls,
            book_id,
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
        Actualiza los datos de un libro existente en la base de datos
        Parametros:
        book_id(int) id del libro
        title(str) título del libro
        authors(str) nombre y apellido de los autores
        genre(str) género al que pertenece el libro
        isbn(int) isbn del libro
        publisher(str) editorial
        copies(str) cantidad de copias ingresadas
        status(str) estado inicial del libro en el inventario
        inactive_reason(str) motivo de inactividad del libro
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

                # Validacion previa a la actualizacion para verificar el estado de las copias del libro antes de intentar pasarlo a Inactivo.
                # Regla de integridad: un libro no puede estar inactivo si
                # tiene copias prestadas
                if status == "Inactivo":

                    # Cuenta la cantidad de copias prestadas
                    cursor.execute(
                        "SELECT * FROM copy WHERE book_id = ? AND status_loan = ?;",
                        (book_id,
                         STATUS_LOAN_LOANED))

                    loaned_copies = cursor.fetchall()

                    loaned_copies_number = len(loaned_copies)

                    if loaned_copies_number > 0:
                        return False, "No es posible inactivar un libro que posee copias prestadas. Revise el estado del libro que intenta actualizar o gestione las copias en la sección de Préstamos y Devoluciones.", []

                # Activar un libro que se encuentra Inactivo
                # Se consulta el estado actual del libro
                cursor.execute(
                    "SELECT status FROM book WHERE book_id = ?", (book_id,))

                row = cursor.fetchone()

                actual_status = row[0]

                if status == "Activo" and actual_status == "Inactivo":
                    # Automaticamente todas sus copias se ponen como
                    # "Disponible" y se limpia el valor de unavailable_reason
                    cursor.execute(
                        "UPDATE copy set status_loan = ?, unavailable_reason = ? WHERE book_id = ?",
                        (STATUS_LOAN_AVAILABLE,
                         inactive_reason,
                         book_id))

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

                # Insertar copias
                if copies < 0:
                    return False, "La cantidad de copias a añadir debe ser un número positivo o 0 si no desea añadir copias.", []

                elif copies >= 0:
                    # Buscar el último `copy_code` existente para este book_id
                    cursor.execute(
                        "SELECT copy_code FROM copy WHERE book_id = ?", (book_id,))
                    row = cursor.fetchall()
                    last_copy_code = row[-1][0]

                    # Extraer el índice
                    last_copy_code_split = last_copy_code.split('-')
                    count_base = last_copy_code_split[-1]
                    count_base_int = int(count_base)

                    # Añadir copias
                    for i in range(copies):
                        sum = count_base_int + i + 1
                        sum_str = str(sum)

                        new_copy_code = f"{isbn}-{sum_str}"

                        list_copy_code.append(new_copy_code)

                        cursor.execute(
                            "INSERT INTO copy (book_id, isbn, copy_code, status_loan, unavailable_reason, user_id) VALUES (?, ?, ?, ?, ?, ?)",
                            (book_id,
                             isbn,
                             new_copy_code,
                             STATUS_LOAN_AVAILABLE,
                             inactive_reason,
                             user_id))

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
                    "UPDATE book set isbn = ?, title = ?, publisher = ?, genre_id = ?, user_id = ?, status = ?, inactive_reason = ? WHERE book_id = ?",
                    (isbn,
                     title,
                     publisher,
                     genre_id,
                     user_id,
                     status,
                     inactive_reason,
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

                # Si el usuario quiere pasar el libro a estado inactivo,
                # automaticamente todas sus copias se ponen como "No
                # disponible"
                if status == "Inactivo":
                    cursor.execute(
                        "UPDATE copy set status_loan = ?, unavailable_reason = ? WHERE book_id = ?",
                        (STATUS_LOAN_UNAVAILABLE,
                         inactive_reason,
                         book_id))

                connection.commit()

                return True, "Libro actualizado correctamente", list_copy_code

        except sqlite3.Error as e:
            print(f"\n--- ERROR DE SQLITE EN UPDATE_BOOK: {e} ---")
            return False, f"\n--- ERROR DE SQLITE EN UPDATE_BOOK: {e} ---"

    def get_all_books():
        """
        Devuelve todos los libros registrado en la base de datos.
        No recibe parámetros.
        """

        try:
            with db.get_db_connection() as connection:

                cursor = connection.cursor()

                cursor.execute(
                    "SELECT book_id, isbn, title, publisher, genre_id, user_id, status FROM book")

                rows = cursor.fetchall()

                rows_complete = []

                if rows is not None:

                    for row in rows:

                        row = list(row)

                        # Extraer ID del género del libro
                        cursor.execute(
                            "SELECT genre_id FROM book WHERE book_id = ?;", (row[0], ))

                        genre_id = cursor.fetchone()

                        # Obtener nombre del género
                        cursor.execute(
                            "SELECT name FROM genre WHERE genre_id = ?;", (genre_id[0],))

                        genre_name = cursor.fetchone()

                        row[4] = genre_name[0]

                        rows_complete.append(row)

                        # Obtener ID del autor
                        cursor.execute(
                            "SELECT author_id FROM book_author WHERE book_id = ?;", (row[0],))

                        author_id = cursor.fetchone()

                        # Obtener nombre y apellido del autor
                        cursor.execute(
                            "SELECT first_name, last_name FROM author WHERE author_id = ?;", (author_id[0],))

                        author_name = cursor.fetchall()

                        author = author_name[0]

                        print(author)

                        author_complete = ""

                        for i in author:
                            author_complete = f"{author[0]} {author[1]}"

                        row.append(author_complete)

                        rows_complete.append(row)

                        print(rows_complete)

                return True, rows

        except sqlite3.Error as e:
            return False, str(e)
