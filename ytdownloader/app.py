from PyQt5 import QtCore, QtGui, QtWidgets
from pytube import exceptions, YouTube


def set_youtube(link):
    yt = YouTube(link)
    return yt


def download_video(path, vid):
    stream = vid.streams.filter(progressive=True).get_highest_resolution()
    stream.download(path)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(399, 410)
        self.setWindowIcon(QtGui.QIcon('ytlogo.ico'))

        self.central_widget = QtWidgets.QWidget(self)

        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.yt_big_logo_label = QtWidgets.QLabel(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.yt_big_logo_label.sizePolicy().hasHeightForWidth())
        self.yt_big_logo_label.setSizePolicy(size_policy)
        self.yt_big_logo_label.setPixmap(QtGui.QPixmap("ytbiglogo.svg.png"))
        self.yt_big_logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.vertical_layout.addWidget(self.yt_big_logo_label)

        self.paste_link_label = QtWidgets.QLabel(self.central_widget)
        self.vertical_layout.addWidget(self.paste_link_label)

        self.text_link = QtWidgets.QLineEdit(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.text_link.sizePolicy().hasHeightForWidth())
        self.text_link.setSizePolicy(size_policy)
        self.vertical_layout.addWidget(self.text_link)

        self.download_button = QtWidgets.QPushButton(self.central_widget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.download_button.sizePolicy().hasHeightForWidth())
        self.download_button.setSizePolicy(size_policy)
        self.vertical_layout.addWidget(self.download_button)
        self.download_button.pressed.connect(self.save_video)

        self.setCentralWidget(self.central_widget)

        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 399, 21))

        self.file_menu = QtWidgets.QMenu(self.menu_bar)

        self.edit_menu = QtWidgets.QMenu(self.menu_bar)

        self.setMenuBar(self.menu_bar)

        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)

        self.about_action = QtWidgets.QAction(self)
        self.about_action.setStatusTip("Wyświetl informacje o autorze")
        self.about_action.setShortcut("Ctrl+A")
        self.about_action.triggered.connect(self.get_author_info)

        self.exit_action = QtWidgets.QAction(self)
        self.exit_action.setStatusTip("Wyjdź z aplikacji")
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close_app)

        self.file_menu.addAction(self.exit_action)
        self.edit_menu.addAction(self.about_action)

        self.menu_bar.addAction(self.file_menu.menuAction())
        self.menu_bar.addAction(self.edit_menu.menuAction())

        self.retranslate_ui(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self, Main_Window):
        _translate = QtCore.QCoreApplication.translate
        Main_Window.setWindowTitle(_translate("Main_Window", "Youtube Downloader"))
        self.paste_link_label.setText(_translate("Main_Window", "<html><head/><body><p align=\"center\"><span "
                                                                "style=\" font-size:20pt;\">Wklej "
                                                                "link</span></p></body></html>"))
        self.download_button.setText(_translate("Main_Window", "Pobierz"))
        self.file_menu.setTitle(_translate("Main_Window", "Plik"))
        self.edit_menu.setTitle(_translate("Main_Window", "Pomoc"))
        self.about_action.setText(_translate("Main_Window", "O autorze"))
        self.exit_action.setText(_translate("Main_Window", "Wyjście"))

    def close_app(self):
        choice = QtWidgets.QMessageBox.question(self, "Wyjście", "Czy na pewno chcesz wyjść?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()

    def get_author_info(self):
        QtWidgets.QMessageBox.information(self, "Autor", "Jakub Tomala")

    def save_video(self):
        try:
            video = set_youtube(self.text_link.text())
            path = self.get_file_path(video.title)[0]
            download_video(path, video)
            QtWidgets.QMessageBox.information(self, "Sukces", "Udało się pobrać film")
        except exceptions.RegexMatchError:
            self.error_prompt("Nieprawidłowy format linku!")
        except exceptions.VideoUnavailable:
            self.error_prompt("Film jest niedostępny")
        except:
            self.error_prompt("Wystąpił nieoczekiwany błąd");

    def error_prompt(self, text):
        QtWidgets.QMessageBox.warning(self, "Błąd", text)

    def get_file_path(self, name_of_vid):
        return QtWidgets.QFileDialog.getSaveFileName(self, "Zapisz film", name_of_vid)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
