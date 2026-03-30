from tkinter import *
from tkinter import messagebox
from controllers import user_controller
from components.password_container_frame import PasswordContainer


class LoginView(Frame):

    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        title_label = Label(self, text="Login", font=(None, 18, "bold"))
        title_label.pack(pady=10)

        email_label = Label(self, text="Email")
        email_label.pack(pady=10)

        self.email_entry = Entry(self)
        self.email_entry.pack(pady=10)

        password_label = Label(self, text="Contraseña:")
        password_label.pack(pady=10)

        self.password_container = PasswordContainer(self)
        self.password_container.pack(pady=10)

        forgot_password_label = Label(
            self, text="¿Olvidó su contraseña? Restablézcala.", font=(
                "None", 10, "underline"), foreground="blue")
        forgot_password_label.pack(pady=10)
        forgot_password_label.bind(
            "<Button-1>",
            lambda event: controller.show_frame("ResetPasswordView"))

        login_button = Button(
            self,
            text="Iniciar sesión",
            width=10,
            padx=10,
            pady=10,
            command=lambda: self.on_login_click(
                self.email_entry.get(),
                self.password_container.password_entry.get()))
        login_button.pack(pady=10)

        register_label = Label(
            self, text="¿Todavía no es usuario? Regístrese.", font=(
                "None", 10, "underline"), foreground="blue")
        register_label.pack(pady=10)
        register_label.bind(
            "<Button-1>",
            lambda event: controller.show_frame("RegisterView"))

    def clean_entries(self):

        self.email_entry.delete(0, END)
        self.password_container.password_entry.delete(0, END)

    def on_login_click(self, email, password):

        resultado = user_controller.login(email, password)

        if resultado["estado"] == "ok":
            self.clean_entries()
            first_name = resultado["first_name"]
            last_name = resultado["last_name"]
            username = f"{first_name} {last_name}"
            self.controller.actual_user = username
            self.controller.load_private_views()
            self.controller.show_frame("HomeView", data={"username": username})
        else:
            messagebox.showerror("Error", resultado["mensaje"])
