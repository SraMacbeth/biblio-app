from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from components.copies_form import CopiesForm
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
            inactive_reason="",
            callback_refresh = ""):
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
        self.callback_refresh = callback_refresh

        self.title(self.form_title)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
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

        self.original_data = {
            "title": self.book_title,
            "authors": [(self.author_firstname, self.author_lastname)],
            "genre": self.genre,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "type_form": self.type_form,
            "status": self.status,
            "inactive_reason": '---' if self.status == 'Activo' else self.inactive_reason
        }

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
            
            self.status_entry = Entry(container, relief="flat")
            self.status_entry.insert(0, self.status)
            self.status_entry.config(state="readonly")
            self.status_entry.grid(row=7, column=1, pady=10, sticky="w")
            
            self.top_separator = ttk.Separator(container)
            self.top_separator.grid(
                row=9, column=0, columnspan=2, pady=10, sticky="ew")

            self.manage_copies_button = Button(
                container, text="Gestionar copias", command=self.open_copies_form)
            self.manage_copies_button.grid(
                row=10, column=0, columnspan=2, pady=20)

            self.bottom_separator = ttk.Separator(container)
            self.bottom_separator.grid(
                row=11, column=0, columnspan=2, pady=10, sticky="ew")

            self.edit_book_button = Button(
                container, text="Editar libro", command=self.validate_and_save)
            self.edit_book_button.grid(
                row=12, column=0, columnspan=2, pady=20)

        self.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def validate_and_save(self):
        
        data_to_validate = {
            "title" : self.book_title_entry.get(),
            "authors":[(self.first_name_author_entry.get(),
                        self.last_name_author_entry.get())],
            "genre": self.selected_genre.get(),
            "isbn": self.isbn_entry.get(),
            "publisher":self.publisher_entry.get(),
            "type_form": self.type_form
            } 
            
        if self.type_form == "new_book_form":
            data_to_validate["copies"] = self.copies_entry.get()
                            
        validate_response = book_controller.validate_fields_form(data_to_validate)
       
        if validate_response["estado"] == "error":
            messagebox.showerror("Error", validate_response["mensaje"])
            return
        
        if self.type_form == "new_book_form":
            
            result_add = book_controller.add_book(data_to_validate["title"],
                        data_to_validate["authors"],
                        data_to_validate["genre"],
                        data_to_validate["isbn"],
                        data_to_validate["publisher"],
                        data_to_validate["copies"])
            
            if result_add["estado"] == "error":
                messagebox.showerror("Error", result_add["mensaje"])
                return
            else:
                messagebox.showinfo("Exito", result_add["mensaje"])
                self.grab_release()
                self.destroy()

        if self.type_form == "edit_book_form":
            
            result_check_changes = book_controller.check_data_changes(self.original_data, data_to_validate)
            
            if result_check_changes["estado"] == "sin cambios":
                messagebox.showinfo("Mensaje", result_check_changes["mensaje"])
                self.grab_release()
                self.destroy()
                return
                                               
            result_update = book_controller.update_book(
                            self.book_id,
                            data_to_validate["title"],
                            data_to_validate["authors"],
                            data_to_validate["genre"],
                            data_to_validate["isbn"],
                            data_to_validate["publisher"])
                
            if result_update["estado"] == "error":
                messagebox.showerror("Error", result_update["mensaje"])
                return
                    
            else:
                messagebox.showinfo("Exito", result_update["mensaje"])
                self.grab_release()
                self.on_closing()

    def open_copies_form(self):

        result = book_controller.search_book_by_id(self.book_id)

        if result["estado"] == "ok":
            id_book, title, author_firstname, author_lastname, genre, isbn, publisher, status, inactive_reason, copies_data, total_copies, available_copies = result[
                "detalles"]

        copies_form = CopiesForm(
            "Gestión de copias",
            parent=self,
            controller=self,
            type_form="copies_form",
            book_id=id_book,
            isbn=isbn,
            status=status,
            copies_data=copies_data,
            callback_refresh=self.refresh_book_status)

        copies_form.transient(self)

        copies_form.grab_set()

        self.wait_window(copies_form)
    
    def refresh_book_status(self):
        result = book_controller.search_book_by_id(self.book_id)
        new_status = result["detalles"][7]
        self.status_entry.config(state="normal")
        self.status_entry.delete(0, END)
        self.status_entry.insert(0, new_status)
        self.status_entry.config(state="readonly")

    def on_closing(self):
        if self.callback_refresh:
            self.callback_refresh()
        
        self.destroy()
