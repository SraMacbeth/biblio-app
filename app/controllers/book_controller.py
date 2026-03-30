import re

try:
	from app.models.book_model import Book, STATUS
except ModuleNotFoundError as e:
	from models.book_model import Book, STATUS

# TODO: Reemplazar por el ID del usuario logueado cuando el sistema de login esté conectado
CURRENT_USER_ID = 1

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
			
	if book_id == "":
		return {"estado": "error", "mensaje":"El campo de búsqueda no puede estar vacío."}
	if not is_id_valid(book_id):
		return {"estado": "error", "mensaje":"El ID ingresado sólo puede contener números."}
	
	book = Book.get_book_by_id(book_id)
	
	if book == None:
		return {"estado": "error", "mensaje":"No existen libros registrados para el ID ingresado."}
	else:
		
		book_items, author_name, genre_name, copies_data = book
						
		id_book = book_items[0]
		
		title = book_items[2]
				
		author_firstname, author_lastname = author_name[0]
		
		genre = genre_name[0]
		
		isbn = book_items[1]
		
		publisher = book_items[3]
		
		status = book_items[6]
		
		formatted_copies = []

		available_copies = 0

		for i in copies_data:
			copy_list = list(i)
			if copy_list[3] == None:
				copy_list[3] = "---"
			formatted_copies.append(copy_list)
			if i[2] == "Disponible":
				available_copies += 1
				
		total_copies = len(formatted_copies)			
		book_details = [id_book, title,author_firstname, author_lastname, genre, isbn, publisher, status, formatted_copies, total_copies, available_copies]
				
		return {"estado": "ok", "mensaje":"Libro encontrado", "detalles" : book_details} 

def add_book(title, authors, genre, isbn, publisher, copies):
	
	"""
	agrega un nuevo libro en la base de datos
	Parametros: 
	isbn(int) isbn del libro
	title(str) título del libro
	authors(str) nombre y apellido de los autores
	publisher(str) editorial
	genre(str) género al que pertenece el libro
	user_id(int) id del usuario que ingresó el libro
	copies(str) cantidad de copias ingresadas
	Retorna diferentes mensajes en funcion de los casos
	"""	
	
	if title == "" or authors[0][0] == "" or authors[0][1] == "" or genre == "" or isbn == "" or publisher == "" or copies == "":
		return {"estado": "error", "mensaje":"Los campos no pueden estar vacíos."}

	try:
		int_copies = int(copies)
	except ValueError:
		return {"estado": "error", "mensaje":"El campo copias solo acepta valores numéricos."}

	if int_copies <= 0:
		return {"estado": "error", "mensaje":"El libro ingresado debe tener al menos una copia."}

	success, message, copy_codes = Book.add_book(title, authors, genre, isbn, publisher, int_copies, status=STATUS,user_id=CURRENT_USER_ID)
	
	if success == False:
		return {"estado": "error", "mensaje": message}
	else:
		if copy_codes:

			final_message = message 
			
			header = "\n\nTome nota de los códigos de copia generados por el sistema:\n"
			
			formatted_list = format_copy_codes(copy_codes)

			final_message += header + formatted_list
		
		return {"estado": "ok", "mensaje": final_message}

def update_book(book_id, title, authors, genre, isbn, publisher, copies, status, unavailable_reason):

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
	unavailable_reason (str) motivo por el cual un libro no esta disponible para prestamo
	user_id(int) id del usuario que ingresó el libro
	Retorna diferentes mensajes en funcion de los casos
	"""

	if title == "" or authors[0][0] == "" or authors[0][1] == "" or genre == "" or isbn == "" or publisher == "" or copies == "" or status == "":
		return {"estado": "error", "mensaje":"Los campos no pueden estar vacíos"}
	
	try:
		int_copies = int(copies)
	except ValueError:
		return {"estado": "error", "mensaje":"El campo copias solo acepta valores numéricos."}

	if int_copies < 0:
		return {"estado": "error", "mensaje":"La cantidad de copias a añadir debe ser un número positivo o 0 si no desea añadir copias."}

	if not unavailable_reason or unavailable_reason.strip() == "":
		unavailable_reason = "---"

	success, message, copy_codes = Book.update_book(book_id, title, authors, genre, isbn, publisher, int_copies, status, unavailable_reason, user_id=CURRENT_USER_ID)

	final_message = message
	
	if success == False:
		return {"estado": "error", "mensaje": message}
	else:
		if copy_codes:

			final_message = message 
			
			header = "\n\nTome nota de los códigos de copia generados por el sistema:\n"
			
			formatted_list = format_copy_codes(copy_codes)

			final_message += header + formatted_list
		
		return {"estado": "ok", "mensaje": final_message}

def advertise_change_status(selected_status):
    
    """
    Muestra los mensajes informativos al seleccionar un nuevo estado que explican consecuencias y alternativas de gestión individual
    """
    return {"estado": "ok", "mensaje": f"Ha seleccionado '{selected_status}'. \nTenga en cuenta que al guardar, esto afectará a todas las copias del libro actual. \nSi solo quiere modificar algunas, use 'Gestionar Copias' antes de finalizar."}

def get_all_inventory():
	
	"""
	Devuelve una lista con todos los libros del inventario.
	No recibe parámetros
	"""
	success, data = Book.get_all_books()

	if success == False:
		return {"estado": "error"}
	else:
		list_book = []
		for i in data:
			i = list(i)
			list_book.append(i)

		return {"estado": "ok", "inventario": list_book}


	
	
