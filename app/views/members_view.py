from tkinter import *
from views.base_view import BaseView
from components.search_bar_frame import SearchBar

class MembersView(BaseView):

    def __init__(self, parent, controller, user=None):
        super().__init__(parent, controller)
        self.controller = controller
        self.user = user

        self.search_bar = SearchBar(
            self.main_area,
            search_callback=None,
            search_type='member',
            show_entity_selection=False)
        self.search_bar.grid(row=0, column=0, sticky="ew")
        self.search_bar.set_text_label(
            "Ingrese el DNI del socio que desea buscar:")

        self.new_member_button = Button(
            self.main_area,
            text="Agregar nuevo socio")
        self.new_member_button.grid(row=3, column=0, columnspan=4, pady=10)

        self.main_area.grid_columnconfigure(0, weight=1)