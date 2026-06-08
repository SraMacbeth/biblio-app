from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from controllers import book_controller
from components.edit_copy_form import EditCopyForm

class CopiesForm(Toplevel):
    
    """
    Formulario que permite gestionar las copias un libro.
    """

    def __init__(
            self,
            form_title,
            parent,
            controller,
            type_form="",
            book_id="",
            isbn="",
            user=None,
            status="",
            copies_data="",
            callback_refresh = ""):
        super().__init__(parent)
        self.form_title = form_title
        self.controller = controller
        self.type_form = type_form
        self.book_id = book_id
        self.isbn = isbn
        self.user = user
        self.status = status
        self.copies_data = copies_data
        self.callback_refresh = callback_refresh
        
        self.title(self.form_title)
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
            
        self.copies_label = Label(container, text="Detalle de copias:")
        self.copies_label.grid(row=1, column=0, pady=10, sticky="w")
        
        self.treeview_columns = ("ID", "Código", "Estado", "Observaciones", "Acción")

        self.copies_treeview = ttk.Treeview(container, columns=self.treeview_columns, show='headings', height=1)
        
        self.copies_treeview.bind('<Button-1>', self.block_resizing, add='+')

        self.copies_treeview.grid(row=2, column=0, columnspan=2, sticky="w")

        self.copies_treeview.heading("ID", text="ID")
        self.copies_treeview.column("ID", width=0, minwidth=50, stretch=False, anchor="center")

        self.copies_treeview.heading("Código", text="Código")
        self.copies_treeview.column("Código", width=230, minwidth=230, stretch=False, anchor="center")

        self.copies_treeview.heading("Estado", text="Estado")
        self.copies_treeview.column("Estado", width=120, minwidth=120, stretch=False, anchor="center")

        self.copies_treeview.heading("Observaciones", text="Observaciones")
        self.copies_treeview.column("Observaciones", width=120, minwidth=120, stretch=False, anchor="center")
        
        self.copies_treeview.heading("Acción", text="Acción")
        self.copies_treeview.column("Acción", width=120, minwidth=120, stretch=False, anchor="center")

        self.existing_copies = self.copies_data

        self.treeview_values = [row for row in self.existing_copies] if self.existing_copies else []

        total_filas = len(self.treeview_values)
        self.copies_treeview.config(height=max(1, total_filas))

        for i in self.treeview_values:
            i = list(i)
            i.append("[ Editar ]")
            self.copies_treeview.insert(parent='', index='end', values=i)
        
        self.copies_treeview.bind("<ButtonRelease-1>", self.on_treeview_click)
        
        self.copies_treeview.bind("<Motion>", self.on_action_column_hover)
			
        self.copies_label = Label(container, text="Copias a añadir:")
        self.copies_label.grid(row=3, column=0, pady=20, sticky="w")

        self.copies_entry = Entry(container)
        self.copies_entry.insert(0, 0)
        self.copies_entry.grid(row=3, column=1, pady=20, sticky="w")
        
        self.edit_copies_button = Button(container, text="Actualizar copias", command=self.update_copies)
        self.edit_copies_button.grid(row=4, column=0, columnspan=2, pady=20)

    def block_resizing(self, event):
        return "break"
    
    def on_treeview_click(self, event):
        
        region_clicked = self.copies_treeview.identify_region(event.x, event.y)
            
        column_clicked = self.copies_treeview.identify_column(event.x)

        if region_clicked == "cell" and column_clicked == "#5":
            copy_selected = self.copies_treeview.identify_row(event.y)
            copy_data = self.copies_treeview.item(copy_selected, 'values')
            self.open_copy_form(copy_data)
        
    def on_action_column_hover(self, event):
        
        region_hover = self.copies_treeview.identify_region(event.x, event.y)

        column_hover = self.copies_treeview.identify_column(event.x)
        
        if region_hover == "cell" and column_hover == "#5":
            self.copies_treeview.config(cursor="hand2")
        else:
            self.copies_treeview.config(cursor="")
            
    def update_copies(self):
        
        copies_to_add = self.copies_entry.get()
              
        result = book_controller.update_copies(self.book_id, self.isbn, self.status,  copies_to_add)

        if result["estado"] == "error":
            messagebox.showerror("Error", result["mensaje"])
            return
                    
        else:
            messagebox.showinfo("Exito", result["mensaje"])
            self.callback_refresh()
            self.grab_release()
            self.destroy()

    def refresh_copy_data(self):
                
        result = book_controller.search_book_by_id(self.book_id)
        copies_data = result["detalles"][9]
        
        items = self.copies_treeview.get_children()
        self.copies_treeview.delete(*items)
        
        for i in copies_data:
            row_values = i + ["[ Editar ]"]
            self.copies_treeview.insert(parent='', index='end', values=row_values)
        
        self.callback_refresh()
            
        
    def open_copy_form(self, copy_data):
        
        copy_id, copy_code, status_loan, unavailable_reason, action = copy_data
        
        copy_form = EditCopyForm(
            "Editar copia",
            parent=self,
            controller=self,
            type_form="edit_copy_form",
            book_id=self.book_id,
            copy_id=copy_id,
            copy_code=copy_code,
            status_loan=status_loan,
            unavailable_reason=unavailable_reason,
            callback_refresh=self.refresh_copy_data)

        copy_form.transient(self)

        copy_form.grab_set()

        self.wait_window(copy_form)
