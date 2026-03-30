from tkinter import *
from tkinter import messagebox
from controllers import user_controller
from components.password_container_frame import PasswordContainer


class ResetPasswordView(Frame):

    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        title_label = Label(
            self, text="Reseteo de contraseña", font=(
                None, 18, "bold"))
        title_label.pack(pady=10)

        email_label = Label(
            self, text="Ingrese su dirección de correo electronico:")
        email_label.pack(pady=10)

        email_entry = Entry(self)
        email_entry.pack(pady=10)

        password1_label = Label(self, text="Ingrese su nueva contraseña:")
        password1_label.pack(pady=10)

        hint_password_label = Label(
            self,
            text="La contraseña debe contener como mínimo 8 caracteres \n y al menos 1 mayúscula, 1 minúscula, 1 símbolo y 1 número.")
        hint_password_label.pack(pady=10)

        self.password_container_1 = PasswordContainer(self)
        self.password_container_1.pack(pady=10)

        password2_label = Label(self, text="Ingrese nuevamente su contraseña:")
        password2_label.pack(pady=10)

        self.password_container_2 = PasswordContainer(self)
        self.password_container_2.pack(pady=10)

        reset_password_button = Button(
            self,
            text="Reset Password",
            width=10,
            padx=20,
            pady=10,
            command=lambda: self.on_reset_click(
                email_entry.get(),
                self.password_container_1.password_entry.get(),
                self.password_container_2.password_entry.get()))
        reset_password_button.pack(pady=10)

        return_login_label = Label(
            self, text="Cancelar y volver al Login", font=(
                "None", 10, "underline"), foreground="blue")
        return_login_label.pack(pady=10)
        return_login_label.bind(
            "<Button-1>",
            lambda event: controller.show_frame("LoginView"))

    def on_reset_click(self, email, password1, password2):

        resultado = user_controller.reset_password(email, password1, password2)

        if resultado["estado"] == "ok":
            messagebox.showinfo("Exito", resultado["mensaje"])
            self.controller.show_frame("LoginView")
        else:
            messagebox.showerror("Error", resultado["mensaje"])
