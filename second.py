from tkinter import *

def hello():
    for i in range(3, 0, -1):
        print(i)

window = Tk()
window.title("My Application")
window.geometry("1000x750")
window.minsize(600, 500)
window.config(background="#30384a")

frame = Frame(window, bg="#30384a")

label_title = Label(frame, text="Bienvenue sur l'application", font=("Arial", 28), bg="#30384a", fg="white")
label_title.pack()

label_title = Label(frame, text="Ici vous pourrez compter vos tirs", font=("Arial", 20), bg="#30384a", fg="white")
label_title.pack()

button = Button(frame, text="Clique ici", font=("Arial, 25"), bg="white", fg="#30384a", command=hello)
button.pack(pady=25, fill=X)
frame.pack(expand=YES)


window.mainloop()
