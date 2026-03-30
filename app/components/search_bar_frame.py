from tkinter import *


class SearchBar(Frame):

    """
    Barra de búsqueda que permite realizar xonsultas a la base de datos. Se reutiliza en las vistas Search, Book y Member.
    parent(Tk.Widget): El widget padre.
    """

    def __init__(
            self,
            parent,
            search_callback,
            search_type='all',
            show_entity_selection=False):
        super().__init__(parent)
        self.search_callback = search_callback

        self.label = Label(self, text="")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        self.search_bar_entry = Entry(self, width=50)
        self.search_bar_entry.grid(row=1, column=0, sticky="ew", pady=10)

        self.search_button = Button(
            self, text="Buscar", command=self.search_callback)
        self.search_button.grid(row=1, column=1, sticky="w", pady=10)

        self.entity_var = StringVar(value=search_type)

        self.radio_buttons_frame = Frame(self)
        self.radio_buttons_frame.grid(row=2, column=0, sticky="w", pady=10)

        self.book_option = Radiobutton(
            self.radio_buttons_frame,
            text="Libros",
            variable=self.entity_var,
            value="book")

        self.member_option = Radiobutton(
            self.radio_buttons_frame,
            text="Socios",
            variable=self.entity_var,
            value="member")

        if show_entity_selection:
            self.book_option.grid(
                row=0, column=0, sticky="w", padx=10, pady=10)
            self.member_option.grid(
                row=0, column=1, sticky="w", padx=10, pady=10)

    def set_text_label(self, text_label):
        self.label.config(text=text_label)

    def get_search_text(self):
        return self.search_bar_entry.get()

    def get_search_entity(self):
        return self.entity_var.get()
