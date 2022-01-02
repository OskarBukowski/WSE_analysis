from tkinter import *
from tkinter.ttk import *
import time


class Execute:
    user_tkinter_input = None

    def __init__(self):
        pass



    def time(self):
        def counter(*args):
            start = time.time()
            val = self(*args)
            print(f"Execution time {self.__name__}: { time.time() - start}")
            return val

        return counter

    def user_action_follower(self):
        def action_to_log(*args):
            print(f"Opened tkinter window")
            self(*args)
            print(f"Ticker written by user: {Execute.user_tkinter_input}")

        return action_to_log


    @staticmethod
    @user_action_follower
    @time
    def tkinter_open_window():
        root = Tk()
        root.title('Stock name input')
        root.geometry('200x100+500+500')

        entry = Entry(root)
        entry.pack()
        entry.focus_set()

        def user_input():
            Execute.user_tkinter_input = str(entry.get()).upper()

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
