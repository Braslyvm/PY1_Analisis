import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize, pyqtSignal

#view  Labyrint
class LabyrinthWidget(QWidget):
    back_to_main = pyqtSignal()  # signal to go back to main menu

    def __init__(self):
        self.matrx=""
        super().__init__()
        self.setFixedSize(1100, 800)

        # Background image
        img_path = os.path.join(os.path.dirname(__file__), "../Resources/images/WindowLabyrinth.png")
        background_pixmap = QPixmap(img_path)
        background = QLabel(self)
        background.setPixmap(background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background.setGeometry(0, 0, self.width(), self.height())
        background.lower()

        # Back button
        back_button = QPushButton("", self)
        back_button.setGeometry(900, 700, 150, 50)
        icon_path = os.path.join(os.path.dirname(__file__), "../Resources/images/back.png")
        icon = QIcon(icon_path)
        back_button.setIcon(icon)
        back_button.setIconSize(QSize(40, 40))
        back_button.setStyleSheet("background-color: red")
        back_button.clicked.connect(self.back_to_main.emit) 


         # Combobox requesting the size for the Labyrinth
        layout = QVBoxLayout()
        self.combo = QComboBox()  
        self.combo.setFixedSize(150, 50)
        self.combo.addItems(["5x5", "10x10", "15x15", "20x20", "25x25"])
        layout.addWidget(self.combo)
        self.setLayout(layout)

        # Button create new Labyrinth
        self.button_create = QPushButton("Create", self)
        self.button_create.resize(300, 70)
        self.button_create.move((self.width() - 300) // 2, (self.height() - 70) // 2 - 60)
        self.button_create.clicked.connect(self._toggle_combo)

        #Create container 
        self.container = QWidget(self)
        self.container.setFixedSize(700, 700)
        self.container.move(50, 50)

        # Layout of the container
        self.containerlayout = QVBoxLayout(self.container)
        self.containerlayout.setContentsMargins(0, 0, 0, 0)
        self.containerlayout.setSpacing(0)

        # Create the table 
        self.table = QTableWidget()
        self.containerlayout.addWidget(self.table)

        # deactivate scrollbars 
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setShowGrid(True)
        self.table.setMouseTracking(False)
        self.table.setEnabled(False) 



    # hide and show elements
    def _toggle_combo(self):
        self.matrx = self.combo.currentText()  # Guarda la selección
        self.combo.hide()
        self.button_create.hide()
        self.table.show()  
        self.container.show() 
        if (self.matrx == "5x5"):
            self.set_matrix_size(5, 5)
        if (self.matrx == "10x10"):
            self.set_matrix_size(10, 10)
        if (self.matrx == "15x15"):
            self.set_matrix_size(15, 15)
        if (self.matrx == "20x20"):
            self.set_matrix_size(20, 20)
        if (self.matrx == "25x25"):
            self.set_matrix_size(25, 25)



      

    #matrix filling
    def set_matrix_size(self, rows, cols):
        self.table.clear()
        self.table.setRowCount(rows)
        self.table.setColumnCount(cols)

        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        total_size = 700
        cell_size = total_size // max(rows, cols)

        for i in range(cols):
            self.table.setColumnWidth(i, cell_size)
        for i in range(rows):
            self.table.setRowHeight(i, cell_size)

        self.table.setFixedSize(cell_size * cols, cell_size * rows)
        for row in range(rows):
            for col in range(cols):
                item = QTableWidgetItem("")
                self.table.setItem(row, col, item)



    #restoring the interface
    def reset(self):
        self.combo.setCurrentIndex(0)  
        self.esconder = False
        self.combo.show()  
        self.button_create.show()  
        self.table.hide()
        self.container.hide()




# view  main
class MainMenuWidget(QWidget):
    def __init__(self, on_play):
        super().__init__()
        self.setFixedSize(1100, 800)

        # Background image
        img_path = os.path.join(os.path.dirname(__file__), "../Resources/images/main.png")
        background_pixmap = QPixmap(img_path)
        background = QLabel(self)
        background.setPixmap(background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background.setGeometry(0, 0, self.width(), self.height())
        background.lower()

        # Play button
        button1 = QPushButton("Play", self)
        button1.resize(300, 70)
        button1.move((self.width() - 300) // 2, (self.height() - 70) // 2 - 60)
        button1.clicked.connect(on_play)

        # Load button (does nothing for now)
        button2 = QPushButton("Load Labyrinth", self)
        button2.resize(300, 70)
        button2.move((self.width() - 300) // 2, (self.height() - 70) // 2 + 30)





class WindowMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1100, 800)
        self.setWindowTitle("Labyrinth")

        # Stacked widget to switch views
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Main menu
        self.main_menu = MainMenuWidget(self.open_labyrinth)
        self.stack.addWidget(self.main_menu)

        # Labyrinth screen
        self.labyrinth_widget = LabyrinthWidget()
        self.labyrinth_widget.back_to_main.connect(self.return_to_main)
        self.stack.addWidget(self.labyrinth_widget)

    def open_labyrinth(self):
        # Si no existe, crear una nueva instancia
        if not hasattr(self, 'labyrinth_widget') or self.labyrinth_widget is None:
            self.labyrinth_widget = LabyrinthWidget()
            self.labyrinth_widget.back_to_main.connect(self.return_to_main)
            self.stack.addWidget(self.labyrinth_widget)

        # Restablecer su estado antes de mostrarlo
        self.labyrinth_widget.reset()

        self.stack.setCurrentWidget(self.labyrinth_widget)



    # Restablecer el estado de LabyrinthWidget
    def return_to_main(self):
        self.labyrinth_widget.reset()
        self.stack.setCurrentWidget(self.main_menu)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Labyrinth")

    # Load style sheet
    file_path = os.path.join(os.path.dirname(__file__), "style.qss")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            app.setStyleSheet(f.read())

    window = WindowMain()
    window.show()
    sys.exit(app.exec_())
