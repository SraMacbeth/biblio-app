import sqlite3
from . import db

CURRENT_USER_ID = 1

class Member():

    def __init__(
            self,
            member_id,
            first_name,
            last_name,
            dni,
            address,
            email,
            phone_number):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.address = address
        self.email = email
        self.phone_number = phone_number

    @classmethod
    def get_member_by_dni(cls, dni):
        """
        Obtiene los datos del socio que coincide con el dni ingresado
        Parametros: dni(int) dni del socio
        Retorna una tupla con los datos del socio si existe o None si no existe
        """

        try:
                with db.get_db_connection() as connection:
                    cursor = connection.cursor()

                    # Obtener datos del socio segun su DNI
                    cursor.execute(
                        "SELECT member_id, first_name, last_name, dni, address, email, phone_number FROM member WHERE dni = ?;",
                        (dni,
                         ))

                    member = cursor.fetchone()

                    return member

        except sqlite3.Error as e:
            #print(e)
            return False, str(e)

    @classmethod
    def add_member(
            cls,
            first_name,
            last_name,
            dni,
            address,
            email,
            phone_number,
            user_id):
        """
        Inserta los datos de un nuevo socio en la base de datos
        Parametros:
        first_name(str): nombre del socio
        last_name(str): apellido del socio
        dni(int): DNI del socio
        address(str): dirección del socio
        email(str): correo electrónico del socio
        phone_number(int): teléfono del socio
        user_id(int): id del usuario que ingresa el socio
        """

        try:
            with db.get_db_connection() as connection:
                cursor = connection.cursor()

                # Verificar si el usuario existe en la base de datos
                cursor.execute("SELECT * FROM member WHERE dni = ?", (dni,))

                if cursor.fetchone():
                    return False, f"El usuario que intenta ingresar DNI {dni} ya se encuentra en la base de datos. \nUse el formulario de Edición si desea modificar sus datos."
                else:
                    # Insertar socio
                    cursor.execute(
                        "INSERT INTO member (first_name, last_name, dni, address, email, phone_number, user_id) VALUES(?, ?, ?, ?, ?, ?, ?);",
                        (first_name,
                        last_name,
                        dni,
                        address,
                        email,
                        phone_number,
                        CURRENT_USER_ID))

                    connection.commit()

                    return True, "Socio ingresado exitosamente."

        except sqlite3.Error as e:
            #print(f"\n--- ERROR DE SQLITE EN ADD_BOOK: {e} ---")
            return False, str(e)
