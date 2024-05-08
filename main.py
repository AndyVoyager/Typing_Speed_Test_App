__author__ = "AndyVoyager"

from tkinter import messagebox
from gui import App


def on_closing():
    """
    This function is called when the application is closing. It displays a confirmation dialog asking the user if they
     want to quit. If the user confirms, the application is destroyed.
    """
    if messagebox.askokcancel("Exit", "Do you want to quit?"):
        app.destroy()


app = App()
app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()
