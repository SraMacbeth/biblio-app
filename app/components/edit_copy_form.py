from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from controllers import book_controller

class EditCopyForm(Toplevel):
    
    """
    Formulario que permite editar una copia de un libro.
    """

    def __init__(
            self,
            form_title,
            parent,
            controller,
            type_form="",
            book_id="",
            copy_id="",
            copy_code="",
            user=None,
            status_loan="",
            unavailable_reason="",
            callback_refresh = ""):
        super().__init__(parent)
        self.form_title = form_title
        self.controller = controller
        self.type_form = type_form
        self.book_id = book_id
        self.copy_id=copy_id
        self.copy_code=copy_code
        self.user=user
        self.status_loan=status_loan
        self.unavailable_reason=unavailable_reason
        self.callback_refresh = callback_refresh
        
        self.title(self.form_title)
        self.resizable(False, False)
        self.container = Frame(self)
        self.container.grid(row=0, column=1, padx=20, pady=20)
        
        self.title_label = Label(
            self.container, text=self.form_title, font=(
                None, 18, "bold"))
        self.title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=10,
            sticky="nsew")
            
        self.id_copy_label = Label(self.container, text="ID de copia:")
        self.id_copy_label.grid(row=1, column=0, pady=10, sticky="w")
        
        self.id_copy_entry = Entry(self.container, relief="flat")
        self.id_copy_entry.insert(0, self.copy_id)
        self.id_copy_entry.config(state="readonly")
        self.id_copy_entry.grid(row=1, column=1, pady=10, sticky="w")
        
        self.copy_code_label = Label(self.container, text="Código de copia:")
        self.copy_code_label.grid(row=2, column=0, pady=10, sticky="w")
        
        self.copy_code_entry = Entry(self.container, relief="flat")
        self.copy_code_entry.insert(0, self.copy_code)
        self.copy_code_entry.config(state="readonly")
        self.copy_code_entry.grid(row=2, column=1, pady=10, sticky="w")
        
        self.status_loan_label = Label(self.container, text="Estado para préstamo:")
        self.status_loan_label.grid(row=3, column=0, pady=10, sticky="w")

        self.selected_status_loan = StringVar(value=self.status_loan)
        
        self.status_loan_selector = ttk.Combobox(self.container, textvariable=self.selected_status_loan, values=["Disponible", "No disponible"], state="readonly")
        self.status_loan_selector.set(self.status_loan)
        self.status_loan_selector.grid(row=3, column=1, pady=10, sticky="w")

        self.unavailable_reason_selector_visibility = self.status_loan_selector.bind('<<ComboboxSelected>>', lambda e: self.toggle_reason_visibility())

        self.unavailable_reason_label = Label(self.container, text="Motivo:")

        self.unavailable_reason_entry = Entry(self.container, relief="flat")

        self.selected_unavailable_reason = StringVar(value=self.unavailable_reason)

        self.unavailable_reason_selector = ttk.Combobox(self.container, textvariable=self.selected_unavailable_reason, values=["---", "Dañado", "En reparación", "Donación", "Descatalogado", "Pérdida", "Robo"], state="readonly")

        self.selected_unavailable_reason.set(self.unavailable_reason)

        self.toggle_reason_visibility()
        
        self.edit_copy_button = Button(self.container, text="Actualizar copia", command=self.update_copy)
        self.edit_copy_button.grid(row=5, column=0, columnspan=2, pady=20)
        
    def toggle_reason_visibility(self, *args):
        
        if self.status_loan_selector.get() == "Disponible":
            self.unavailable_reason_label.grid_remove()
            self.unavailable_reason_selector.grid_remove()
            self.selected_unavailable_reason.set("---")
        elif self.status_loan_selector.get() == "No disponible" and self.unavailable_reason != "Preestado":
            self.unavailable_reason_label.grid(row=4, column=0, pady=10, sticky="w")
            self.selected_unavailable_reason.set(self.unavailable_reason)            
            self.unavailable_reason_selector.grid(row=4, column=1, pady=10, sticky="w")
        else:
            self.unavailable_reason_label.grid(row=4, column=0, pady=10, sticky="w")
            self.unavailable_reason_entry.insert(0, self.unavailable_reason)
            self.unavailable_reason_entry.config(state="readonly")
            self.unavailable_reason_entry.grid(row=4, column=1, pady=10, sticky="w")
            
    def update_copy(self):
        
        original_data = (self.book_id, self.copy_id, self.copy_code, self.status_loan, self.unavailable_reason)

        data_to_validate = (self.book_id, self.id_copy_entry.get(), self.copy_code_entry.get(), self.selected_status_loan.get(), self.selected_unavailable_reason.get() or self.unavailable_reason_entry.get())

        result_check_changes = book_controller.check_data_changes(original_data, data_to_validate)
        
        if result_check_changes["estado"] == "sin cambios":
            messagebox.showinfo("Mensaje", result_check_changes["mensaje"])
            self.grab_release()
            self.destroy()
            return
                    
        result = book_controller.update_copy(data_to_validate[0], data_to_validate[1], data_to_validate[3], data_to_validate[4])

        if result["estado"] == "error":
            messagebox.showerror("Error", result["mensaje"])
            return
                    
        else:
            messagebox.showinfo("Exito", result["mensaje"])
            self.callback_refresh()
            self.grab_release()
            self.destroy()
