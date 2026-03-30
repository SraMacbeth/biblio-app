from app.models.book_model import Book
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


class TestBookModel(unittest.TestCase):

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

    # --- TESTS DE INVENTARIO Y SEGURIDAD ---
    def test_insercion_correcta(self):
        """Prueba que un nuevo libro se añade correctamente."""

        libro_a_agregar = ["Rayuela",
                           [("Julio",
                             "Cortázar")],
                           "Ficción Contemporánea",
                           "978-1",
                           "Alfaguara",
                           3,
                           STATUS,
                           TEST_USER_ID]

        # Act: Intentamos insertar
        exito = Book.add_book(*libro_a_agregar)

        # Aseert
        self.assertTrue(exito, "La inserción falló")

        # Verificacion de codigos
        # Buscar el ID del libro en la DB por su ISBN
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = row[0]
        conn.close()
        # Buscar el libro por su ID
        inserted_book = Book.get_book_by_id(generated_id)
        # Assert - Verificar que al insertar un libro con 3 copias, la base de
        # datos realmente contenga los códigos ISBN-1, ISBN-2 e ISBN-3
        self.assertEqual(inserted_book[3][0][1], "978-1-1", "978-1-1")
        self.assertEqual(inserted_book[3][1][1], "978-1-2", "978-1-2")
        self.assertEqual(inserted_book[3][2][1], "978-1-3", "978-1-3")

    def test_buscar_por_id(self):
        '''Asegura que get_book_by_id devuelve exactamente lo que se espera'''

        # PREPARACIÓN: Insertar un libro manualmente para tener algo que buscar
        libro_datos = ["Rayuela",
                       [("Julio",
                         "Cortázar")],
                       "Ficción Contemporánea",
                       "978-1",
                       "Alfaguara",
                       1,
                       STATUS,
                       TEST_USER_ID]
        Book.add_book(*libro_datos)

        # Buscar el ID en la DB por el ISBN del libro
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = row[0]
        conn.close()

        # Act
        datos_libro = Book.get_book_by_id(generated_id)

        # Assert
        self.assertIsNotNone(datos_libro,
                             "No se encontró el libro con el ID generado")

        # Verificar el libro encontrado por su titulo
        self.assertEqual(datos_libro[0][2], "Rayuela", "El título no coincide")

    def test_buscar_por_id_inexistente(self):
        '''Asegura que si se busca un libro con un id inexistente devuelve el error'''

        # PREPARACIÓN: Insertar un libro manualmente para tener algo que buscar
        libro_datos = ["Rayuela",
                       [("Julio",
                         "Cortázar")],
                       "Ficción Contemporánea",
                       "978-1",
                       "Alfaguara",
                       1,
                       TEST_USER_ID,
                       STATUS]
        Book.add_book(*libro_datos)

        # Buscar el ID del libro ingresado en la DB por el ISBN del libro
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = row[0]
        conn.close()

        # Id inexistente a buscar, se calcula en base al id generado.
        id_inexistente = generated_id + 1

        # Act
        datos_libro = Book.get_book_by_id(id_inexistente)

        # Assert
        self.assertIsNone(
            datos_libro,
            "Error: se encontró un libro con el ID ingresado")

    def test_actualizar_libro(self):
        """Prueba que un libro existente se actualiza correctamente."""

        # PREPARACIÓN: Insertar un libro manualmente para tener algo que
        # actualizar
        libro_datos = ["Rayuela",
                       [("Julio",
                         "Cortázar")],
                       "Ficción Contemporánea",
                       "978-1",
                       "Alfaguara",
                       1,
                       STATUS,
                       TEST_USER_ID]
        Book.add_book(*libro_datos)

        # Buscar el ID en la DB por el ISBN del libro
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = row[0]
        conn.close()

        # Crear los nuevps datos del libro
        nuevos_datos = [generated_id,
                        "Rayuela",
                        [("Julio",
                          "Cortázar")],
                        "Ficción Contemporánea",
                        "978-1",
                        "Alfaguara",
                        1,
                        "Inactivo",
                        None,
                        TEST_USER_ID]

        # Act
        exito = Book.update_book(*nuevos_datos)

        # Assert
        self.assertTrue(exito[0], "La actualizacion fallo.")

        # Verificar el libro actualizado por su estado
        libro_actualizado = Book.get_book_by_id(generated_id)
        self.assertEqual(
            libro_actualizado[0][6],
            "Inactivo",
            "El estado inicial no coincide")

        # Verificar que también ocurrió la consecuencia lógica (se modifico a
        # "No disponible" el estado de las copias)
        self.assertEqual(libro_actualizado[3][0][2], "No disponible")

    def test_continuidad_codigos_actualizacion(self):
        ''' Asegura que al aumentar la cantidad de copias de un libro, los codigos de las nuevas copias mantienen la continuidad respecto de las copias existentes.'''

        # PREPARACIÓN: Insertar un libro manualmente para tener algo que
        # actualizar
        libro_datos = ["Rayuela",
                       [("Julio",
                         "Cortázar")],
                       "Ficción Contemporánea",
                       "978-1",
                       "Alfaguara",
                       2,
                       STATUS,
                       TEST_USER_ID]
        Book.add_book(*libro_datos)

        # Buscar el ID en la DB por el ISBN del libro
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = row[0]
        conn.close()

        # Act
        nuevos_datos = [generated_id,
                        "Rayuela",
                        [("Julio",
                          "Cortázar")],
                        "Ficción Contemporánea",
                        "978-1",
                        "Alfaguara",
                        4,
                        STATUS,
                        None,
                        TEST_USER_ID]
        Book.update_book(*nuevos_datos)

        # Assert
        libro_actualizado = Book.get_book_by_id(generated_id)

        # Verificar que ahora el total de copias sea 6
        self.assertEqual(
            len(libro_actualizado[3]), 6, "El número total de copias no es 4")

        # Verificar la continuidad de los indices en los codigos de las nuevas
        # copias
        self.assertEqual(
            libro_actualizado[3][2][1],
            "978-1-3",
            "El codigo de copia no es correcto")

        self.assertEqual(
            libro_actualizado[3][3][1],
            "978-1-4",
            "El codigo de copia no es correcto")

    def test_validacion_de_integridad(self):
        '''Confirma que el modelo devuelve False y su correspondiente mensaje de error,
        cuando se intenta pasar a "Inactivo" un libro que tiene al menos una copia con status_loan = 'Prestado'.'''

        # PREPARACIÓN:

        # Insertar un libro manualmente para tener algo que actualizar
        libro_datos = ["Rayuela",
                       [("Julio",
                         "Cortázar")],
                       "Ficción Contemporánea",
                       "978-1",
                       "Alfaguara",
                       1,
                       STATUS,
                       TEST_USER_ID]
        Book.add_book(*libro_datos)

        # Buscar el ID en la DB por el ISBN del libro
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = row[0]
        conn.close()

        # Cambiar manualmente el estado de una copia a "Prestado"
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE copy SET status_loan = ?, unavailable_reason = ? WHERE rowid IN (SELECT rowid FROM copy WHERE book_id = ? AND status_loan = 'Disponible')",
            (STATUS_LOAN_LOANED,
             "Préstamo",
             generated_id))
        conn.commit()

        # Crear los nuevps datos del libro
        nuevos_datos = [generated_id,
                        "Rayuela",
                        [("Julio",
                          "Cortázar")],
                        "Ficción Contemporánea",
                        "978-1",
                        "Alfaguara",
                        1,
                        "Inactivo",
                        None,
                        TEST_USER_ID]

        # Act
        exito = Book.update_book(*nuevos_datos)

        # Assert
        self.assertFalse(exito[0], exito[1])

    def test_validar_copia_mayor_a_cero(self):
        '''
Verifica que si el modelo recibe un 0 en el número de copias al agregar un libro, devuelve el mensaje de error esperado.
'''

    # PREPARACIÓN:
    # Insertar un libro con 0 copias manualmente
        datos_libro = ["Rayuela",
                       [("Julio",
                         "Cortázar")],
                       "Ficción Contemporánea",
                       "978-1",
                       "Alfaguara",
                       0,
                       STATUS,
                       TEST_USER_ID]

        # Act
        exito = Book.add_book(*datos_libro)

        # Assert
        self.assertFalse(exito[0], exito[1])

    def test_de_reactivacion(self):
        '''
Verifica que si un libro pasa de estado "Inactivo" a "Activo" todas sus copias se vuelven disponibles y se resetea el unavailable_reason.
'''

    # PREPARACIÓN:
    # Insertar un libro inactivo con copias no disponibles
        datos_libro = ["Rayuela",
                       [("Julio",
                         "Cortázar")],
                       "Ficción Contemporánea",
                       "978-1",
                       "Alfaguara",
                       1,
                       "Inactivo",
                       TEST_USER_ID]
        Book.add_book(*datos_libro)

        # Buscar el ID en la DB por el ISBN del libro
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT book_id FROM book WHERE isbn = ?", ("978-1",))
        row = cursor.fetchone()
        generated_id = row[0]
        conn.close()

        # Cambiar manualmente el estado de una copia a "No disponible"
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE copy SET status_loan = ?, unavailable_reason = ? WHERE rowid IN (SELECT rowid FROM copy WHERE book_id = ? AND status_loan = 'Disponible')",
            (STATUS_LOAN_UNAVAILABLE,
             "Libro Inactivado",
             generated_id))
        conn.commit()
        conn.close()

        # Act
        nuevos_datos = [generated_id,
                        "Rayuela",
                        [("Julio",
                          "Cortázar")],
                        "Ficción Contemporánea",
                        "978-1",
                        "Alfaguara",
                        1,
                        STATUS,
                        None,
                        TEST_USER_ID]
        Book.update_book(*nuevos_datos)

        # Extraer el status_loan y el unavailabre_reason del libro luego de la
        # actualizacion
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT status_loan, unavailable_reason FROM copy WHERE book_id = ?",
            (generated_id,
             ))
        row = cursor.fetchone()
        conn.close()

        # Assert
        self.assertEqual(
            row[0],
            "Disponible",
            "El libro no se encuentra disponible")
        self.assertEqual(row[1], None, "El libro tiene una observacion")
