from tkinter import *
from views.base_view import BaseView


class MembersView(BaseView):

    def __init__(self, parent, controller, user=None):
        super().__init__(parent, controller)
        self.controller = controller
        self.user = user

        self.label = Label(self.main_area, text="Members View")
        self.label.grid(row=0, column=0, padx=10, pady=20, sticky="nsew")

        self.grid_rowconfigure(1, weight=1)
