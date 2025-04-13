import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class LabyrinthWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1100, 800)

        # Set the background of the labyrinth window
        ruta_img = os.path.join(os.path.dirname(__file__), "../Resources/images/WindowLabyrinth.png")
        backgroundMain = QPixmap(ruta_img)
        background = QLabel(self)
        background.setPixmap(backgroundMain.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background.setGeometry(0, 0, self.width(), self.height())
        background.lower()

class WindowMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1100, 800)
        self.setWindowTitle("Labyrinth")

        # Set the background of the main window
        ruta_img = os.path.join(os.path.dirname(__file__), "../Resources/images/main.png")
        backgroundMain = QPixmap(ruta_img)
        background = QLabel(self)
        background.setPixmap(backgroundMain.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background.setGeometry(0, 0, self.width(), self.height())
        background.lower()

        # Create buttons in the main window
        button1 = QPushButton("Play", self)
        button1.resize(300, 70) 
        button1.move(((self.width() - button1.width()) // 2), ((self.height() - button1.height()) // 2)-60)
        button1.clicked.connect(self.open_labyrinth)

        button2 = QPushButton("Load Labyrinth", self)
        button2.resize(300, 70) 
        button2.move(((self.width() - button2.width()) // 2), ((self.height() - button2.height()) // 2)+30)

        self.labyrinth_widget = None  # Starts without the labyrinth widget

    def open_labyrinth(self):
        # If there is already an instance of LabyrinthWidget, remove it
        if self.labyrinth_widget:
            self.labyrinth_widget.deleteLater()

        # Create new labyrinth content and add it to the main window
        self.labyrinth_widget = LabyrinthWidget()
        self.setCentralWidget(self.labyrinth_widget)  # Change the content of the main window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Labyrinth")

    # Load and apply the style sheet
    file_path = os.path.join(os.path.dirname(__file__), "style.qss")
    with open(file_path, "r") as f:
        app.setStyleSheet(f.read())

    ui = WindowMain()
    ui.show()
    sys.exit(app.exec_())
