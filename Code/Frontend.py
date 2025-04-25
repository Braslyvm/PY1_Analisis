import sys
import random
import os
import Backend
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal

from Backend import *



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


        self.name = QLineEdit(self.container)
        self.name.setGeometry(50, 100, 200, 30)
        self.name.setPlaceholderText("write...") 
 


        # Sava button
        button_Sava = QPushButton("Sava", self.container)
        button_Sava.resize(300, 70)
        button_Sava.move(50,400)
        button_Sava.clicked.connect(lambda: self.save(Matrix))

        # mini view  
        self.sup_container = QWidget(self.container)
        self.sup_container.setFixedSize(500, 500)
        self.sup_container.move(450, 50)
        self.sup_container.setStyleSheet("margin: 0; padding: 0; border: none;")

        # Layout del contenedor - más ajustado
        self.containerlayout = QVBoxLayout(self.sup_container)
        self.containerlayout.setContentsMargins(0, 0, 0, 0)
        self.containerlayout.setSpacing(0)

        # create table
        self.table = QTableWidget()
        self.containerlayout.addWidget(self.table)

        # atable adjustment
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Matrix size
        matrix_size = len(Matrix)
        self.table.setRowCount(matrix_size)
        self.table.setColumnCount(matrix_size)

        available_size = 500  
        cell_size = available_size // matrix_size
        if cell_size == 33:
            self.sup_container.setFixedSize(495, 495)
        
        # Configure headers
        self.table.horizontalHeader().setDefaultSectionSize(cell_size)
        self.table.verticalHeader().setDefaultSectionSize(cell_size)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.horizontalHeader().setMinimumSectionSize(1)
        self.table.verticalHeader().setMinimumSectionSize(1)

        # adjust the size of the table
        for i in range(matrix_size):
            self.table.setRowHeight(i, cell_size)
            self.table.setColumnWidth(i, cell_size)

        # Hide headers and borders
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setShowGrid(False)

  
        images = {
            0: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/Pared.png")),
            1: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/calle.png")),
            2: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/inicio.png")),
            3: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/fin.png")),
            5: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/Pared1.png"))}

        # fill in the table
        for i in range(matrix_size):
            for j in range(matrix_size):
                cell_value = Matrix[i][j]
                
                # Crear el QLabel
                cells = QLabel()

                # Verifica si es pared y si debajo hay una calle
                if cell_value == 0 and i < matrix_size - 1 and Matrix[i+1][j] == 1:
                    scaled_pixmap = images[5].scaled(
                        cell_size, cell_size, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                else:
                    scaled_pixmap = images[cell_value].scaled(
                        cell_size, cell_size, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )

                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i, j, cells)



    def save (self,matrix):
        name = self.name.text()
        Backend.save_matrix_to_json(matrix,name)
        self.back_to_main.emit()

   

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
    sava_Labytint = pyqtSignal(list)  

    def __init__(self, Matrix,Save =None):
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

        # create container 
        self.container = QWidget(self)
        self.container.setFixedSize(700, 700)
        self.container.move(50, 50)
        self.container.setStyleSheet("margin: 0; padding: 0; border: none;")
        self.container.setAttribute(Qt.WA_TranslucentBackground)

        # Layout del contenedor - más ajustado
        self.containerlayout = QVBoxLayout(self.container)
        self.containerlayout.setContentsMargins(0, 0, 0, 0)
        self.containerlayout.setSpacing(0)
        

        # crete table
        self.table = QTableWidget()
        self.containerlayout.addWidget(self.table)

        # atable adjustment
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Matrix size
        matrix_size = len(Matrix)
        self.table.setRowCount(matrix_size)
        self.table.setColumnCount(matrix_size)

        available_size = 700  
        cell_size = available_size // matrix_size
        if cell_size == 46:
            self.container.setFixedSize(690, 690)

        
        # Configure headers
        self.table.horizontalHeader().setDefaultSectionSize(cell_size)
        self.table.verticalHeader().setDefaultSectionSize(cell_size)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.horizontalHeader().setMinimumSectionSize(1)
        self.table.verticalHeader().setMinimumSectionSize(1)

    
         



        # adjust the size of the table
        for i in range(matrix_size):
            self.table.setRowHeight(i, cell_size)
            self.table.setColumnWidth(i, cell_size)

        # Hide headers and borders
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setShowGrid(False) 

  
        images = {
            0: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/Pared.png")),
            1: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/calle.png")),
            2: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/inicio.png")),
            3: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/fin.png")),
            5: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/Pared1.png"))}

        # fill in the table
        for i in range(matrix_size):
            for j in range(matrix_size):
                cell_value = Matrix[i][j]
                
                # Crear el QLabel
                cells = QLabel()

                # Verifica si es pared y si debajo hay una calle
                if cell_value == 0 and i < matrix_size - 1 and Matrix[i+1][j] == 1:
                    scaled_pixmap = images[5].scaled(
                        cell_size, cell_size, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                else:
                    scaled_pixmap = images[cell_value].scaled(
                        cell_size, cell_size, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )

                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i, j, cells)



        if Save is None:
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

        #Create container 
        self.container = QWidget(self)
        self.container.setFixedSize(600, 700)
        self.container.move(50, 50)
        palette = self.container.palette()
        palette.setColor(QPalette.Window, QColor(139, 69, 19, 180))  
        self.container.setPalette(palette)
        self.container.setAutoFillBackground(True)

        self.labyrinth_list = QListWidget(self.container)
        self.labyrinth_list.setGeometry(50, 50, 500, 500)
        
        self.cargar()
        
        Button_load= QPushButton("load labyrint",self)
        Button_load.resize(300, 70)
        Button_load.move((self.width() - 300) // 2 + 325, (self.height() - 70) // 2 - 100 )
        Button_load.clicked.connect(self.load)

            

        Button_delete= QPushButton("delete labyrint",self)
        Button_delete.resize(300, 70)
        Button_delete.move((self.width() - 300) // 2 + 325, (self.height() - 70) // 2)
        Button_delete.clicked.connect(self.delete_labyrinth)

    def cargar (self):
        self.labyrinth_list.clear()  
        self.matrices = Backend.get_matrix_names_from_json()
        for nombre in self.matrices:
            self.labyrinth_list.addItem(nombre)


    def load (self):
        item = self.labyrinth_list.selectedItems()
        name = item[0].text()
        matrix = Backend.load_matrix_from_json(name)
        self.show_labyrinth.emit(matrix)

    def delete_labyrinth(self):
        item = self.labyrinth_list.selectedItems()
        name = item[0].text()
        matrix = Backend.delete_matrix_from_json(name)
        self.cargar()


           
            



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
            matrix = Backend.create_valid_matrix(5)
            self.show_labyrinth.emit(matrix)
        if (self.matrx == "10x10"):
            matrix = Backend.create_valid_matrix(10)
            self.show_labyrinth.emit(matrix)
        if (self.matrx == "15x15"):
            matrix = Backend.create_valid_matrix(15)
            self.show_labyrinth.emit(matrix)
        if (self.matrx == "20x20"):
            matrix = Backend.create_valid_matrix(20)
            self.show_labyrinth.emit(matrix)
        if (self.matrx == "25x25"):
            matrix = Backend.create_valid_matrix(25)
            self.show_labyrinth.emit(matrix)
    

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
        self.labyrinth_load.show_labyrinth.connect(self.open_view_labyrinth)


    
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


    def open_labyrinth_Load(self):
        if not hasattr(self, 'labyrinth_load') or self.labyrinth_load is None:
            self.labyrinth_load = LoadLabytint()
            self.labyrinth_load.back_to_main.connect(self.return_to_main)
            self.stack.addWidget(self.labyrinth_load)
        
 
        self.labyrinth_load.cargar()  
        
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
