from models.user_model import User
import re
import string


def mail_validation(email):
    """
    Valida el formato del email ingresado por el uuario
    Parametros:
    email(str) direccion de correo del usuario
    Retorna True si el correo coincide con el patron establecido o False si no coincide
    """

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9._]+\.[a-zA-Z]{2,}$"

    return bool(re.match(pattern, email))


def is_password_valid(password):
    """
    Valida la seguridad de la contraseña creada por el usuario
    Parametros:
    password(str) contraseña creada por el usuario
    Retorna True si el la contraseña cumple con los requisitos de seguridad  o False si no lo hace
    """

    if len(password) < 8:
        return False

    if all(not caracter.isupper() for caracter in password):
        return False

    if all(not caracter.islower() for caracter in password):
        return False

    if all(caracter not in string.punctuation for caracter in password):
        return False

    if all(not caracter.isdigit() for caracter in password):
        return False

    return True


def login(email, password):
    """
    Permite el acceso del usuario al sistema
    Parametros:
    email(str) direccion de correo del usuario
    password(str) contraseña creada por el usuario
    Retorna diferentes mensajes en funcion de los casos y nombre y aṕellido del usuario en caso de login exitoso.
    """

    user = User.get_user_by_email(email)

    if email == "" or password == "":
        return {
            "estado": "error",
            "mensaje": "Los campos no pueden estar vacíos."}
    elif not user:
        return {"estado": "error", "mensaje": "El email no esta registrado."}
    elif user[4] != password:
        return {"estado": "error", "mensaje": "Contraseña inválida."}
    else:
        first_name = user[1]
        last_name = user[2]
        return {
            "estado": "ok",
            "mensaje": "Login exitoso",
            "first_name": first_name,
            "last_name": last_name}


def register(firstName, lastName, email, password1, password2):
    """
    Registra un nuevo usuario en la base de datos
    Parametros:
    firstName(str) nombre del usuario
    lastName(str) apellido del usuario
    email(str) direccion de correo del usuario
    password(str) contraseña creada por el usuario
    Retorna diferentes mensajes en funcion de los casos
    """

    if firstName == "" or lastName == "" or email == "" or password1 == "" or password2 == "":
        return {
            "estado": "error",
            "mensaje": "Los compos no pueden estar vacíos"}

    if not mail_validation(email):
        return {"estado": "error", "mensaje": "El email ingrado es inválido."}

    if User.check_user_by_email(email):
        return {
            "estado": "error",
            "mensaje": "El email ya se encuentra registrado."}

    if not is_password_valid(password1):
        return {
            "estado": "error",
            "mensaje": "Las contraseñas ingresada no es válida."}

    if password1 != password2:
        return {"estado": "error", "mensaje": "Las contraseñas no coinciden."}

    new_user = User.insert_user(firstName, lastName, email, password1)
    return {
        "estado": "ok",
        "mensaje": "Registro exitoso.\nInicie sesión a continuación"}


def reset_password(email, password1, password2):
    """
    Permite al usuario establecer una nueva contraseña
    Parametros:
    email(str) direccion de correo del usuario
    password1(str) primer contraseña ingresada por el usuario
    password2(str) segunda contraseña ingresada por el usuario
    Retorna diferentes mensajes en funcion de los casos
    """

    if email == "" or password1 == "" or password2 == "":
        return {
            "estado": "error",
            "mensaje": "Los compos no pueden estar vacíos."}

    if not mail_validation(email):
        return {"estado": "error", "mensaje": "El email ingrado es inválido."}

    if not User.check_user_by_email(email):
        return {"estado": "error", "mensaje": "El email no esta registrado."}

    if not is_password_valid(password1):
        return {
            "estado": "error",
            "mensaje": "La contraseña ingresada no es válida."}

    if password1 != password2:
        return {"estado": "error", "mensaje": "Las contraseñas no coinciden."}

    User.update_password(email, password1)

    return {
        "estado": "ok",
        "mensaje": "Contraseña actualizada correctamente.\nInicie sesión a continuación"}
