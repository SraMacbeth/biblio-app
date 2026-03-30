from app.controllers import book_controller
from . import test_db_setup
import unittest
import os
os.environ['TESTING'] = 'True'


# Se definen constantes para los tests
STATUS_LOAN_AVAILABLE = "Disponible"
STATUS_LOAN_LOANED = "Prestado"
STATUS_LOAN_UNAVAILABLE = "No disponible"
STATUS = "Activo"
TEST_ISBN = "9789500739718"
TEST_USER_ID = 1


class TestBookController(unittest.TestCase):

    # --- Configuración del entorno de prueba ---

    @classmethod
    def setUpClass(cls):
        """ Se ejecuta una vez: Crea las tablas de la DB de prueba. """
        test_db_setup.create_tables()

    def setUp(self):
        """ Se ejecuta antes de cada test. """
        # Limpiar datos de tests anteriores pero mantener las tablas
        test_db_setup.clear_tables()

        # Insertar el usuario obligatorio para que la Foreign Key no falle
        conn = test_db_setup.get_test_connection()

        db_name = conn.execute("PRAGMA database_list").fetchall()[0][2]
        if "test_library.db" not in db_name:
            self.fail(f"¡PELIGRO! El test intentó conectarse a: {db_name}")

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user (user_id, first_name, last_name, email, password) VALUES (?, ?, ?, ?, ?)",
            (TEST_USER_ID, "Admin", "Test", "admin@test.com", "1234")
        )
        conn.commit()
        conn.close()

    @classmethod
    def tearDownClass(cls):
        """Se ejecuta una vez después de TODAS las pruebas. Borra el archivo DB."""
        # Puedes comentar esta línea si quieres inspeccionar el archivo DB de prueba después de correr los tests
        # test_db_setup.drop_database()
        pass

    def test_estructura_de_busqueda(self):
        ''' Verifica que search_book_by_id devuelva un diccionario donde detalles[8] es efectivamente una lista de tuplas con las copias.'''

        # PREPARACIÓN:
        # Insertar un libro manualmente para tener algo que buscar

        datos_libro = [
            "Rayuela", [
                ("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1]

        book_controller.add_book(*datos_libro)

        # Buscar el ID en la DB por el ISBN del libro
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = str(row[0])
        conn.close()

        # Obtener la lista de copias del libro de manera manual para comparar
        # su estructura
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT copy_id, copy_code, status_loan, unavailable_reason FROM copy WHERE book_id = ?;",
            (generated_id,
             ))
        copy_tuple = cursor.fetchall()
        conn.commit()

        copy_list = []
        for i in copy_tuple:
            list_i = list(i)
            if list_i[3] is None:
                list_i[3] = "---"
            copy_list.append(list_i)

        # Act
        book = book_controller.search_book_by_id(generated_id)

        # Assert
        self.assertEqual(
            book['detalles'][8],
            copy_list,
            "La estructura de datos devuelta no es la esperada.")

    def test_inyeccion_de_usuario(self):
        '''Comprueba que al llamar a add_book desde el controlador, no se necesita pasar el ID de usuario, pero que en la base de datos el registro aparece con el ID 1 (CURRENT_USER_ID)'''

        # PREPARACIÓN:
        # Datos del libro que se pasan al controlador y no incluyen el ID del
        # usuario
        datos_libro = [
            "Rayuela", [
                ("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1]

        # Act
        exito = book_controller.add_book(*datos_libro)

        # Buscar el ID del libro en la DB por su ISBN
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = str(row[0])
        conn.close()

        # Obtención del ID del usuario asignado en la DB
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id FROM book WHERE book_id = ?;", (generated_id,))
        row = cursor.fetchone()
        user_id_in_db = row[0]
        conn.commit()

        # Assert
        self.assertEqual(
            user_id_in_db,
            book_controller.CURRENT_USER_ID,
            "El ID de usuario no coincide")

    def test_validar_copia_mayor_a_cero(self):
        '''
        Verifica que si se envía un 0 en el número de copias al agregar un libro, el controlador devuelve el mensaje de error esperado.
        '''

        # PREPARACIÓN:
        # Insertar un libro con 0 copias manualmente
        datos_libro = [
            "Rayuela", [
                ("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 0]

        # Act
        exito = book_controller.add_book(*datos_libro)

        # Assert
        self.assertEqual(exito["estado"], "error")
        self.assertEqual(
            exito["mensaje"],
            "El libro ingresado debe tener al menos una copia.")

    def test_de_duplicado_en_alta(self):
        """
        Verifica si el ISBN ingresado por el usuario al añadir un libro ya existe en la base de datos y muestra el mensaje de error correspondiente.
        """
        # PREPARACIÓN:
        # Insertar un libro
        datos_primer_libro = [
            "Rayuela", [
                ("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1]
        book_controller.add_book(*datos_primer_libro)

        # Insertar un segundo libro repitiendo el ISBN del primero
        datos_segundo_libro = ["Las venas abiertas de América Latina", [
            ("Eduardo", "Galeano")], "Ensayo", "978-1", "Siglo XXI Editores", 1]

        # Act
        exito = book_controller.add_book(*datos_segundo_libro)

        # Assert
        self.assertEqual(exito["estado"], "error")
        self.assertEqual(
            exito["mensaje"],
            "El libro que intenta ingresar ISBN 978-1 ya se encuentra en la base de datos. \nUse el formulario de Edición para ajustar la cantidad de copias.")

    def test_de_duplicado_en_edicion(self):
        """
        Verifica si el nuevo ISBN ingresado por el usuario al editar un libro ya existe en la base de datos y muestra el mensaje de error correspondiente.
        """
        # PREPARACIÓN:
        # Insertar el primer libro
        datos_primer_libro = [
            "Rayuela", [
                ("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1]
        book_controller.add_book(*datos_primer_libro)

        # Insertar el segundo libro
        datos_segundo_libro = ["Las venas abiertas de América Latina", [
            ("Eduardo", "Galeano")], "Ensayo", "999-2", "Siglo XXI Editores", 1]
        book_controller.add_book(*datos_segundo_libro)

        # Buscar el ID del segundo libro en la DB por su ISBN
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("999-2",))
        row = cursor.fetchone()
        generated_id = str(row[0])
        conn.close()

        # Act - Intentar editar el segundo libro poniéndole el ISBN del primero
        nuevos_datos_segundo_libro = [generated_id, "Las venas abiertas de América Latina", [
            ("Eduardo", "Galeano")], "Ensayo", "978-1", "Siglo XXI Editores", 1, STATUS, None]
        exito = book_controller.update_book(*nuevos_datos_segundo_libro)

        # Assert
        self.assertEqual(exito["estado"], "error")
        self.assertEqual(
            exito["mensaje"],
            "El ISBN ingresado ya pertenece a otro libro.")

    def test_traer_todo_el_inventario(self):
        """
        Verifica que la función de búsqueda global devuelve todos los libros cargados en la base de datos en el formato correcto para ser mostrados en la vista.
        """

        # PREPARACIÓN:
        # Insertar un libro
        datos_primer_libro = [
            "Rayuela", [
                ("Julio", "Cortázar")], "Ficción Contemporánea", "978-1", "Alfaguara", 1]
        book_controller.add_book(*datos_primer_libro)

        # Insertar un segundo libro
        datos_segundo_libro = ["Las venas abiertas de América Latina", [
            ("Eduardo", "Galeano")], "Ensayo", "923-4", "Siglo XXI Editores", 1]
        book_controller.add_book(*datos_segundo_libro)

        # Act
        exito = book_controller.get_all_inventory()

        # Assert
        self.assertEqual(exito['estado'], "ok", "La operación falló")
        self.assertEqual(
            len(exito['inventario']), 2, "El tamaño de la lista de libros no es el esperado")
        self.assertEqual(exito['inventario'][0],
                         [1,
                          "Rayuela",
                          "Julio Cortázar",
                          "Alfaguara",
                          "Ficción Contemporánea",
                          "Activo",
                          1,
                          1],
                         "Las datos no coinciden")
