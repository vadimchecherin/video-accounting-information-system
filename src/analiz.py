import sys
import json
from deepface import DeepFace
import cv2
import pickle
from PySide2 import QtCore, QtGui, QtWidgets
import qimage2ndarray
import shutil
import faces_train
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox as mb
import os
import datetime
from PySide2.QtWidgets import QApplication,QMainWindow, QAction
from PySide2.QtGui import QIcon


class Window(QMainWindow):
    pause = False
    video = False

    labels = {"person_name": 1}
    with open("pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

    def __init__(self, width=640, height=480, fps=30):

        super().__init__()

        self.create_menu()

        self.show()



        QtWidgets.QWidget.__init__(self)

        self.video_size = QtCore.QSize(width, height)
        self.camera_capture = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.video_capture = cv2.VideoCapture()
        self.frame_timer = QtCore.QTimer()

        self.setup_camera(fps)
        self.fps = fps

        self.frame_label = QtWidgets.QLabel()
        self.img_label = QtWidgets.QLabel()
        self.img_label_1 = QtWidgets.QLabel()
        self.Start_button = QtWidgets.QPushButton("Start")
        self.Clean_button = QtWidgets.QPushButton("Clean")
        self.check_button = QtWidgets.QPushButton("Сheck")
        self.quit_button = QtWidgets.QPushButton("Quit")
        self.Add_person_button = QtWidgets.QPushButton("Add_person")
        self.play_pause_button = QtWidgets.QPushButton("Pause")
        self.camera_video_button = QtWidgets.QPushButton("Switch to video")
        self.main_layout = QtWidgets.QGridLayout()

        self.setup_ui()

        QtCore.QObject.connect(self.check_button, QtCore.SIGNAL("clicked()"), self.check)
        QtCore.QObject.connect(self.Start_button, QtCore.SIGNAL("clicked()"), self.display_video_stream)
        QtCore.QObject.connect(self.Clean_button, QtCore.SIGNAL("clicked()"), self.clean)
        QtCore.QObject.connect(self.Add_person_button, QtCore.SIGNAL("clicked()"), self.Add_person)
        QtCore.QObject.connect(self.play_pause_button, QtCore.SIGNAL("clicked()"), self.play_pause)
        QtCore.QObject.connect(self.camera_video_button, QtCore.SIGNAL("clicked()"), self.camera_video)

    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        viewMenu = mainMenu.addMenu("View")
        editMenu = mainMenu.addMenu("Edit")
        searchMenu = mainMenu.addMenu("Font")
        helpMenu = mainMenu.addMenu("Help")

        openAction = QAction(QIcon('open.png'), "Open", self)
        openAction.setShortcut("Ctrl+O")

        saveAction = QAction(QIcon('save.png'), "Save", self)
        saveAction.setShortcut("Ctrl+S")

        exitAction = QAction(QIcon('exit.png'), "Exit", self)
        exitAction.setShortcut("Ctrl+X")

        exitAction.triggered.connect(self.exit_app)

        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

    def exit_app(self):
        self.close()

    def setup_ui(self):

        try:
            from PyQt5.QtWinExtras import QtWin  # !!!
            myappid = 'mycompany.myproduct.subproduct.version'  # !!!
            QtWin.setCurrentProcessExplicitAppUserModelID(myappid)  # !!!
        except ImportError:
            pass

        self.setWindowTitle('Peregrinus Tuus')
        self.setWindowIcon(QtGui.QIcon('front_title.jpg'))
        self.frame_label.setFixedSize(640, 480)
        self.img_label.setFixedSize(360, 420)
        self.img_label_1.setFixedSize(360, 80)
        self.quit_button.clicked.connect(self.close_win)
        self.main_layout.addWidget(self.frame_label, 0, 0, 2, 2)
        self.main_layout.addWidget(self.img_label, 1, 2, 1, 2)
        self.main_layout.addWidget(self.img_label_1, 1, 2, 0, 2)
        self.main_layout.addWidget(self.play_pause_button, 3, 0, 1, 1)
        self.main_layout.addWidget(self.camera_video_button, 3, 1, 1, 1)
        self.main_layout.addWidget(self.Add_person_button, 3, 2, 1, 1)
        self.main_layout.addWidget(self.Start_button, 3, 3, 1, 1)
        self.main_layout.addWidget(self.Clean_button, 5, 3, 1, 1)
        self.main_layout.addWidget(self.check_button, 5, 2, 1, 1)
        self.main_layout.addWidget(self.quit_button, 5, 0, 1, 2)
        self.setLayout(self.main_layout)

    def clean(self):
        self.img_label.setText("")
        self.img_label_1.setText("")
        self.img_label.setStyleSheet("background-color: #ffffff;")
        self.img_label_1.setStyleSheet("background-color: #ffffff;")

    def play_pause(self):
        if not self.pause:
            self.frame_timer.stop()
            self.play_pause_button.setText("Play")
        else:
            self.frame_timer.start(int(1000 // self.fps))
            self.play_pause_button.setText("Pause")

        self.pause = not self.pause

    def take_screnshot_form_video(self):

        cap = cv2.VideoCapture(0)
        count = 17
        num = 0  # ограничение на количество скриншотов для обучения

        while True:
            ret, frame = cap.read()

            fps = cap.get(cv2.CAP_PROP_FPS)
            multiplier = fps * 3

            if ret:
                frame_id = int(round(cap.get(1)))
                # print(frame_id)
                cv2.imshow("frame", frame)
                k = cv2.waitKey(20)

                if frame_id % multiplier == 0:
                    cv2.imwrite(f"images/vadim/{count}.jpg", frame)
                    print(f"Take a screenshot {count}")
                    count += 1
                    num += 1
                if k == ord(" "):
                    cv2.imwrite(f"dataset_from_video/screen_{count}_extra.jpg", frame)
                    print(f"Take a extra_screenshot {count}")
                    count += 1
                    num += 1
                if num == 150:
                    break

                elif k == ord("q"):
                    print("Q pressed, closing the app")
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    def Add_person(self):
        root = Tk()
        root.withdraw()
        src = filedialog.askdirectory()
        src1 = src.split("/")[-1]
        dest = f'D:\Diplom\diplom\OpenCV-Python-Series-master\OpenCV-Python-Series-master\src\images\{src1}'
        destination = shutil.copytree(str(src), dest)

        def group_add(path_analiz):
            s = entry.get()
            if not s.isdigit():
                mb.showinfo(
                    "Info",
                    "База данных обновлена")
            else:
                entry.delete(0, END)
                label['text'] = s
            file_1 = open(f'images/{path_analiz}/group.txt', "w")
            file_1.write(s)
            file_1.close()
            root.destroy()

        root.deiconify()
        root.geometry("300x100+400+400")
        label1 = Label(text="Введите должность человека")
        label1.pack()
        entry = Entry()
        entry.pack(pady=10)

        Button(text='Добавить', command=lambda: group_add(src1)).pack()
        label = Label(height=3)
        label.pack()

        root.mainloop()
        faces_train.train()

        if not os.path.exists("dataset_from_face_check"):
            os.mkdir("dataset_from_face_check")

        for adress, dirs, files in os.walk("images"):
            for file in files:
                full = os.path.join(adress, file)
                if "1.png" or "1.jpg" in full:
                    img = cv2.imread(str(full))
                    filename = adress.split("\\")[-1]
                    path = 'dataset_from_face_check'
                    cv2.imwrite(os.path.join(path, f'{filename}.jpg'), img)
                    break

        for adress, dirs, files in os.walk("dataset_from_face_check"):
            for file in files:
                full = os.path.join(adress, file)
                filename = full.split("\\")[-1]
                filename1 = filename.split(".")[0]
                face_analyze(full, filename1)

    def camera_video(self):
        if not self.video:
            path = QtWidgets.QFileDialog.getOpenFileName(filter="Videos (*.mp4)")
            if len(path[0]) > 0:
                self.video_capture.open(path[0])
                self.camera_video_button.setText("Switch to camera")
                self.video = not self.video
        else:
            self.camera_video_button.setText("Switch to video")
            self.video_capture.release()
            self.video = not self.video

    def setup_camera(self, fps):

        self.camera_capture.set(3, self.video_size.width())
        self.camera_capture.set(4, self.video_size.height())

        self.frame_timer.timeout.connect(self.display_video_stream)
        self.frame_timer.start(int(1000 // fps))

    def display_video_stream(self):

        face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
        # eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
        # smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read("./recognizers/face-trainner.yml")

        labels = {"person_name": 1}
        with open("pickles/face-labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            labels = {v: k for k, v in og_labels.items()}

        if not self.video:
            ret, frame = self.camera_capture.read()
        else:
            ret, frame = self.video_capture.read()

        if not ret:
            return False

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if not self.video:
            frame = cv2.flip(frame, 1)
        else:
            frame = cv2.resize(frame, (self.video_size.width(), self.video_size.height()), interpolation=cv2.INTER_AREA)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            # print(x,y,w,h)
            roi_gray = gray[y:y + h, x:x + w]  # (ycord_start, ycord_end)
            roi_color = frame

            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf >= 4 and conf <= 85:
                # print(5: #id_)
                # print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

                # img_item = f"dataset_from_face/{name}.jpg"
                # img_item_frame = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)
                # cv2.imwrite(img_item, img_item_frame)

                img_item = f"dataset_from_face/{name}.jpg"
                file = open(img_item, "a")
                img_item_frame = cv2.cvtColor(roi_color, cv2.COLOR_BGR2RGB)
                cv2.imwrite(img_item, img_item_frame)
                file.close()

            color = (255, 255, 255)  # BGR 0-255
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

        image = qimage2ndarray.array2qimage(frame)
        self.frame_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def close_win(self):
        self.camera_capture.release()
        self.video_capture.release()
        cv2.destroyAllWindows()
        self.close()

    def check(self):
        original_stdout = sys.stdout
        list = []
        for adress, dirs, files in os.walk("dataset_from_face_check"):
            for file in files:
                full = os.path.join(adress, file)
                for adress_dataset_from_face, dirs, files_dataset_from_face in os.walk("dataset_from_face"):
                    for file_from_face in files_dataset_from_face:
                        path_img_1 = os.path.join(adress_dataset_from_face, file_from_face)
                        if face_verify(img_1=path_img_1, img_2=str(full)) == True:
                            with open('pass.txt', 'w') as f:
                                sys.stdout = f
                                dt = datetime.datetime.now()
                                dt_string = dt.strftime("Дата: %d/%m/%Y  Время: %H:%M:%S")
                                print(f'Найдено совпадение. \nC {file.split(".")[0]}. Пропустить!\n{dt_string} ')

                                sys.stdout = original_stdout  # Reset the standard output to its original value

                            self.img_label_1.setStyleSheet("background-color: #00ff00; font-size: 12pt;")
                            text = open('pass.txt', 'r').read()
                            self.img_label_1.setText(str(text))

                            filename = full.split("\\")[-1]
                            filename1 = filename.split(".")[0]
                            data = open(f'images/{filename1}/face_analyze.txt', 'r').read()
                            self.img_label.setText(str(data))
                            self.img_label.setStyleSheet("background-color: #00ff00;font-size: 9pt;")
                            list.append(True)
                        else:
                            list.append(False)
        print(list)
        if any(list):
            pass
        else:
            with open('detain.txt', 'w') as f:
                sys.stdout = f  # Change the standard output to the file we created.
                print('Совпадений не найдено. Нарушитель! Задержать!!!')
                sys.stdout = original_stdout  # Reset the standard output to its original value

            data = open('detain.txt', 'r').read()
            self.img_label_1.setText(str(data))
            self.img_label_1.setStyleSheet("background-color: #ff3366; font-size: 9pt;")


def face_verify(img_1, img_2):
    try:
        result_dict = DeepFace.verify(img1_path=img_1, img2_path=img_2)

        with open('result.json', 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)
        if result_dict.get('verified'):
            return True
        else:
            return False
    except Exception as _ex:
        return _ex


def face_analyze(img_path, path_analiz):
    try:
        result_dict = DeepFace.analyze(img_path=img_path, actions=['age', 'gender'])

        with open('face_analyze.json', 'w') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)

        original_stdout = sys.stdout

        with open(f'images/{path_analiz}/group.txt', 'r') as fr, open(f'images/{path_analiz}/face_analyze.txt',
                                                                      'w') as f:
            sys.stdout = f  # Change the standard output to the file we created.
            group = fr.read()
            print(f'[+] Статус: {group}')
            print(f'[+] Предпологаемый возраст: {result_dict.get("age")}')
            print(f'[+] Пол: {result_dict.get("gender")}')
            sys.stdout = original_stdout  # Reset the standard output to its original value

    except Exception as _ex:
        return _ex




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('front_title.jpg'))
    window = Window()
    window.show()
    sys.exit(app.exec_())

