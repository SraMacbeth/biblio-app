from app.models.member_model import Member
from . import test_db_setup
import unittest
import os
os.environ['TESTING'] = 'True'

# Se definen constantes para los tests
TEST_USER_ID = 1

class TestMemberModel(unittest.TestCase):

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

    # --- TESTS DE SEGURIDAD ---
    def test_insercion_correcta(self):
        """Prueba que un nuevo socio se añade correctamente."""

        socio_a_agregar = ["Ana",
                           "Pérez",
                           "11222333",
                           "Sarmiento 1515 - Olivos",
                           "anaperez@gmail.com",
                           "1123456789",
                           TEST_USER_ID]

        # Act: Intentamos insertar
        exito, mensaje = Member.add_member(*socio_a_agregar)

        # Assert
        self.assertTrue(exito, f"La operación falló con el error: {mensaje}")

        # Confirmar que el socio existe en la base de datos
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM member WHERE dni = 11222333")
        row = cursor.fetchone()
        conn.close()

        # Assert
        self.assertEqual(row, ((1,'Ana','Pérez', 11222333,'Sarmiento 1515 - Olivos','anaperez@gmail.com','1123456789',1)
))

    def test_dni_se_almacena_correctamente(self):
        """Prueba que el DNI del nuevo socio se guarda correctamente."""

        # Preparación: Agregar un socio pára tener un DNI que verificar
        socio_a_agregar = ["Ana",
                           "Pérez",
                           "11222333",
                           "Sarmiento 1515 - Olivos",
                           "anaperez@gmail.com",
                           "1123456789",
                           TEST_USER_ID]

        exito, mensaje = Member.add_member(*socio_a_agregar)

        # Act: Obtener DNI del nuevo socio
        conn = test_db_setup.get_test_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT dni FROM member WHERE member_id = ?", (1, ))
        row = cursor.fetchone()
        dni_guardado = row[0]
        conn.close()

        # Assert
        self.assertEqual(dni_guardado, 11222333, "El DNI guardado no coincide con el ingresado por el usuario.")

    def test_verificar_socio_duplicado_en_creacion(self):
        """
        Verifica que no se permite crear dos socios con el mismo DNI.
        """

        # Preparación: Agregar el primer socio
        primer_socio = ["Ana",
                           "Pérez",
                           "11222333",
                           "Sarmiento 1515 - Olivos",
                           "anaperez@gmail.com",
                           "1123456789",
                           TEST_USER_ID]

        Member.add_member(*primer_socio)

        # Act: Intentar agregar el segundo socio con el mismo DNI que el primero
        segundo_socio = ["Juan",
                        "López",
                        "11222333",
                        "Rosario 3567 - Florida",
                        "juanlopez85@gmail.com",
                        "1198765432",
                         TEST_USER_ID]

        socio_dos = Member.add_member(*segundo_socio)

        # Assert
        self.assertFalse(socio_dos[0], "Nuevo usuario insertado exitosamente.")
        self.assertIn("El usuario que intenta ingresar DNI 11222333 ya se encuentra en la base de datos. \nUse el formulario de Edición si desea modificar sus datos.", socio_dos[1])
