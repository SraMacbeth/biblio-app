from tkinter import *
from views.base_view import BaseView
from components.search_bar_frame import SearchBar
from components.search_result_container_frame import SearchResultContainer
from components.book_form import BookForm
from controllers import book_controller

class BooksView(BaseView):
	
	def __init__(self, parent, controller, user=None):
		super().__init__(parent, controller)
		self.controller = controller
		self.user = user
		
		self.search_bar = SearchBar(self.main_area, search_callback=self.search, search_type='book', show_entity_selection=False)
		self.search_bar.grid(row=0, column=0, sticky="ew")
		
		text_label_updated = self.search_bar.set_text_label("Ingrese el ID del libro que desea buscar:")
		
		self.search_result_container = SearchResultContainer(self.main_area)
		self.search_result_container.grid(row=1, column=0, sticky="ew")
		
		self.action_button_container = Frame(self.main_area)
		self.action_button_container.grid(row=1, column=1, sticky="s", padx=5)
		self.action_button_container.grid_remove()
		
		self.edit_button = Button(self.action_button_container, text="✎", font=(None, 20, "bold"), fg="green", padx=5, pady=5,  command=self.open_edit_book_form, state=DISABLED)
		self.edit_button.grid(row=0, column=0, padx=5, pady=5)
		
		self.new_book_button = Button(self.main_area, text="Agregar nuevo libro", command = self.open_new_book_form)
		self.new_book_button.grid(row=3, column=0, columnspan=4, pady=10)
		
		self.main_area.grid_columnconfigure(0, weight=1)

	def clean_entries(self, entry):
		entry.delete(0, END)
		
	def search(self):
			
		self.search_result_container.clear_result_frame()
		
		book_id = self.search_bar.get_search_text()
		
		self.search_result_container.text_search_label.config(text=f"Resultado para la búsqueda: {book_id}")
		
		self.search_result_container.text_search_label .grid(row=0, column=0, pady=10, sticky="w")

		search_entity = self.search_bar.get_search_entity()
		
		result = book_controller.search_book_by_id(book_id)
		
		self.action_button_container.grid_remove()
		self.edit_button.config(state=DISABLED)
		
		if result["estado"] == "ok":

			data = result["detalles"]

			register_id = data[0]
			title = data[1]
			author_firstname = data[2]
			author_lastname = data[3]
			author_name = f"{author_firstname} {author_lastname}"
			isbn = data[5]
			publisher = data[6]
			status = data[7]
			total_copies = data[9]
			available_copies = data[10]

			treeview_values = [register_id, title, author_name, isbn, publisher, status, total_copies, available_copies]

			self.search_result_container.result_treeview.insert(parent='', index='end', values=treeview_values)
	
			self.search_result_container.adjust_columns_to_content(title, author_name, publisher)

			self.search_result_container.result_treeview.grid(row=1,column=0, sticky="nsew")
			self.search_result_container.xscrollbar_treeview.grid(row=2,column=0, sticky="ew")
			
			self.action_button_container.grid()
			self.edit_button.config(state=NORMAL)
		
			#self.clean_entries(self.search_bar.search_bar_entry)
		else:
			self.clean_entries(self.search_bar.search_bar_entry)
			self.search_result_container.result_label.config(text=result["mensaje"], font=(None, 10, "bold"), fg="red", anchor="w")
			self.search_result_container.result_label.grid(row=1, column=0, pady=10, sticky="ew")
		
	def open_new_book_form(self):
		
		new_book_form = BookForm("Agregar nuevo libro", parent=self, controller=self, type_form="new_book_form")
		
		new_book_form.transient(self)
		
		new_book_form.grab_set()
		
		self.wait_window(new_book_form)

	def open_edit_book_form(self):
		
		book_id = self.search_bar.get_search_text()
		
		result = book_controller.search_book_by_id(book_id)
				
		if result["estado"] == "ok":
			id_book, title,author_firstname, author_lastname, genre, isbn, publisher, status, copies_data, total_copies, available_copies = result["detalles"]
		
		edit_book_form = BookForm("Editar libro", parent=self, controller=self, type_form="edit_book_form", book_id=book_id, book_title=title, author_firstname=author_firstname, author_lastname=author_lastname, genre=genre, isbn=isbn, publisher=publisher, status=status, copies_data=copies_data)
		
		edit_book_form.transient(self)
		
		edit_book_form.grab_set()
		
		self.wait_window(edit_book_form)