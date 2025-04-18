import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal



class SavaLabytint(QWidget):
    back_to_main = pyqtSignal()
    def __init__(self,Matrix):
        super().__init__()
        self.setFixedSize(1100, 800)

        # Background image
        img_path = os.path.join(os.path.dirname(__file__), "../Resources/images/waiting screen.png")
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

        #Create container 
        self.container = QWidget(self)
        self.container.setFixedSize(1000, 600)
        self.container.move(50, 50)
        palette = self.container.palette()
        palette.setColor(QPalette.Window, QColor(139, 69, 19, 180))  #
        self.container.setPalette(palette)
        self.container.setAutoFillBackground(True)

        label_Save = QLabel("Write the name of the Labytint", self.container)
        label_Save.move(50, 50)  


        name = QLineEdit(self.container)
        name.setGeometry(50, 100, 200, 30)
        name.setPlaceholderText("write...") 
 


        # Sava button
        button_Sava = QPushButton("Sava", self.container)
        button_Sava.resize(300, 70)
        button_Sava.move(50,400)


        # mini view 
        self.sup_container = QWidget(self.container)
        self.sup_container.setFixedSize(500, 500)
        self.sup_container.move(450, 50)

        # Layout of the sup_container
        self.containerlayout = QVBoxLayout(self.sup_container)
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

        self.table.clear()
        self.table.setRowCount(len(Matrix))
        self.table.setColumnCount(len(Matrix))

        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        total_size = 500
        cell_size = total_size // max(len(Matrix), len(Matrix))

        for i in range(len(Matrix)):
            self.table.setColumnWidth(i, cell_size)
        for i in range(len(Matrix)):
            self.table.setRowHeight(i, cell_size)

        self.table.setFixedSize(cell_size * len(Matrix), cell_size * len(Matrix))
        for row in range(len(Matrix)):
            for col in range(len(Matrix)):
                item = QTableWidgetItem("")
                self.table.setItem(row, col, item)








#
#
#
#
#
#
#
#
#View labyrint
class ViewLabytint(QWidget):
    back_to_main = pyqtSignal()
    sava_Labytint =pyqtSignal(list)  # signal to go back to main menu
    def __init__(self,Matrix):
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

        self.table.clear()
        self.table.setRowCount(len(Matrix))
        self.table.setColumnCount(len(Matrix))

        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)

        total_size = 700
        cell_size = total_size // max(len(Matrix), len(Matrix))

        for i in range(len(Matrix)):
            self.table.setColumnWidth(i, cell_size)
        for i in range(len(Matrix)):
            self.table.setRowHeight(i, cell_size)

        self.table.setFixedSize(cell_size * len(Matrix), cell_size * len(Matrix))
        for row in range(len(Matrix)):
            for col in range(len(Matrix)):
                item = QTableWidgetItem("")
                self.table.setItem(row, col, item)



        Button_save= QPushButton("save labyrint",self)
        Button_save.resize(300, 70)
        Button_save.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 100 )
        Button_save.clicked.connect(lambda: self.Sava_Labytint(Matrix))
        


        Button_solution= QPushButton("view solution",self)
        Button_solution.resize(300, 70)
        Button_solution.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2)





    def Sava_Labytint(self,Matrix):
        self.sava_Labytint.emit(Matrix)


    






#
#
#
#
#
#
#Load labyrint
class LoadLabytint(QWidget):
    back_to_main = pyqtSignal()  # signal to go back to main menu
    
    def __init__(self):
        super().__init__()
        self.setFixedSize(1100, 800)

        # Background image
        img_path = os.path.join(os.path.dirname(__file__), "../Resources/images/waiting screen.png")
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
        


        



#
#
#
#
#
#
#view  Create Labyrint
class CreateLabyrinth(QWidget):
    back_to_main = pyqtSignal()  # signal to go back to main menu
    show_labyrinth = pyqtSignal(list) 

    def __init__(self):
        super().__init__()
        self.setFixedSize(1100, 800)

        # Background image
        img_path = os.path.join(os.path.dirname(__file__), "../Resources/images/waiting screen.png")
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


        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Horizontal layout for ComboBox and Create button
        h_layout = QHBoxLayout()

        # Combobox requesting the size for the Labyrinth
        self.combo = QComboBox(self)
        self.combo.setFixedSize(150, 50)
        self.combo.addItems(["5x5", "10x10", "15x15", "20x20", "25x25"])
        h_layout.addWidget(self.combo)

        # Button create new Labyrinth
        self.button_create = QPushButton("Create Labyrinth", self)
        self.button_create.setFixedSize(300, 70)
        self.button_create.setStyleSheet("background-color: green; color: white; font-size: 16px;")
        self.button_create.clicked.connect(self._toggle_combo)
        h_layout.addWidget(self.button_create)

        # Add horizontal layout to main layout
        main_layout.addLayout(h_layout)


        # Set layout
        self.setLayout(main_layout)


        



    # hide and show elements
    def _toggle_combo(self):
        self.matrx = self.combo.currentText()  # Guarda la selección
        self.combo.hide()
        self.button_create.hide()

        if (self.matrx == "5x5"):
            matrix = self.generar_matriz(5)
            self.show_labyrinth.emit(matrix)
        if (self.matrx == "10x10"):
            matrix = self.generar_matriz(10)
            self.show_labyrinth.emit(matrix)
        if (self.matrx == "15x15"):
            matrix = self.generar_matriz(15)
            self.show_labyrinth.emit(matrix)
        if (self.matrx == "20x20"):
            matrix = self.generar_matriz(20)
            self.show_labyrinth.emit(matrix)
        if (self.matrx == "25x25"):
            matrix = self.generar_matriz(25)
            self.show_labyrinth.emit(matrix)



    def generar_matriz(self,n):
        return [[(i * n + j + 1) for j in range(n)] for i in range(n)]
    

    #restoring the interface
    def reset(self):
        self.combo.setCurrentIndex(0)  
        self.esconder = False
        self.combo.show()  
        self.button_create.show()  



#
#
#
#
#
#
# view  main
class MainMenuWidget(QWidget):
    def __init__(self, on_play,on_load):
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
        button2.clicked.connect(on_load)




#
#
#
#
#
#
class WindowMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1100, 800)
        self.setWindowTitle("Labyrinth")

        # Stacked widget to switch views
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Main menu
        self.main_menu = MainMenuWidget(self.open_labyrinth_Create, self.open_labyrinth_Load)
        self.stack.addWidget(self.main_menu)

        # Load Labyrinth screen
        self.labyrinth_load = LoadLabytint()
        self.labyrinth_load.back_to_main.connect(self.return_to_main)
        self.stack.addWidget(self.labyrinth_load)

        # Labyrinth screen
        self.labyrinth_Create = CreateLabyrinth()
        self.labyrinth_Create.back_to_main.connect(self.return_to_main)
        self.stack.addWidget(self.labyrinth_Create)


        # View Labyrinth
        self.labyrinth_Create.show_labyrinth.connect(self.open_view_labyrinth)


    
    #Create windows  SavaLabytint
    def open_labyrinth_Save(self, matrix):
        self.save_labyrinth = SavaLabytint(matrix)
        self.stack.addWidget(self.save_labyrinth)
        self.save_labyrinth.back_to_main.connect(self.return_to_main)
        self.stack.setCurrentWidget(self.save_labyrinth)



    #Create windows ViewLabytint
    def open_view_labyrinth(self, matrix):
        self.view_labyrinth = ViewLabytint(matrix)
        self.view_labyrinth.back_to_main.connect(self.return_to_main)
        self.view_labyrinth.sava_Labytint.connect(self.open_labyrinth_Save)
        self.stack.addWidget(self.view_labyrinth)
        self.stack.setCurrentWidget(self.view_labyrinth)


    #Create windows CreateLabyrinth
    def open_labyrinth_Create(self):
        if not hasattr(self, 'labyrinth_Create') or self.labyrinth_Create is None:
            self.labyrinth_Create = CreateLabyrinth()
            self.labyrinth_Create.back_to_main.connect(self.return_to_main)
            self.stack.addWidget(self.labyrinth_Create)
        self.labyrinth_Create.reset()

        self.stack.setCurrentWidget(self.labyrinth_Create)

    #Create windows LoadLabytint
    def open_labyrinth_Load(self):
        if not hasattr(self, 'labyrinth_load') or self.labyrinth_load is None:
            self.labyrinth_load = LoadLabytint()
            self.labyrinth_load.back_to_main.connect(self.return_to_main)
            self.stack.addWidget(self.labyrinth_load)

        self.stack.setCurrentWidget(self.labyrinth_load)

    # resets CreateLabyrinth
    def return_to_main(self):
        self.labyrinth_Create.reset()
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
