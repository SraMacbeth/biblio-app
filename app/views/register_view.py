from tkinter import *
from tkinter import messagebox
from controllers import user_controller
from components.password_container_frame import PasswordContainer


class RegisterView(Frame):

    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        title_label = Label(self, text="Registro", font=(None, 18, "bold"))
        title_label.pack(pady=10)

        email_label = Label(
            self, text="Ingrese su dirección de correo electronico::")
        email_label.pack(pady=10)

        email_entry = Entry(self)
        email_entry.pack(pady=10)

        first_name_label = Label(self, text="Ingrese su nombre:")
        first_name_label.pack(pady=10)

        first_name_entry = Entry(self)
        first_name_entry.pack(pady=10)

        last_name_label = Label(self, text="Ingrese su apellido:")
        last_name_label.pack(pady=10)

        last_name_entry = Entry(self)
        last_name_entry.pack(pady=10)

        password_label = Label(self, text="Ingrese su contraseña:")
        password_label.pack(pady=10)

        hint_password_label = Label(
            self,
            text="La contraseña debe contener como mínimo 8 caracteres \n y al menos 1 mayúscula, 1 minúscula, 1 símbolo y 1 número.")
        hint_password_label.pack(pady=10)

        self.password_container_1 = PasswordContainer(self)
        self.password_container_1.pack(pady=10)

        second_password_label = Label(
            self, text="Ingrese nuevamente su contraseña:")
        second_password_label.pack(pady=10)

        self.password_container_2 = PasswordContainer(self)
        self.password_container_2.pack(pady=10)

        register_buttton = Button(
            self,
            text="Register",
            width=10,
            padx=10,
            pady=10,
            command=lambda: self.on_register_click(
                first_name_entry.get(),
                last_name_entry.get(),
                email_entry.get(),
                self.password_container_1.password_entry.get(),
                self.password_container_2.password_entry.get()))
        register_buttton.pack(pady=10)

        return_login_label = Label(
            self, text="¿Ya tiene una cuenta? Inicie sesión.", font=(
                "None", 10, "underline"), foreground="blue")
        return_login_label.pack(pady=10)
        return_login_label.bind(
            "<Button-1>",
            lambda event: controller.show_frame("LoginView"))

    def on_register_click(
            self,
            firstName,
            lastName,
            email,
            password,
            secondPassword):

        resultado = user_controller.register(
            firstName, lastName, email, password, secondPassword)

        if resultado["estado"] == "ok":
            messagebox.showinfo("Exito", resultado["mensaje"])
            self.controller.show_frame("LoginView")
        else:
            messagebox.showerror("Error", resultado["mensaje"])
