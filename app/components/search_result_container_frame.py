from tkinter import *
from tkinter import ttk
import tkinter.font as tkfont


class SearchResultContainer(Frame):

    def __init__(self, parent):
        super().__init__(parent, width=700, height=100)

        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.text_search_label = Label(self, text="")

        self.result_label = Label(self, text="")

        self.xscrollbar_treeview = ttk.Scrollbar(self, orient=HORIZONTAL)

        self.treeview_columns = (
            "ID",
            "Título",
            "Autor",
            "ISBN",
            "Editorial",
            "Status",
            "Stock",
            "Disponibles")

        self.result_treeview = ttk.Treeview(
            self,
            columns=self.treeview_columns,
            show='headings',
            height=1,
            xscrollcommand=self.xscrollbar_treeview.set)

        self.xscrollbar_treeview.config(command=self.result_treeview.xview)

        self.result_treeview.bind('<Button-1>', self.block_resizing, add='+')

        self.result_treeview.grid(row=0, column=0, sticky="nsew")
        self.result_treeview.grid_remove()
        self.xscrollbar_treeview.grid(row=1, column=0, sticky="ew")
        self.xscrollbar_treeview.grid_remove()

        self.result_treeview.heading("ID", text="ID")
        self.result_treeview.column(
            "ID",
            width=50,
            minwidth=50,
            stretch=False,
            anchor="center")

        self.result_treeview.heading("Título", text="Título")
        self.result_treeview.column(
            "Título",
            width=230,
            minwidth=230,
            stretch=False,
            anchor="center")

        self.result_treeview.heading("Autor", text="Autor")
        self.result_treeview.column(
            "Autor",
            width=120,
            minwidth=120,
            stretch=False,
            anchor="center")

        self.result_treeview.heading("ISBN", text="ISBN")
        self.result_treeview.column(
            "ISBN",
            width=120,
            minwidth=120,
            stretch=False,
            anchor="center")

        self.result_treeview.heading("Editorial", text="Editorial")
        self.result_treeview.column(
            "Editorial",
            width=130,
            minwidth=130,
            stretch=False,
            anchor="center")

        self.result_treeview.heading("Status", text="Status")
        self.result_treeview.column(
            "Status",
            width=50,
            minwidth=50,
            stretch=False,
            anchor="center")

        self.result_treeview.heading("Stock", text="Stock")
        self.result_treeview.column(
            "Stock",
            width=50,
            minwidth=50,
            stretch=False,
            anchor="center")

        self.result_treeview.heading("Disponibles", text="Disponibles")
        self.result_treeview.column(
            "Disponibles",
            width=100,
            minwidth=50,
            stretch=False,
            anchor="center")

    def clear_result_frame(self):
        for widget in self.winfo_children():
            widget.grid_remove()

        for item in self.result_treeview.get_children():
            self.result_treeview.delete(item)

    def get_best_width(self, treeview, data):

        try:
            style = ttk.Style()
            font_info = style.lookup("Treeview", "font")
            font = tkfont.Font(font=font_info)
        except BaseException:
            font = tkfont.nametofont("TkdefaultFont")

        max_width = 0
        for text in data:
            text_width = font.measure(str(text))

            if text_width > max_width:
                max_width = text_width

        return max_width + 15

    def block_resizing(self, event):
        return "break"

    def adjust_columns_to_content(self, title, author_name, publisher):

        def adjust_column(column_id, text, initial_width):

            if text:
                calculated_width = self.get_best_width(
                    self.result_treeview, [text])
                new_width = max(calculated_width, initial_width)
                self.result_treeview.column(
                    column_id,
                    width=new_width,
                    minwidth=initial_width,
                    stretch=False)

        adjust_column("Título", title, 230)
        adjust_column("Autor", author_name, 120)
        adjust_column("Editorial", publisher, 130)
