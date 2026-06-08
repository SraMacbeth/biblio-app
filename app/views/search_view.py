from tkinter import *
from views.base_view import BaseView
from components.search_result_container_frame import SearchResultContainer
from controllers import book_controller

class SearchView(BaseView):

    def __init__(self, parent, controller, user=None):
        super().__init__(parent, controller)
        self.controller = controller
        self.user = user

        self.label = Label(self.main_area, text="Búsqueda global")
        self.label.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
        
        self.search_result_container = SearchResultContainer(self.main_area)
        self.search_result_container.grid(row=1, column=0, sticky="ew")
        
    def update_data(self, data=None):
        
        if data and "username" in data:
            self.user = data["username"]
        
        self.search()
        
    def search(self):
        
        self.search_result_container.clear_result_frame()
        
        self.search_result_container.result_treeview.config(displaycolumns=["ID", "Título", "Autor", "ISBN","Editorial","Status",])
        
        result = book_controller.get_all_inventory()

        if result["estado"] == "ok":

            inventory = result["inventario"]
                
            total_books = len(inventory)
            self.search_result_container.result_treeview.config(height=max(1, total_books))    
            
            for book in inventory:
                treeview_values = [
                    book[0],
                    book[2],
                    book[5],
                    book[1],
                    book[3],
                    book[4],
                    "",
                    ""
                ]
            
                self.search_result_container.result_treeview.insert(parent='', index='end', values=treeview_values)                    
                
            self.search_result_container.result_treeview.grid(row=1, column=0, sticky="nsew")
            
        else:
            self.search_result_container.result_label.config(
                text=result["mensaje"], font=(
                    None, 10, "bold"), fg="red", anchor="w")
            self.search_result_container.result_label.grid(
                row=1, column=0, pady=10, sticky="ew")
        
