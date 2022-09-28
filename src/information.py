import tkinter
import os
import subprocess
from tkinter import messagebox
from tkinter import simpledialog

class MainContextMenu(tkinter.Menu):
	''' Контекстное меню для внутренней области директории'''
	def __init__(self, main_window, parent):
		super(MainContextMenu, self).__init__(parent, tearoff = 0)
		self.main_window = main_window
		self.add_command(label="Создать директорию", command = self.create_dir)
		self.add_command(label="Создать файл", command = self.create_file)

	def popup_menu(self, event):
		''' функция для активации контекстного меню'''
		#если активны другие меню - отменяем их
		if self.main_window.file_context_menu:
			self.main_window.file_context_menu.unpost()
		if self.main_window.dir_context_menu:
			self.main_window.dir_context_menu.unpost()
		self.post(event.x_root, event.y_root)

	def create_dir(self):
		''' функция для создания новой директории в текущей'''
		dir_name = simpledialog.askstring("Новая директория", "Введите название новой директории")
		if dir_name:
			command = "mkdir {0}".format(dir_name).split(' ')
			#выполняем команду отдельным процессом
			process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Операция невозможна!","Отказано в доступе.")
			self.main_window.refresh_window()


	def create_file(self):
		''' функция для создания нового файла в текущей директории'''
		dir_name = simpledialog.askstring("Новый файл", "Введите название нового файла")
		if dir_name:
			command = "touch {0}".format(dir_name).split(' ')
			#выполняем команду отдельным процессом
			process = subprocess.Popen(command, cwd=self.main_window.path_text.get(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Операция невозможна!","Отказано в доступе.")
			self.main_window.refresh_window()



	def insert_to_dir(self):
		''' функция для копирования файла или директории в текущую директорию'''
		copy_obj = self.main_window.buff
		to_dir = self.main_window.path_text.get()
		if os.path.isdir(self.main_window.buff):
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['cp', '-r', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			if err:
				messagebox.showwarning("Операция невозможна!", err.decode("utf-8"))
		else:
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['cp', '-n', copy_obj, to_dir], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			out, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Операция невозможна!",err.decode("utf-8"))
		self.main_window.refresh_window()


class FileContextMenu(tkinter.Menu):
    def __init__(self, main_window, parent):
        super(FileContextMenu, self).__init__(parent, tearoff=0)
        self.main_window = main_window
        self.add_command(label="Открыть файл", command=self.open_file)
        self.add_separator()
        self.add_command(label="Копировать", command=self.copy_file)
        self.add_command(label="Переименовать", command=self.rename_file)
        self.add_separator()
        self.add_command(label="Удалить", command=self.delete_file)

    def open_file(self):
        ''' функция для открытия файла сторонними программами'''
        ext = self.main_window.take_extention_file(self.main_window.selected_file)
        full_path = self.main_window.path_text.get() + self.main_window.selected_file

        if ext in ['txt', 'py', 'html', 'css', 'js']:
            if 'mousepad' in self.main_window.all_program:
                subprocess.Popen(["mousepad", full_path], start_new_session=True)
            else:
                self.problem_message()
        elif ext == 'pdf':
            if 'evince' in self.main_window.all_program:
                subprocess.run(["evince", full_path], start_new_session=True)
            else:
                self.problem_message()
        elif ext in ['png', 'jpeg', 'jpg', 'gif']:
            if 'ristretto' in self.main_window.all_program:
                subprocess.run(["ristretto", full_path], start_new_session=True)
            else:
                self.problem_message()
        else:
            self.problem_message()

    def problem_message(self):
        messagebox.showwarning("Проблема при открытии файла", 'Прости, но я не могу открыть этот файл')

    def copy_file(self):
        ''' функция для копирования файла'''
        # заносим полный путь к файлу в буффер
        self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
        self.main_window.refresh_window()

    def delete_file(self):
        ''' функция для удаления выбранного файла'''
        full_path = self.main_window.path_text.get() + self.main_window.selected_file
        # выполняем команду отдельным процессом
        process = subprocess.Popen(['rm', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = process.communicate()
        # при возникновении ошибки выводим сообщение
        if err:
            messagebox.showwarning("Проблема при удалении файла", 'У Вас нет прав для удаления данного файла')
        self.main_window.refresh_window()

    def rename_file(self):
        ''' функция для переименования выбранного файла'''
        new_name = simpledialog.askstring("Переименование файла", "Введите новое название файла")
        if new_name:
            old_file = self.main_window.path_text.get() + self.main_window.selected_file
            new_file = self.main_window.path_text.get() + new_name
            # выполняем команду отдельным процессом
            process = subprocess.Popen(['mv', old_file, new_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, err = process.communicate()
            # при возникновении ошибки выводим сообщение
            if err:
                messagebox.showwarning("Проблема при переименовании файла",
                                       'У Вас нет прав для переименования данного файла')
            self.main_window.refresh_window()

    def popup_menu(self, event):
        ''' функция для активации контекстного меню'''
        self.post(event.x_root, event.y_root)
        # если активны другие меню - отменяем их
        if self.main_window.main_context_menu:
            self.main_window.main_context_menu.unpost()
        if self.main_window.dir_context_menu:
            self.main_window.dir_context_menu.unpost()
        self.main_window.selected_file = event.widget["text"]
class DirContextMenu(tkinter.Menu):
	def __init__(self, main_window, parent):
		super(DirContextMenu, self).__init__(parent, tearoff = 0)
		self.main_window = main_window
		self.add_command(label="Переименовать", command = self.rename_dir)
		self.add_command(label="Копировать", command = self.copy_dir)
		self.add_separator()
		self.add_command(label="Удалить", command = self.delete_dir)

	def copy_dir(self):
		''' функция для копирования директории'''
		self.main_window.buff = self.main_window.path_text.get() + self.main_window.selected_file
		self.main_window.refresh_window()


	def delete_dir(self):
		''' функция для удаления выбранной директории'''
		full_path = self.main_window.path_text.get() + self.main_window.selected_file
		if os.path.isdir(full_path):
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['rm', '-rf', full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Проблема при удалении директории", 'У Вас нет прав для удаления данной директории')
		self.main_window.refresh_window()

	def rename_dir(self):
		''' функция для переименования выбранной директории'''
		new_name = simpledialog.askstring("Переименование директории", "Введите новое название директории")
		if new_name:
			old_dir = self.main_window.path_text.get() + self.main_window.selected_file
			new_dir = self.main_window.path_text.get() + new_name
			#выполняем команду отдельным процессом
			process = subprocess.Popen(['mv', old_dir, new_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			output, err = process.communicate()
			#при возникновении ошибки выводим сообщение
			if err:
				messagebox.showwarning("Проблема при переименовании директории", 'У Вас нет прав для переименования данной директории')
			self.main_window.refresh_window()

	def popup_menu(self, event):
		''' функция для активации контекстного меню'''
		self.post(event.x_root, event.y_root)
		#если активны другие меню - отменяем их
		if self.main_window.main_context_menu:
			self.main_window.main_context_menu.unpost()
		if self.main_window.file_context_menu:
			self.main_window.file_context_menu.unpost()
		self.main_window.selected_file = event.widget["text"]
class MainWindow():
	''' Класс основного окна'''
	def __init__(self):
		self.root = tkinter.Tk()
		self.root.title("FileManager")
		self.root.resizable(width = False, height = False)
		self.root.geometry('450x300')

		self.hidden_dir = tkinter.IntVar()
		self.buff = None
		self.all_program = os.listdir('C:/')

		self.root.bind('<Button-1>', self.root_click)
		self.root.bind('<FocusOut>', self.root_click)

		#top frame
		self.title_frame = tkinter.Frame(self.root)
		self.title_frame.pack(fill = 'both', expand = True)

		#back button
		self.back_button = tkinter.Button(self.title_frame, text = "..", command = self.parent_dir, width = 1, height = 1)
		self.back_button.pack(side = 'left')

		#path entry
		self.path_text = tkinter.StringVar()
		self.path_text.set('/')
		self.current_path = tkinter.Entry(self.title_frame, textvariable = self.path_text, width = 40, state='readonly')
		self.current_path.pack(side = 'left')

		#button show/hidde hidden dir/file
		self.check_button = tkinter.Checkbutton(self.title_frame, text = "Hidden", font = ("Helvetica", 10), padx = 1, pady = 1, variable = self.hidden_dir, command = self.refresh_window)
		self.check_button.pack(side = 'left')

		#main frame
		self.main_frame = tkinter.Frame(self.root)
		self.main_frame.pack()

		# scroll bar
		self.scrollbar_vert = tkinter.Scrollbar(self.main_frame, orient="vertical")
		self.scrollbar_vert.pack(side = 'right', fill = 'y')

		self.scrollbar_hor = tkinter.Scrollbar(self.main_frame, orient="horizontal")
		self.scrollbar_hor.pack(side = 'bottom', fill = 'x')

		#canvas
		self.canvas = tkinter.Canvas(self.main_frame, borderwidth=0,  bg = 'white')
		self.inner_frame = tkinter.Frame(self.canvas,  bg = 'white')

		#команды для прокрутки
		self.scrollbar_vert["command"] = self.canvas.yview
		self.scrollbar_hor["command"] = self.canvas.xview

		#настройки для canvas
		self.canvas.configure(yscrollcommand=self.scrollbar_vert.set, xscrollcommand = self.scrollbar_hor.set, width=400, heigh=250)

		self.canvas.pack(side='left', fill='both', expand=True)
		self.canvas.create_window((0,0), window=self.inner_frame, anchor="nw")


		#отрисовываем содержимое лиректории
		self.dir_content()


	def root_click(self, event):
		''' функция для обработки события клика в root'''
		#если есть контекстные меню - отменяем
		if self.file_context_menu:
			self.file_context_menu.unpost()
		if self.main_context_menu:
			self.main_context_menu.unpost()
		if self.dir_context_menu:
			self.dir_context_menu.unpost()

	def dir_content(self):
		''' функция для определения содержимого текущей директории'''
		#содержимое в текущей директории
		dir_list = os.listdir(self.path_text.get())
		path = self.path_text.get()

		if not dir_list:
			#общее контекстное меню
			self.main_context_menu = MainContextMenu(self, self.canvas)
			self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
			if self.buff:
				self.main_context_menu.add_command(label="Вставить", command = self.main_context_menu.insert_to_dir)
			self.inner_frame.bind('<Button-3>', self.main_context_menu.popup_menu)
			#контекстное меню для файлов
			self.file_context_menu = None
			#контекстное меню для директории
			self.dir_context_menu = None
			return None

		#общее контекстное меню
		self.main_context_menu = MainContextMenu(self, self.canvas)
		self.canvas.bind('<Button-3>', self.main_context_menu.popup_menu)
		if self.buff:
			self.main_context_menu.add_command(label="Вставить", command = self.main_context_menu.insert_to_dir)
		#контекстное меню для файлов
		self.file_context_menu = FileContextMenu(self, self.inner_frame)
		#контекстное меню для директории
		self.dir_context_menu = DirContextMenu(self, self.inner_frame)


		i = 0
		for item in dir_list:

			if os.path.isdir(str(path) + item):
				#обрабатываем директории
				if os.access(str(path) + item, os.R_OK):
					if (not self.hidden_dir.get() and  not item.startswith('.')) or self.hidden_dir.get():
						photo = tkinter.PhotoImage(file ="img/folder.png")

						icon = tkinter.Label(self.inner_frame, image=photo,  bg = 'white')
						icon.image = photo
						icon.grid(row=i+1, column=0)

						folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white', cursor = 'hand1')
						folder_name.bind("<Button-1>", self.move_to_dir)
						folder_name.bind("<Button-3>", self.dir_context_menu.popup_menu)
						folder_name.grid(row=i+1, column=1, sticky='w')
				else:
					if (not self.hidden_dir.get() and not item.startswith('.')) or self.hidden_dir.get():
						photo = tkinter.PhotoImage(file ="img/folder_access.png")

						icon = tkinter.Label(self.inner_frame, image=photo,  bg = 'white')
						icon.image = photo
						icon.grid(row=i+1, column=0)

						folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
						folder_name.bind("<Button-1>", self.move_to_dir)
						folder_name.grid(row=i+1, column=1, sticky='w')

			else:
				#обрабатываем файлы
				if (not self.hidden_dir.get() and not item.startswith('.')) or self.hidden_dir.get():
					ext = self.take_extention_file(item)
					#фото, картинки
					if ext in ['jpeg', 'jpg', 'png', 'gif']:
						photo = tkinter.PhotoImage(file ="img/photo.png")

						icon = tkinter.Label(self.inner_frame, image=photo,  bg = 'white')
						icon.image = photo
						icon.grid(row=i+1, column=0)

						file_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
						file_name.grid(row=i+1, column=1, sticky='w')

						file_name.bind("<Button-3>", self.file_context_menu.popup_menu)
					else:
						#другие файлы
						if os.access(str(path) + item, os.R_OK):
							photo = tkinter.PhotoImage(file ="img/file.png")

							icon = tkinter.Label(self.inner_frame, image=photo,  bg = 'white')
							icon.image = photo
							icon.grid(row=i+1, column=0)

							folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
							folder_name.grid(row=i+1, column=1, sticky='w')

							folder_name.bind("<Button-3>", self.file_context_menu.popup_menu)

						else:
							photo = tkinter.PhotoImage(file ="img/file_access.png")

							icon = tkinter.Label(self.inner_frame, image=photo,  bg = 'white')
							icon.image = photo
							icon.grid(row=i+1, column=0)

							folder_name = tkinter.Label(self.inner_frame, text=item,  bg = 'white')
							folder_name.grid(row=i+1, column=1, sticky='w')
			i += 1
		#обновляем inner_frame и устанавливаем прокрутку для нового содержимого
		self.inner_frame.update()
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))

	def move_to_dir(self, event):
		''' функция для перехода в выбранную директорию'''
		elem = event.widget
		dir_name = elem["text"]
		fool_path = self.path_text.get() + dir_name
		if os.path.isdir(fool_path) and os.access(fool_path, os.R_OK):
			old_path = self.path_text.get()
			self.path_text.set(old_path + dir_name + '/')
			self.root_click('<Button-1>')
			self.refresh_window()


	def parent_dir(self):
		''' функция для перемещения в родительскую директорию'''
		old_path = [i for i in self.path_text.get().split('/') if i]
		new_path = '/'+'/'.join(old_path[:-1])
		if not new_path:
			new_path = '/'
		if os.path.isdir(new_path):
			if new_path == '/':
				self.path_text.set(new_path)

			else:
				self.path_text.set(new_path + '/')
			self.refresh_window()


	def take_extention_file(self, file_name):
		''' функция для получения расширения файла'''
		ls = file_name.split('.')
		if len(ls)>1:
			return ls[-1]
		else:
			return None

	def refresh_window(self):
		''' функция для обновления текущего отображения директорий/файлов'''
		for widget in self.inner_frame.winfo_children():
				widget.destroy()
		self.dir_content()
		self.canvas.yview_moveto(0)


win = MainWindow()
win.root.mainloop()