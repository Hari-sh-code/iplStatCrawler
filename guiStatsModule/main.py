from tkinter import *

from pandas.core.window import Window

window = Tk() #instantiate an instance of a window

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Set the window size to fit the screen
window.geometry(f"{screen_width}x{screen_height}")

window.title("iplAnalyzer")

logo = PhotoImage(file="logo.png")
window.iconphoto(True, logo)

# label = Label(window,
#               text="Hello world",
#               font=("Frontierswoman",40,'bold'),
#               fg='black',
#               background="yellow",
#               relief=SUNKEN,
#               bd=10,
#               padx=20,
#               pady=20,
#               image = logo,
#               compound="bottom")
#
# label.pack()

# def submit():
#     username = entry.get()
#     print("Hello "+username)
#     entry.config(state=DISABLED)
#
# def delete():
#     entry.delete(0,END)
#
# def backspace():
#     entry.delete(len(entry.get())-1,END)
#
# entry = Entry(window,
#               font=("Arial",50),
#               fg="green",
#               bg="black",
#               show="*")
#
# entry.insert(0,"Spongebob")
#
# entry.pack(side=LEFT)
#
# submit_button = Button(window,
#                        text="submit",
#                        command=submit)
#
# delete_button = Button(window,
#                        text= "delete",
#                        command = delete)
#
# backspace_button = Button(window,
#                           text = "backspace",
#                           command = backspace)
#
# submit_button.pack(side=RIGHT)
# delete_button.pack(side=RIGHT)
# backspace_button.pack(side=RIGHT)

x = IntVar()

def display():
    if(x.get()==1):
        print("I agree")

    else:
        print("I don't agree")

check_button = Checkbutton(window,
                           text = 'I agree to the anything',
                           variable=x,
                           onvalue = 1,
                           offvalue=0,
                           command=display,
                           font = ("Arial",'20'),
                           foreground="purple",
                           background="pink",
                           activeforeground="black",
                           activebackground="yellow")

check_button.pack()



window.mainloop() #place window on computer screen, listen for events
