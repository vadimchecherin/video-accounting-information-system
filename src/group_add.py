from tkinter import *
from tkinter import messagebox as mb

def group_add():
    s = entry.get()
    if not s.isdigit():
        mb.showinfo (
            "Info",
            "База данных обновлена")
    else:
        entry.delete(0, END)
        label['text'] = s

    root.destroy()
    return s

root = Tk()
root.geometry("300x100")
label1 = Label(text="Введите должность человека")
label1.pack()
entry = Entry()
entry.pack(pady=10)
Button(text='Обновить', command=group_add).pack()
label = Label(height=3)
label.pack()

root.mainloop()

