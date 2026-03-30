from tkinter import *


class PasswordContainer(Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.show_image = PhotoImage(file="images/ojo.png")
        self.hide_image = PhotoImage(file="images/invisible.png")

        self.password_entry = Entry(self, show="*")
        self.password_entry.pack(side=LEFT)

        self.show_hide_password_button = Button(
            self, image=self.show_image, command=lambda: self.show_hide_password(
                self.password_entry, self.show_hide_password_button))
        self.show_hide_password_button.pack(side=LEFT)

    def show_hide_password(self, entry, button):

        if entry.cget('show') == "*":
            entry.config(show="")
            button.config(image=self.hide_image)
        else:
            entry.config(show="*")
            button.config(image=self.show_image)
