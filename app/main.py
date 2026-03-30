from tkinter import *
from models import db
from views.login_view import LoginView
from views.reset_password_view import ResetPasswordView
from views.register_view import RegisterView
from views.home_view import HomeView
from views.search_view import SearchView
from views.books_view import BooksView
from views.members_view import MembersView
from views.loan_view import LoanView
import os
import sys

# --- Garantizar que la aplicación funcione sin importar desde qué carpeta se ejecute (ya sea por terminal o mediante el botón 'Play' de VS Code) ---
# Obtener la ruta absoluta de donde está el archivo que se está ejecutando
base_dir = os.path.dirname(os.path.abspath(__file__))

# Cambiar el "directorio de trabajo" de Python a esa carpeta
os.chdir(base_dir)

# Agregar la carpeta base al PATH de Python para facilitar importaciones MVC
sys.path.append(base_dir)


class App(Tk):

    """
    Clase principal de aplicación.
    Administra la ventana raíz y la navegación entre vistas(frames), utilizando un sistema centralizado para mostrar y actualizar frames.
    También puede mantener el estado global del usuario autenticado.
    Hereda de Tk: ventana principal de Tkinter.
    """

    def __init__(self):
        super().__init__()
        self.title("BiblioApp")
        # self.geometry("830x600")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.actual_user = None

        public_views = (LoginView, ResetPasswordView, RegisterView)

        for F in public_views:
            name = F.__name__
            frame = F(parent=self, controller=self)
            frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.frames[name] = frame

        self.show_frame("LoginView")

    def load_private_views(self):

        private_views = (
            HomeView,
            SearchView,
            BooksView,
            MembersView,
            LoanView)

        for F in private_views:
            name = F.__name__
            frame = F(parent=self, controller=self, user=self.actual_user)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[name] = frame

    def show_frame(self, name, data=None):
        frame = self.frames[name]
        if data and hasattr(frame, "update_data"):
            frame.update_data(data)
        frame.tkraise()


if __name__ == "__main__":
    db.setup_database()
    app = App()
    app.mainloop()
