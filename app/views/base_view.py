from tkinter import *
from components.header_bar_frame import HeaderBar


class BaseView(Frame):

    """
    Clase base para todas las vistas que requieren mostrar HeaderBar con nombre de usuario y botón de logout.
    """

    def __init__(self, parent, controller, user=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user

        self.header = HeaderBar(
            self,
            return_home_callback=self.return_home,
            logout_callback=self.logout)
        self.header.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        self.main_area = Frame(self)
        self.main_area.grid(row=2, column=1, sticky="nsew", padx=20, pady=20)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def update_data(self, data):
        username = data.get("username", "")
        self.header.set_username(username)

    def return_home(self):
        self.controller.show_frame("HomeView")

    def logout(self):
        self.actual_user = None
        self.controller.show_frame("LoginView")
