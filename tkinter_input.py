from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk, Image


class Execute:
    def __init__(self):
        pass

    @staticmethod
    def tkinter_open_window():
        root = Tk()
        root.title('Stock name input')
        root.geometry('200x100+500+500')

        entry = Entry(root)
        entry.pack()
        entry.focus_set()

        def user_input():
            Execute.input = entry.get()

        style = Style(root)
        style.theme_use('default')
        style.configure('W.TButton',
                        font=('arial', 12, 'bold'),
                        background='blue',
                        foreground='white'
                        )

        button = Button(root,
                        text='Confirm',
                        command=lambda: [user_input(), root.destroy()],
                        style='W.TButton'
                        ).pack(side='bottom')

        root.mainloop()





#### comment with nice styling


# def darkstyle(root):
#     ''' Return a dark style to the window'''
#
#     style = Style(root)
#     root.tk.call('source', 'azure dark/azure dark.tcl')
#     style.theme_use('azure')
#     style.configure("Accentbutton", foreground='white')
#     style.configure("Togglebutton", foreground='white')
#
#     return style
#
#
# def main_window():
#     """ The window with the darkstyle """
#     root = Tk()
#     root.title("My App")
#     root.resizable(False),
#     img = PhotoImage(file=(Image.open("background.jpg")))
#
#     style = darkstyle(root)
#
#     lab = Label(
#         root,
#         text="Write here the stock name",
#         compound="center",
#         font="arial 50",
#         image=img)
#
#     lab.pack(fill="both", expand=1)
#
#     button = Button(
#         root,
#         text="Confirm",
#         style="Accentbutton",
#         command=lambda: [print_text(), root.destroy()]
#         )
#
#     button.place(relx=0.43, rely=0.7, width=100, height=30)
#
#     root.mainloop()
#
#
# main_window()
