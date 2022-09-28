from tkinter import *
from tkinter import messagebox as mb
import shutil
import os
import win32api
import win32print


def update_path_field(path_field, path):
    """Обновляет поле со строкой пути для активного окна.
    
    Arguments:
        path_field {Entry} -- Поле со строкой пути.
        path {str} -- Путь.
    """

    path_field.delete(0, "end")
    path_field.insert(0, path)


def update_list_box(list_box):
    """Обновляет список файлов и папок в ListBox.
    
    Arguments:
        list_box {Listbox} -- Объект tkinter.ListBox.
    """

    list_box.delete(0, "end")
    path = path_field.get()
    dir_content = os.listdir(path)

    for item in dir_content:
        # Проверить, файл это или директория
        if os.path.isdir(path + item):  # Если директория
            list_box.insert("end", item + "/")  # В конец добавить /
        elif os.path.isfile(path + item):  # Перестраховывамся. Если попадает какое-то дерьмо, не добавляем
            list_box.insert("end", item)


def update_panels():
    """Обновляет обе панели сразу."""

    global left_panel_path, right_panel_path, left_panel, right_panel

    left_panel.delete(0, "end")
    right_panel.delete(0, "end")
    left_panel_content = os.listdir(left_panel_path)
    right_panel_content = os.listdir(right_panel_path)

    for left in left_panel_content:
        if os.path.isdir(left_panel_path + left):
            left_panel.insert("end", left + "/")
        elif os.path.isfile(left_panel_path + left):
            left_panel.insert("end", left)
    
    for right in right_panel_content:
        if os.path.isdir(right_panel_path + right):
            right_panel.insert("end", right + "/")
        elif os.path.isfile(right_panel_path + right):
            right_panel.insert("end", right)

def left_panel_clicked(event):
    """Обрабатывает клик левой кнопкой мыши по левой панели.
    
    Arguments:
        event {Event} -- Событие клика левой кнопкой мыши.
    """

    global last_active_panel, path_field,  left_panel_path

    if last_active_panel == "r":  # Проверка нужна, чтобы не затирать путь лишний раз
        last_active_panel = "l" # Запоминаем последнюю использованную панель
        update_path_field(path_field, left_panel_path)



def right_panel_clicked(event):
    """Обрабатывает клик левой кнопкой мыши по правой панели.

    Arguments:
        event {Event} -- Событие клика левой кнопкой мыши.
    """

    global last_active_panel, path_field, right_panel_path

    if last_active_panel == "l":  # Проверка нужна, чтобы не затирать путь лишний раз
        last_active_panel = "r"  # Возможно, это можно сделать средствами Tk, но нет
        update_path_field(path_field, right_panel_path)




def left_panel_doubleclicked(event):
    """Обрабатывает двойной клик в левой панели.
    
    Arguments:
        event {Event} -- Событие двойного клика левой кнопкой мыши.
    """
    global path_field, right_panel, left_panel_path

    current_path = path_field.get()
    new_path = left_panel.get(left_panel.curselection())

    if os.path.isdir(current_path + new_path):
        left_panel_path = current_path + new_path
        update_path_field(path_field, left_panel_path)
        update_list_box(left_panel)

    src1 = left_panel_path.replace('/', '\\')
    src = src1.split("\\")[-2]
    string = src1 + src + ".txt"

    def print_textbox():
        win32api.ShellExecute(0,"printto",string,'"%s"' % win32print.GetDefaultPrinter(),".",0)

    try:
        with open(string, 'r') as file:
            lst = file.read()


        ws = Tk()
        ws.title('Информация для печати')
        ws.geometry('400x300')

        frame = Frame(ws)
        text_box = Text(
            frame,
            height=15,
            width=45,
            wrap='word'
        )
        text_box.insert('end', lst)
        text_box.pack(side=LEFT, expand=True)

        sb = Scrollbar(frame)
        sb.pack(side=RIGHT, fill=BOTH)

        text_box.config(yscrollcommand=sb.set)
        sb.config(command=text_box.yview)

        frame.pack(expand=True)
        Button(ws,
                   text="Печать",
                   width=15,
                   height=2,
                   command=print_textbox
               ).pack(expand=True)
    except FileNotFoundError:
        print('')




def right_panel_doubleclicked(event):
    """Обрабатывает двойной клик в правой панели.
    
    Arguments:
        event {Event} -- Событие двойного клика левой кнопкой мыши.
    """
    global path_field, right_panel, right_panel_path

    current_path = path_field.get()
    new_path = right_panel.get(right_panel.curselection())

    if os.path.isdir(current_path + new_path):
        right_panel_path = current_path + new_path
        update_path_field(path_field, right_panel_path)
        update_list_box(right_panel)


def go_button_clicked(event):
    """Обрабатывает нажатие на кнопку GO.
    
    Arguments:
        event {Event} -- Событие нажатия на кнопку.
    """

    global left_panel_path, right_panel_path

    path = path_field.get()



    if os.path.isdir(path) == False:  # Если в строке пути не путь к директории - ничего не делать
        return

    if path[-1] != "/":
        path += "/"  # Если пользователь так не любит ставить палки в конце, я сделаю это за него
        update_path_field(path_field, path)

    if last_active_panel == "l":
        left_panel_path = path
        update_list_box(left_panel)
    elif last_active_panel == "r":
        right_panel_path = path
        update_list_box(right_panel)


def back_button_clicked(event):
    """Обрабатывает нажатие на кнопку BACK.
    
    Arguments:
        event {Event} -- Событие нажатия на кнопку.
    """

    global left_panel_path, right_panel_path

    path = path_field.get()
    splited_path = path.split("/")  # Разделить путь, чтобы убрать из него верхнюю директорию
    new_path = "D:\Diplom\diplom\OpenCV-Python-Series-master\OpenCV-Python-Series-master\src\information\\"
    update_path_field(path_field, new_path)

    if last_active_panel == "l":
        left_panel_path = new_path
        update_list_box(left_panel)
    elif last_active_panel == "r":
        right_panel_path = new_path
        update_list_box(right_panel)


def copytree(src, dst, symlinks=False, ignore=None):
    """Рекурсивно коприрует указанную директорию. 
    Обертка для shutil.copytree(). У оригинала есть проблемы с копированием.
    
    Arguments:
        src {str} -- Источник.
        dst {str} -- Получатель.
    
    Keyword Arguments:
        symlinks {bool} -- Копировать символические ссылки. (default: {False})
        ignore {None} -- Игнорировать ошибки. (default: {None})
    """

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def copy_button_clicked(event):
    """Обрабатывает нажатие на кнопку Copy.

    Arguments:
        event {Event} -- Событие нажатия на кнопку.
    """

    message = ""
    item_path = ""
    target_path = ""

    if last_active_panel == "l":
        item = left_panel.get(left_panel.curselection())
        message = item + "\nFrom: " + left_panel_path + "\nTo: " + right_panel_path
        item_path = left_panel_path + item
        target_path = right_panel_path + item
    elif last_active_panel == "r":
        item = right_panel.get(right_panel.curselection())  # Получить выбранный элемент
        message = item + "\nFrom: " + right_panel_path + "\nTo: " + left_panel_path
        item_path = right_panel_path + item
        target_path = left_panel_path + item

    answer = mb.askyesno(title="Copy", message=message)  # Получить ответ от диалогового окна

    if answer == True:
        if os.path.isfile(item_path):
            shutil.copyfile(item_path, target_path)
        elif os.path.isdir(item_path):
            if not os.listdir(item_path):  # Проверить, пустая ли папка
                os.makedirs(target_path)
            else:
                copytree(item_path, target_path)  # Обратите внимание! Используется локальный метод!
    update_panels()


def delete_button_clicked(event):
    """Обрабатывает нажатие на кнопку Del.

    Arguments:
        event {Event} -- Событие нажатия на кнопку.
    """

    message = ""
    item_path = ""

    if last_active_panel == "l":
        item = left_panel.get(left_panel.curselection())
        message = item + "\nFrom: " + left_panel_path
        item_path = left_panel_path + item
    elif last_active_panel == "r":
        item = right_panel.get(right_panel.curselection())  # Получить выбранный элемент
        message = item + "\nFrom: " + right_panel_path
        item_path = right_panel_path + item

    answer = mb.askyesno(title="Удалить", message=message)  # Получить ответ от диалогового окна

    if answer == True:
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    update_panels()


def move_button_clicked(event):
    """Обрабатывает нажатие на кнопку Move.

    Arguments:
        event {Event} -- Событие нажатия на кнопку.
    """

    message = ""
    item_path = ""
    target_path = ""

    if last_active_panel == "l":
        item = left_panel.get(left_panel.curselection())
        message = item + "\nFrom: " + left_panel_path + "\nTo: " + right_panel_path
        item_path = left_panel_path + item
        target_path = right_panel_path + item
    elif last_active_panel == "r":
        item = right_panel.get(right_panel.curselection())  # Получить выбранный элемент
        message = item + "\nFrom: " + right_panel_path + "\nTo: " + left_panel_path
        item_path = right_panel_path + item
        target_path = left_panel_path + item

    answer = mb.askyesno(title="Move", message=message)  # Получить ответ от диалогового окна

    if answer == True:
        if os.path.isfile(item_path):
            shutil.copyfile(item_path, target_path)
            os.remove(item_path)
        elif os.path.isdir(item_path):
            if not os.listdir(item_path):  # Проверить, пустая ли папка
                os.makedirs(target_path) # Если пустая, то создать такую же в месте назначения
                #os.removedirs(item_path)  # Удаляет пустую папку, а также ее пустую мать, бабушку и дочь, если есть
                shutil.rmtree(item_path)
            else:
                copytree(item_path, target_path)
                shutil.rmtree(item_path)
    update_panels()


def rename_button_clicked(event):
    """Обрабатывает нажатие на кнопку Rename.

    Arguments:
        event {Event} -- Событие нажатия на кнопку.
    """

    message = ""
    item_path = ""
    target_path = ""
    global path_field, left_panel_path, right_panel_path

    if last_active_panel == "l":
        item = left_panel.get(left_panel.curselection())
        item_path = left_panel_path + item
        target_path = left_panel_path + path_field.get()
        message = item + "\nFrom: " + item_path + "\nTo: " + target_path
        update_path_field(path_field, left_panel_path)
    elif last_active_panel == "r":
        item = right_panel.get(right_panel.curselection())  # Получить выбранный элемент
        item_path = right_panel_path + item
        target_path = right_panel_path + path_field.get()
        message = item + "\nFrom: " + item_path + "\nTo: " + target_path
        update_path_field(path_field, right_panel_path)

    answer = mb.askyesno(title="Переименовать", message=message)  # Получить ответ от диалогового окна

    if answer == True:
        if os.path.isfile(item_path):
            os.rename(item_path, target_path)
        elif os.path.isdir(item_path):
            os.rename(item_path, target_path)
    update_panels()


def mkdir_button_clicked(event):
    """Обрабатывает нажатие на кнопку MkDir.

    Arguments:
        event {Event} -- Событие нажатия на кнопку.
    """

    global path_field, left_panel_path, right_panel_path

    target_path = path_field.get()
    if last_active_panel == "l":
        update_path_field(path_field, left_panel_path)
    elif last_active_panel == "r":
        update_path_field(path_field, right_panel_path)
    if os.path.isdir(target_path) or os.path.isfile(target_path):
        return

    message = "Создать папку " + target_path
    answer = mb.askyesno(title="Создать папку", message=message)

    if answer == True:
        os.makedirs(target_path)
    update_panels()


def exit_button_clicked(event):
    """Обрабатывает нажатие на кнопку Exit.
    
    Arguments:
        event {Event} -- Событие нажатия на кнопку.
    """

    answer = mb.askyesno(title="Выход", message="Вы действительно хотите выйти?")
    if answer:
        exit(0)


if __name__ == "__main__":
    # Создание главного окна и размещение на нем виджетов
    main_window = Tk()
    main_window.title("Information")
    main_window.resizable(False, False)

    # Установка строки для отображения пути
    path_field = Entry(main_window)
    path_field.grid(row=0, column=1, columnspan=4, sticky="nwes")

    # Установка кнопки перехода на директорию выше
    back_button = Button(main_window, text="Назад")
    back_button.grid(row=0, column=0, sticky="nwes")
    back_button.bind("<Button-1>", back_button_clicked)

    # Установка кнопки GO справа от поля со строкой пути
    go_button = Button(main_window, text="Вперед")
    go_button.grid(row=0, column=5, sticky="nwes")
    # Привязать обработчик нажатия кнопки
    go_button.bind("<Button-1>", go_button_clicked)

    # Установка правой и левой панелей
    left_panel = Listbox(main_window, heigh=15, width=50, selectmode="single")
    left_panel.grid(row=1, column=0, columnspan=5, sticky="nwes")
    left_scroll = Scrollbar(command=left_panel.yview)  # Сделать скролл, но не добавить в окно. Гениально.

    # Установка нижних кнопок
    # print_button = Button(main_window, text="Печать", width=8)
    exit_button = Button(main_window, text="Выход", width=8)
    bottom_buttons = [exit_button]
    count = 0
    for button in bottom_buttons:
        button.grid(row=2, column=count, sticky="nwes")
        count += 1

    # print_button.bind("<Button-1>", copy_button_clicked)
    exit_button.bind("<Button-1>", exit_button_clicked)

    # Определить ОС, на которой работает pyfiman
    if os.name == "posix":
        start_path = "D:\Diplom\diplom\OpenCV-Python-Series-master\OpenCV-Python-Series-master\src"  # В качестве пути взять root
    elif os.name == "nt":  # Все равно упадет, просто не сразу
        start_path = "D:\Diplom\diplom\OpenCV-Python-Series-master\OpenCV-Python-Series-master\src\information\\"
    else:
        exit(1)

    # Установить стандартные пути для панелей
    left_panel_path = start_path

    update_path_field(path_field, start_path)

    # Привязать обработчики клика по панелям
    last_active_panel = "l"
    left_panel.bind("<Button-1>", left_panel_clicked)
    left_panel.bind("<Double-Button-1>", left_panel_doubleclicked)

    update_list_box(left_panel)

    mainloop()
