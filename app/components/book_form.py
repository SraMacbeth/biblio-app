from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from controllers import book_controller, genre_controller


class BookForm(Toplevel):

    """
    Formulario que permite cargar o editar un libro.
    """

    def __init__(
            self,
            form_title,
            parent,
            controller,
            type_form="",
            book_id="",
            user=None,
            book_title="",
            author_firstname="",
            author_lastname="",
            genre="",
            isbn="",
            publisher="",
            copies_data="",
            status="", 
            inactive_reason=""):
        super().__init__(parent)
        self.form_title = form_title
        self.controller = controller
        self.type_form = type_form
        self.book_id = book_id
        self.user = user
        self.book_title = book_title
        self.author_firstname = author_firstname
        self.author_lastname = author_lastname
        self.genre = genre
        self.isbn = isbn
        self.publisher = publisher
        self.copies_data = copies_data
        self.status = status
        self.inactive_reason = inactive_reason

        self.title(self.form_title)
        # self.geometry("500x500")
        self.resizable(False, False)

        container = Frame(self)
        container.grid(row=0, column=1, padx=20, pady=20)

        self.title_label = Label(
            container, text=self.form_title, font=(
                None, 18, "bold"))
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10,
            sticky="nsew")

        self.book_title_label = Label(container, text="Título:")
        self.book_title_label.grid(row=1, column=0, pady=10, sticky="w")

        self.book_title_entry = Entry(container)
        self.book_title_entry.insert(0, self.book_title)
        self.book_title_entry.grid(row=1, column=1, pady=10, sticky="w")

        self.first_name_author_label = Label(
            container, text="Nombre del autor:")
        self.first_name_author_label.grid(row=2, column=0, pady=10, sticky="w")

        self.first_name_author_entry = Entry(container)
        self.first_name_author_entry.insert(0, self.author_firstname)
        self.first_name_author_entry.grid(row=2, column=1, pady=10, sticky="w")

        self.last_name_author_label = Label(
            container, text="Apellido del autor:")
        self.last_name_author_label.grid(row=3, column=0, pady=10, sticky="w")

        self.last_name_author_entry = Entry(container)
        self.last_name_author_entry.insert(0, self.author_lastname)
        self.last_name_author_entry.grid(row=3, column=1, pady=10, sticky="w")

        self.genre_label = Label(container, text="Género:")
        self.genre_label.grid(row=4, column=0, pady=10, sticky="w")

        self.selected_genre = StringVar(value=self.genre)

        self.genre_selector = ttk.Combobox(
            container,
            textvariable=self.selected_genre,
            values=genre_controller.list_genres(),
            state="readonly")
        self.genre_selector.set(self.genre)
        self.genre_selector.grid(row=4, column=1, pady=10, sticky="w")

        self.isbn_label = Label(container, text="ISBN:")
        self.isbn_label.grid(row=5, column=0, pady=10, sticky="w")

        self.isbn_entry = Entry(container)
        self.isbn_entry.insert(0, self.isbn)
        self.isbn_entry.grid(row=5, column=1, pady=10, sticky="w")

        self.publisher_label = Label(container, text="Editorial:")
        self.publisher_label.grid(row=6, column=0, pady=10, sticky="w")

        self.publisher_entry = Entry(container)
        self.publisher_entry.insert(0, self.publisher)
        self.publisher_entry.grid(row=6, column=1, pady=10, sticky="w")

        if type_form == "new_book_form":

            self.copies_label = Label(container, text="Número de copias:")
            self.copies_label.grid(row=7, column=0, pady=10, sticky="w")

            self.copies_entry = Entry(container)
            self.copies_entry.insert(0, self.copies_data)
            self.copies_entry.grid(row=7, column=1, pady=10, sticky="w")

            self.add_new_book_button = Button(
                container, text="Agregar libro", command=self.validate_and_save)
            self.add_new_book_button.grid(
                row=8, column=0, columnspan=2, pady=20)

        if type_form == "edit_book_form":

            self.status_label = Label(container, text="Estado:")
            self.status_label.grid(row=7, column=0, pady=10, sticky="w")

            self.selected_status = StringVar(value=self.status)

            self.status_selector = ttk.Combobox(
                container, textvariable=self.selected_status, values=[
                    "Activo", "Inactivo"], state="readonly")
            self.status_selector.set(self.status)
            self.status_selector.grid(row=7, column=1, pady=10, sticky="w")

            self.advertise_message = self.status_selector.bind(
                '<<ComboboxSelected>>', lambda e: self.show_advertising())

            self.inactive_reason_label = Label(container, text="Motivo de inactivación:")
            
            self.selected_inactive_reason = StringVar(value=self.inactive_reason)

            self.inactive_reason_selector = ttk.Combobox(
                container, textvariable=self.selected_inactive_reason, values=[
                    "Dañado", "En reparación", "Donación", "Descatalogado", "Pérdida", "Robo"], state="readonly")
            
            self.selected_inactive_reason.set(self.inactive_reason)
            
            self.toggle_reason_visibility()
            """
			self.copies_label = Label(container, text="Copias a añadir:")
			self.copies_label.grid(row=8, column=0, pady=10, sticky="w")

			self.copies_entry = Entry(container)
			self.copies_entry.insert(0, 0)
			self.copies_entry.grid(row=8, column=1, pady=10, sticky="w")

			self.xscrollbar_treeview = ttk.Scrollbar(container, orient=HORIZONTAL)

			self.treeview_columns = ("ID", "Código", "Estado", "Observaciones")

			self.copies_treeview = ttk.Treeview(container, columns=self.treeview_columns, show='headings', height=1, xscrollcommand=self.xscrollbar_treeview.set)

			self.xscrollbar_treeview.config(command=self.copies_treeview.xview)

			self.copies_treeview.bind('<Button-1>', self.block_resizing, add='+')

			self.copies_treeview.grid(row=9, column=0, columnspan=2, sticky="w")

			self.copies_treeview.heading("ID", text="ID")
			self.copies_treeview.column("ID", width=0, minwidth=50, stretch=False, anchor="center")

			self.copies_treeview.heading("Código", text="Código")
			self.copies_treeview.column("Código", width=230, minwidth=230, stretch=False, anchor="center")

			self.copies_treeview.heading("Estado", text="Estado")
			self.copies_treeview.column("Estado", width=120, minwidth=120, stretch=False, anchor="center")

			self.copies_treeview.heading("Observaciones", text="Observaciones")
			self.copies_treeview.column("Observaciones", width=120, minwidth=120, stretch=False, anchor="center")

			self.existing_copies = self.copies_data

			treeview_values = [row for row in self.existing_copies] if self.existing_copies else []

			total_filas = len(treeview_values)
			self.copies_treeview.config(height=max(1, total_filas))

			for i in treeview_values:
				self.copies_treeview.insert(parent='', index='end', values=i)
			"""

            self.top_separator = ttk.Separator(container)
            self.top_separator.grid(
                row=9, column=0, columnspan=2, pady=10, sticky="ew")

            self.manage_copies_button = Button(
                container, text="Gestionar copias")
            self.manage_copies_button.grid(
                row=10, column=0, columnspan=2, pady=20)

            self.bottom_separator = ttk.Separator(container)
            self.bottom_separator.grid(
                row=11, column=0, columnspan=2, pady=10, sticky="ew")

            self.edit_book_buttton = Button(
                container, text="Editar libro", command=self.validate_and_save)
            self.edit_book_buttton.grid(
                row=12, column=0, columnspan=2, pady=20)

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def show_advertising(self):

        actual_state = self.selected_status.get()

        result = book_controller.advertise_change_status(actual_state)

        if result["estado"] == "ok":
            messagebox.showinfo("Advertencia", result["mensaje"])
            
        self.toggle_reason_visibility()

    def toggle_reason_visibility(self, *args):
        
        if self.status_selector.get() == "Activo":
            self.inactive_reason_label.grid_remove()
            self.inactive_reason_selector.grid_remove()
            self.selected_inactive_reason.set("")
        else:
            self.inactive_reason_label.grid(row=8, column=0, pady=10, sticky="w")
            self.inactive_reason_selector.grid(row=8, column=1, pady=10, sticky="w")

    def block_resizing(self, event):
        return "break"

    def validate_and_save(self):

        if self.type_form == "new_book_form":
            self.add_new_book(self.book_title_entry.get(),
                              [(self.first_name_author_entry.get(),
                                self.last_name_author_entry.get())],
                              self.selected_genre.get(),
                              self.isbn_entry.get(),
                              self.publisher_entry.get(),
                              self.copies_entry.get())

        if self.type_form == "edit_book_form":
            self.update_book(self.book_id,
                             self.book_title_entry.get(),
                             [(self.first_name_author_entry.get(),
                               self.last_name_author_entry.get())],
                             self.selected_genre.get(),
                             self.isbn_entry.get(),
                             self.publisher_entry.get(),
                             #self.copies_entry.get(),
                             "0",
                             self.selected_status.get(),
                             self.selected_inactive_reason.get(),
                             #None
                             )

    def add_new_book(self, title, authors, genre, isbn, publisher, copies):

        result = book_controller.add_book(
            title, authors, genre, isbn, publisher, copies)

        if result["estado"] == "ok":
            messagebox.showinfo("Exito", result["mensaje"])
            self.grab_release()
            self.destroy()
        else:
            messagebox.showerror("Error", result["mensaje"])

    def update_book(
            self,
            book_id,
            title,
            authors,
            genre,
            isbn,
            publisher,
            copies,
            status,
            unavailable_reason):

        result = book_controller.update_book(
            book_id,
            title,
            authors,
            genre,
            isbn,
            publisher,
            copies,
            status,
            unavailable_reason)

        if result["estado"] == "ok":
            messagebox.showinfo("Exito", result["mensaje"])
            self.grab_release()
            self.destroy()
        else:
            messagebox.showerror("Error", result["mensaje"])
