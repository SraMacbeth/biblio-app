import re

try:
    from app.models.book_model import Book
except ModuleNotFoundError as e:
    from models.book_model import Book

# TODO: Reemplazar por el ID del usuario logueado cuando el sistema de
# login esté conectado
CURRENT_USER_ID = 1

STATUS = "Activo"
INACTIVE_REASON = "---"


def is_id_valid(book_id):
    """
    Valida el formato del ID ingresado por el usuario
    Parametros:
    book_id(int) ID del libro buscado
    Retorna True si el ID coincide con el patron establecido o False si no coincide
    """

    return bool(re.fullmatch(r'\d+', book_id))


def format_copy_codes(codes_list):

    formatted_list = ""

    for code in codes_list:
        formatted_list += f"\n• {code}"

    return formatted_list


def search_book_by_id(book_id):
    
    """
    Permite buscar un libro según su ID.
    """

    book_id = str(book_id)

    if book_id == "":
        return {
            "estado": "error",
            "mensaje": "El campo de búsqueda no puede estar vacío."}
    if not is_id_valid(book_id):
        return {
            "estado": "error",
            "mensaje": "El ID ingresado sólo puede contener números."}

    book = Book.get_book_by_id(book_id)

    if book is None:
        return {
            "estado": "error",
            "mensaje": "No existen libros registrados para el ID ingresado."}
    else:

        book_items, author_name, genre_name, copies_data = book

        id_book = book_items[0]

        title = book_items[2]

        author_firstname, author_lastname = author_name[0]

        genre = genre_name[0]

        isbn = book_items[1]

        publisher = book_items[3]

        status = book_items[6]
        
        inactive_reason = book_items[7]

        formatted_copies = []

        available_copies = 0

        for i in copies_data:
            copy_list = list(i)
            if copy_list[3] is None:
                copy_list[3] = "---"
            formatted_copies.append(copy_list)
            if i[2] == "Disponible":
                available_copies += 1

        total_copies = len(formatted_copies)
        book_details = [
            id_book,
            title,
            author_firstname,
            author_lastname,
            genre,
            isbn,
            publisher,
            status,
            inactive_reason,
            formatted_copies,
            total_copies,
            available_copies]

        return {
            "estado": "ok",
            "mensaje": "Libro encontrado",
            "detalles": book_details}


def validate_fields_form(data_to_validate):

        """
        Valida los datos ingresados por el usuario en los formularios de alta y edición de libro, asegurando que no se envíen al modelo datos vacíos o valores inválidos para las copias.
        Retorna diferentes mensajes en funcion de los casos.
        """
    
        if data_to_validate["title"] == "" or data_to_validate["authors"][0][0] == "" or data_to_validate["authors"][0][1] == "" or data_to_validate["genre"] == "" or data_to_validate["isbn"] == "" or data_to_validate["publisher"] == "":
            return {
                "estado": "error",
                "mensaje": "Los campos no pueden estar vacíos."}
            
        if data_to_validate["type_form"] == "new_book_form":
            if data_to_validate["copies"] == "":
                return {
                "estado": "error",
                "mensaje": "Los campos no pueden estar vacíos."}
 
            try:
                int_copies = int(data_to_validate["copies"])
                data_to_validate["copies"] = int_copies
            except ValueError:
                return {
                    "estado": "error",
                    "mensaje": "El campo copias solo acepta valores numéricos."}
 
            if int_copies <= 0:
                return {
                    "estado": "error",
                    "mensaje": "La cantidad de copias a añadir debe ser un número positivo."}
                
        return {
            "estado": "ok",
            "mensaje": "Campos validados correctamente."}


def add_book(title, authors, genre, isbn, publisher, copies):
    """
    Agrega un nuevo libro en la base de datos
    Parametros:
    title(str) título del libro
    authors(str) nombre y apellido de los autores
    genre(str) género al que pertenece el libro
    isbn(int) isbn del libro
    publisher(str) editorial
    copies(str) cantidad de copias ingresadas
    Retorna diferentes mensajes en funcion de los casos
    """
    
    success, message, copy_codes = Book.add_book(
        title, authors, genre, isbn, publisher, copies, status=STATUS, inactive_reason=INACTIVE_REASON, user_id=CURRENT_USER_ID)

    if not success:
        return {"estado": "error", "mensaje": message}
    else:
        if copy_codes:

            final_message = message

            header = "\n\nTome nota de los códigos de copia generados por el sistema:\n"

            formatted_list = format_copy_codes(copy_codes)

            final_message += header + formatted_list

        return {"estado": "ok", "mensaje": final_message}


def update_book(
        book_id,
        title,
        authors,
        genre,
        isbn,
        publisher,
        #status,
        #inactive_reason
        ):
    """
    actualiza un libro existente en la base de datos
    Parametros:
    book_id (int) identificador del libro
    title(str) título del libro
    authors(str) nombre y apellido de los autores
    genre(str) género al que pertenece el libro
    isbn(int) isbn del libro
    publisher(str) editorial
    copies(str) cantidad de copias ingresadas
    status (str) estado del libro en el inventario
    inactive_reason (str) motivo por el cual un libro no esta disponible para prestamo
    Retorna diferentes mensajes en funcion de los casos
    """
    success, message, copy_codes = Book.update_book(
        book_id, title, authors, genre, isbn, publisher, user_id=CURRENT_USER_ID)

    final_message = message

    if not success:
        return {"estado": "error", "mensaje": message}
    else:
        if copy_codes:

            final_message = message

            header = "\n\nTome nota de los códigos de copia generados por el sistema:\n"

            formatted_list = format_copy_codes(copy_codes)

            final_message += header + formatted_list

        return {"estado": "ok", "mensaje": final_message}


def check_data_changes(original_data, data_to_validate):
    
    if original_data == data_to_validate:
        return {"estado": "sin cambios", "mensaje": "No se detectaron cambios para actualizar."}
    else:
        return {"estado": "con cambios", "mensaje": "Se detectaron cambios para actualizar."}


def update_copies(book_id, isbn, book_status, copies_to_add):
    
    if copies_to_add == "":
        return { "estado": "error",
                "mensaje": "Los campos no pueden estar vacíos."}
    
    try:
        int_copies_to_add = int(copies_to_add)
    except ValueError:
        return {
            "estado": "error",
            "mensaje": "El campo 'Copias a añadir' solo acepta valores numéricos."}
    
    if int_copies_to_add < 0:
        return {"estado": "error",
                "mensaje": "La cantidad de copias a añadir debe ser un número positivo o 0 si no desea añadir copias."}
    
    if int_copies_to_add == 0:
        return {"estado": "ok",
                "mensaje": "No se detectaron cambios para actualizar."}
            
    success, message, copy_codes = Book.update_copies(book_id, isbn, book_status, int_copies_to_add)
    
    final_message = message

    if not success:
        return {"estado": "error", "mensaje": message}
    else:
        if copy_codes:

            final_message = message

            header = "\n\nTome nota de los códigos de copia generados por el sistema:\n"

            formatted_list = format_copy_codes(copy_codes)

            final_message += header + formatted_list

        return {"estado": "ok", "mensaje": final_message}
 
def update_copy(book_id, copy_id, status_loan, unavailable_reason):

    if status_loan == "" or unavailable_reason == "":
        return { "estado": "error",
                "mensaje": "Los campos no pueden estar vacíos."}
                
    if status_loan == "No disponible" and unavailable_reason == "---":
        return { "estado": "error",
                "mensaje": "Debe indicar un motivo de no disponibilidad para esta copia."}
    
    success, message = Book.update_copy(book_id, copy_id, status_loan, unavailable_reason)
    
    if not success:
        return {"estado": "error", "mensaje": message}
    else:
        return {"estado": "ok", "mensaje": message}

# def get_all_inventory():
    # """
    # Devuelve una lista con todos los libros del inventario.
    # No recibe parámetros
    # """
    # success, data = Book.get_all_books()

    # if not success:
        # return {"estado": "error"}
    # else:
        # list_book = []
        # for i in data:
            # i = list(i)
            # list_book.append(i)

        # return {"estado": "ok", "inventario": list_book}
