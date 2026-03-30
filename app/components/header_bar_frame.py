from tkinter import *


class HeaderBar(Frame):

    """
    Barra superior que muestra el nombre del usuario actual y un botón de logout.
    Args:
    parent(Tk.Widget): El widget padre.
    logout_callback(function): Función que se ejecuta al presionar el botón de cerrar sesión.
    """

    def __init__(self, parent, return_home_callback, logout_callback):
        super().__init__(parent)
        self.return_home_callback = return_home_callback
        self.logout_callback = logout_callback

        self.return_home_button = Button(
            self, text="Home", command=self.return_home_callback)
        self.return_home_button.grid(
            row=0, column=0, sticky="w", padx=10, pady=5)

        self.grid_columnconfigure(1, weight=1)

        self.right_frame = Frame(self)
        self.right_frame.grid(row=0, column=2, sticky="e", padx=10, pady=5)

        self.username_label = Label(self.right_frame, text="")
        self.username_label.pack(side=LEFT)

        self.logout_button = Button(
            self.right_frame,
            text="Cerrar sesión",
            command=self.logout_callback)
        self.logout_button.pack(side=LEFT, padx=(5, 0))

    def set_username(self, username):
        self.username_label.config(text=f"Usuario conectado: {username}")
