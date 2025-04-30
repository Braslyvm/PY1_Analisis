import sys
import copy
import os
import Backend
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor 
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QUrl
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication


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

        img_path1 = os.path.join(os.path.dirname(__file__), "../Resources/images/fondo.png")
        background_theme_pixmap = QPixmap(img_path1)
        background_theme = QLabel(self.container)
        background_theme.setPixmap(background_theme_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background_theme.setGeometry(430, 30, 540, 540)

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
            background_theme.setGeometry(430, 30, 535, 535)
        
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
                cells = QLabel()
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

        self.msg_save = QMessageBox(self)
        self.msg_save.setObjectName("CustomMessageBox")
        self.msg_save.setWindowFlags(self.msg_save.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.msg_save.setWindowTitle('Save')
        self.msg_save.setText('Has been saved successfully')
        self.msg_save.setIcon(QMessageBox.NoIcon)
        self.msg_save.setMinimumSize(450, 300)



    """
    tickets:

    Description:
    """
    def save (self,matrix):
        name = self.name.text()
        Backend.save_matrix_to_json(matrix,name)
        self.msg_save.exec_()
        self.back_to_main.emit()


#
#
#
#
#
#
# View labyrint Automatic

class ViewLabytintPersonalized(QWidget):
    back_to_main = pyqtSignal()
    sava_Labytint = pyqtSignal(list)  

    def __init__(self, Matrix,Save =None):

        self.MatrixVL = copy.deepcopy(Matrix)
        self.start = []
        self.solution = []
        self.end = []
        self.position = 0 

        super().__init__()
        self.setFixedSize(1100, 800)

        # Background image
        img_path = os.path.join(os.path.dirname(__file__), "../Resources/images/WindowLabyrinth.png")
        background_pixmap = QPixmap(img_path)
        background = QLabel(self)
        background.setPixmap(background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background.setGeometry(0, 0, self.width(), self.height())
        background.lower()

        # Background image
        img_path1 = os.path.join(os.path.dirname(__file__), "../Resources/images/fondo.png")
        background_theme_pixmap = QPixmap(img_path1)
        background_theme = QLabel(self)
        background_theme.setPixmap(background_theme_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background_theme.setGeometry(30, 30, 740, 740)


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
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.cellClicked.connect(self.Place_Entry)

        # Matrix size
        matrix_size = len(Matrix)
        self.table.setRowCount(matrix_size)
        self.table.setColumnCount(matrix_size)

        available_size = 700  
        self.cell_size = available_size // matrix_size
        if self.cell_size == 46:
            background_theme.setGeometry(30, 30, 730, 730)
            self.container.setFixedSize(690, 690)


            
        # Configure headers
        self.table.horizontalHeader().setDefaultSectionSize(self.cell_size)
        self.table.verticalHeader().setDefaultSectionSize(self.cell_size)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.horizontalHeader().setMinimumSectionSize(1)
        self.table.verticalHeader().setMinimumSectionSize(1)


        # adjust the size of the table
        for i in range(matrix_size):
            self.table.setRowHeight(i, self.cell_size)
            self.table.setColumnWidth(i, self.cell_size)

        # Hide headers and borders
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setShowGrid(False) 

        self.images = {
            0: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/Pared.png")),
            1: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/calle.png")),
            2: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/inicio.png")),
            3: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/fin.png")),
            5: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/Pared1.png")),
            6: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/best case.png")),
            7: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/normal case.png")),
            8: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/adventurous.png")),
            9: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/worst case.png")),
            10: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/inicio2.png")),
            11: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/fin2.png"))}

        # fill in the table
        for i in range(matrix_size):
            for j in range(matrix_size):
                cell_value = Matrix[i][j]
                cells = QLabel()
                if cell_value == 0 and i < matrix_size - 1 and Matrix[i+1][j] == 1:
                    scaled_pixmap =  self.images[5].scaled(
                        self.cell_size, self.cell_size, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                else:
                    scaled_pixmap =  self.images[cell_value].scaled(
                        self.cell_size, self.cell_size, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )

                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i, j, cells)

        if Save is None:

            self.Button_save2= QPushButton("save labyrint personalized",self)
            self.Button_save2.resize(300, 70)
            self.Button_save2.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 100)
            self.Button_save2.clicked.connect(lambda: self.Sava_Labytint(self.MatrixVL))
            self.Button_save2.hide()

        self.Button_remove= QPushButton("Change Entry",self)
        self.Button_remove.resize(300, 70)
        self.Button_remove.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 300)
        self.Button_remove.clicked.connect(lambda: self.Departure_Entry(copy.deepcopy(Matrix)))
        self.Button_remove.hide()

        self.Button_solution= QPushButton("view solution",self)
        self.Button_solution.resize(300, 70)
        self.Button_solution.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 200)
        self.Button_solution.clicked.connect(self.See_Solution)
        self.Button_solution.hide()

        
        self.Button_validate= QPushButton("Validat",self)
        self.Button_validate.resize(300, 70)
        self.Button_validate.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 100 )
        self.Button_validate.clicked.connect(lambda: self.Validate_Labytint(Matrix))
        self.Button_validate.hide()
        

        #label
        self.selec_entry= QLabel("Select Entry",self)
        self.selec_entry.setAlignment(Qt.AlignCenter)
        self.selec_entry.resize(300, 30)
        self.selec_entry.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 300)
        self.selec_entry.setStyleSheet("color: white; font-size: 20px;")
        self.selec_entry.show()

        self.view_best_case = QLabel("Best Case", self)
        self.view_best_case.setAlignment(Qt.AlignCenter)
        self.view_best_case.resize(300, 30)
        self.view_best_case.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 )
        self.view_best_case.setStyleSheet("color: white; font-size: 16px;")
        self.view_best_case.hide()


        self.view_worst_case = QLabel("Worst Case", self)
        self.view_worst_case.setAlignment(Qt.AlignCenter)
        self.view_worst_case.resize(300, 30)
        self.view_worst_case.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 )
        self.view_worst_case.setStyleSheet("color: white; font-size: 16px;")
        self.view_worst_case.hide()

        self.moves_left= QPushButton("<",self)
        self.moves_left.resize(70, 70)
        self.moves_left.move((self.width() - 70) // 2 + 335, (self.height() - 70) // 2 + 50)
        self.moves_left.hide()
        self.moves_left.clicked.connect(self.Left_Solution)

        self.moves_right= QPushButton(">",self)
        self.moves_right.resize(70, 70)
        self.moves_right.move((self.width() - 70) // 2 + 415, (self.height() - 70) // 2 + 50)
        self.moves_right.hide()
        self.moves_right.clicked.connect(self.Righ_Solution)

        self.Button_back_solution= QPushButton("Back",self)
        self.Button_back_solution.resize(300, 70)
        self.Button_back_solution.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 300)
        self.Button_back_solution.clicked.connect(self.Back_Solution)
        self.Button_back_solution.hide()

        self.Button_backtrackin= QPushButton("Backtrackin",self)
        self.Button_backtrackin.resize(300, 70)
        self.Button_backtrackin.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 )
        self.Button_backtrackin.clicked.connect(self.Viw__Backtrackin)
        self.Button_backtrackin.hide()




        #
        self.msg_best = QMessageBox(self)
        self.msg_best.setObjectName("CustomMessageBox")
        self.msg_best.setWindowFlags(self.msg_best.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.msg_best.setWindowTitle('Congratulations!')
        self.msg_best.setText('You escaped in the fastest way')
        self.msg_best.setIcon(QMessageBox.NoIcon)
        self.msg_best.setMinimumSize(450, 300)


        self.msg_bad = QMessageBox(self)
        self.msg_bad.setObjectName("CustomMessageBox")
        self.msg_bad.setWindowFlags(self.msg_bad.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.msg_bad.setWindowTitle('Congratulations!')
        self.msg_bad.setText('It wasnt bad but there is a faster way.')
        self.msg_bad.setIcon(QMessageBox.NoIcon)
        self.msg_bad.setMinimumSize(450, 300)



    """
    tickets:

    Description:
    """
    def Place_Entry(self, row, column):
        self.start =[row,column]
        self.adventurous = self.start
        self.table.cellClicked.disconnect(self.Place_Entry)
        cells = QLabel()
        scaled_pixmap = self.images[2].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
        cells.setPixmap(scaled_pixmap)
        cells.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(row, column, cells)
        self.MatrixVL[row][column]=2

        self.Button_remove.show()
        self.Button_validate.show()
        self.selec_entry.hide()  
    """
    tickets:

    Description:
    """
    def Departure_Entry(self,Matrix):
        self.table.cellClicked.connect(self.Place_Entry)
        cells = QLabel()
        scaled_pixmap = self.images[Matrix[self.start[0]][self.start[1]]].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
        cells.setPixmap(scaled_pixmap)
        cells.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(self.start[0],self.start[1], cells)
        self.MatrixVL[self.start[0]][self.start[1]] = Matrix[self.start[0]][self.start[1]]
        self.start =[]
        self.adventurous = self.start
        self.Button_remove.hide()
        self.Button_validate.hide()
        self.selec_entry.show()
        self.Button_solution.hide()
        self.Button_save2.hide()     

    """
    tickets:

    Description:
    """
    def Sava_Labytint(self,Matrix):
        self.sava_Labytint.emit(Matrix)
        

    """
    tickets:

    Description:
    """
    def Validate_Labytint(self,Matrix):
        x = Backend.get_start_and_goal( copy.deepcopy(self.MatrixVL))
        self.end = x[1]
        self.start = x[0]
        """self.solution = Backend.get_all_pathsA(Matrix,self.start,self.end)
        self.solution = [[list(par) for par in sublista] for sublista in self.solution]
        self.solution.insert(0, [])"""
        self.start = list(x[0])
        self.end = list(x[1])
        self.adventurous = copy.deepcopy(self.start)

        self.solution = [[[4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6],[4, 7], [4, 8]],[[4, 1], [5, 1], [6, 1], [7, 1], [7, 2], [7, 3], [7, 4], [7, 5], [7, 6], [7, 7], [7, 8], [6, 8], [5, 8], [4, 8]]]
        self.solution.insert(0, [])

        self.solutionBk = [[[4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6],[4, 7], [4, 8]],[[4, 1],[3, 1],[2, 1],[3, 1],[4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6],[5, 6],[6, 6],[5, 6], [4, 6], [4, 7], [4, 8]]]
        resultado = []

        for sublista in self.solution :
            nueva_sublista = [list(dupla) for dupla in sublista]
            resultado.append(nueva_sublista)

        self.solution =  resultado.copy() 

        self.numbre_solution = QLabel("Number of Solutions: " + str(len(self.solution) - 1), self)
        self.numbre_solution.setAlignment(Qt.AlignCenter)
        self.numbre_solution.resize(300, 30)
        self.numbre_solution.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 100)
        self.numbre_solution.setStyleSheet("color: white; font-size: 16px;")
        self.numbre_solution.hide()

        Validate = Backend.is_connected(self.MatrixVL,self.start,self.end)
        Validate = True 
        
        if Validate == True:
            self.Button_validate.hide()
            self.Button_remove.hide()
            self.Button_solution.show()
            self.Button_save2.show()
            self.Button_remove.show()
            self.Button_backtrackin.show()
        else:
             QMessageBox.information(self, "Aviso", "NO existe solución")

        """
    tickets:

    Description:
    """
    def Restore_Path(self,path):
        for i in path[1:-1]:
            cells = QLabel()
            scaled_pixmap = self.images[1].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(i[0], i[1]  , cells)
    """
    tickets:

    Description:
    """
    def See_Solution (self):
        self.moves_left.show()
        self.moves_right.show()
        self.numbre_solution.show()
        self.Button_back_solution.show()
        self.Button_solution.hide()
        self.Button_save2.hide()
        self.Button_remove.hide()
        self.view_best_case.hide()
        self.view_worst_case.hide()
        self.Button_backtrackin.hide()
        
        

    def Back_Solution(self):
        self.Restore_Path(self.solution[self.position])
        self.moves_left.hide()
        self.moves_right.hide()
        self.Button_back_solution.hide()
        self.numbre_solution.hide()
        self.Button_solution.show()
        self.Button_save2.show()
        self.Button_remove.show()
        self.view_best_case.hide()
        self.view_worst_case.hide()
        self.Button_backtrackin.show()

    """
    tickets:

    Description:
    """
    def Viw__Backtrackin(self):
        self.Button_solution.hide()
        self.Button_save2.hide()
        self.Button_remove.hide()
        self.Button_backtrackin.hide()

        self.path = copy.deepcopy(self.solutionBk[1])
        self.step_index = 0
        self.inicio = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_step)
        self.timer.start(500)  
        
        

    def update_step(self):
        if self.step_index >= len(self.path):
            self.timer.stop()
            self.Button_solution.show()
            self.Button_save2.show()
            self.Button_remove.show()
            self.Button_backtrackin.show()
            cells = QLabel()
            scaled_pixmap = self.images[3].scaled(
                self.cell_size, self.cell_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.end[0], self.end[1], cells)
            if self.solutionBk[1] == self.solution[1]:
                self.msg_best.exec_()
            else: 
                self.msg_bad.exec_()
            return

        i = self.step_index
        
        if self.inicio == 0:
            cells = QLabel()
            scaled_pixmap = self.images[10].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.path[i][0],self.path[i][1] , cells)
            self.inicio = 1
        elif [self.path[i][0],self.path[i][1]] == self.start:
            cells = QLabel()
            scaled_pixmap = self.images[10].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.path[i][0],self.path[i][1], cells)
        elif [self.path[i][0],self.path[i][1]] == self.end:
            cells = QLabel()
            scaled_pixmap = self.images[11].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.path[i][0],self.path[i][1] , cells)
            
        else:
            cells = QLabel()
            scaled_pixmap = self.images[8].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.path[i][0],self.path[i][1] , cells)

        if i > 0:
            value = self.MatrixVL[self.path[i-1][0]][self.path[i-1][1]]
            label_prev = QLabel()
            label_prev.setPixmap(self.images[value].scaled(self.cell_size, self.cell_size, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            label_prev.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.path[i-1][0], self.path[i-1][1], label_prev)
        

        self.step_index += 1



    




    """
    tickets:

    Description:
    """
    def Righ_Solution (self):
        self.Restore_Path(self.solution[self.position])
        if (self.position == len(self.solution)-1):
            self.position = 0
        else:
            self.position +=1
        self.See_Route (self.solution[self.position])

    """
    tickets:

    Description:
    """
    def Left_Solution (self):
        self.Restore_Path(self.solution[self.position])
        if (self.position == 0):
            self.position = len(self.solution)-1
        else:
            self.position -=1
        self.See_Route (self.solution[self.position])


    """
    tickets:

    Description:
    """
    def See_Route (self,path):
        if self.position == 0:
            self.view_best_case.hide()
            self.view_worst_case.hide()
            for i in path[1:-1]:
                cells = QLabel()
                scaled_pixmap = self.images[1].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i[0], i[1]  , cells)
        elif self.position == 1:
            self.view_best_case.show()
            self.view_worst_case.hide()
            for i in path[1:-1]:
                cells = QLabel()
                scaled_pixmap = self.images[6].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i[0], i[1]  , cells)
        elif self.position == len(self.solution)-1:
            self.view_best_case.hide()
            self.view_worst_case.show()
            for i in path[1:-1]:
                cells = QLabel()
                scaled_pixmap = self.images[9].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i[0], i[1]  , cells)
        else:
            self.view_best_case.hide()
            self.view_worst_case.hide()
            for i in path[1:-1]:
                cells = QLabel()
                scaled_pixmap = self.images[7].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i[0], i[1],cells)
        
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
        self.MatrixVL = copy.deepcopy(Matrix)
        x = Backend.get_start_and_goal( copy.deepcopy(self.MatrixVL))
        self.end = x[1]
        self.start = x[0]
        self.position = 0 
        self.route = []
        self.adventurous = copy.deepcopy(self.start)
        self.solution = Backend.get_all_pathsA(Matrix,self.start,self.end)
        self.solution = [[list(par) for par in sublista] for sublista in self.solution]
        self.solution.insert(0, [])
        self.start = list(x[0])
        self.end = list(x[1])
        
        


        # Background image
        img_path = os.path.join(os.path.dirname(__file__), "../Resources/images/WindowLabyrinth.png")
        background_pixmap = QPixmap(img_path)
        background = QLabel(self)
        background.setPixmap(background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background.setGeometry(0, 0, self.width(), self.height())
        background.lower()

        # Background image
        img_path1 = os.path.join(os.path.dirname(__file__), "../Resources/images/fondo.png")
        background_theme_pixmap = QPixmap(img_path1)
        background_theme = QLabel(self)
        background_theme.setPixmap(background_theme_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        background_theme.setGeometry(30, 30, 740, 740)


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
        self.cell_size = available_size // matrix_size
        if self.cell_size == 46:
            background_theme.setGeometry(30, 30, 730, 730)
            self.container.setFixedSize(690, 690)

        
        # Configure headers
        self.table.horizontalHeader().setDefaultSectionSize(self.cell_size )
        self.table.verticalHeader().setDefaultSectionSize(self.cell_size )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.horizontalHeader().setMinimumSectionSize(1)
        self.table.verticalHeader().setMinimumSectionSize(1)


        # adjust the size of the table
        for i in range(matrix_size):
            self.table.setRowHeight(i, self.cell_size )
            self.table.setColumnWidth(i, self.cell_size )

        # Hide headers and borders
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.setFrameShape(QFrame.NoFrame)
        self.table.setShowGrid(False) 
    

  
        self.images = {
            0: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/Pared.png")),
            1: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/calle.png")),
            2: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/inicio.png")),
            3: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/fin.png")),
            5: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/Pared1.png")),
            6: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/best case.png")),
            7: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/normal case.png")),
            8: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/adventurous.png")),
            9: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/worst case.png")),
            10: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/inicio2.png")),
            11: QPixmap(os.path.join(os.path.dirname(__file__), "../Resources/images/fin2.png"))}

        # fill in the table
        for i in range(matrix_size):
            for j in range(matrix_size):
                cell_value = Matrix[i][j]
                cells = QLabel()
                if cell_value == 0 and i < matrix_size - 1 and Matrix[i+1][j] == 1:
                    scaled_pixmap = self.images[5].scaled(
                        self.cell_size , self.cell_size , 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )
                else:
                    scaled_pixmap = self.images[cell_value].scaled(
                        self.cell_size , self.cell_size , 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )

                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i, j, cells)



        if Save is None:
            self.Button_save= QPushButton("save labyrint",self)
            self.Button_save.resize(300, 70)
            self.Button_save.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 300 )
            self.Button_save.clicked.connect(lambda: self.Sava_Labytint(Matrix))

        self.Button_solution= QPushButton("view solution",self)
        self.Button_solution.resize(300, 70)
        self.Button_solution.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 200)
        self.Button_solution.clicked.connect(self.See_Solution)


        #label
        self.numbre_solution = QLabel("Number of Solutions: " + str(len(self.solution) - 1), self)
        self.numbre_solution.setAlignment(Qt.AlignCenter)
        self.numbre_solution.resize(300, 30)
        self.numbre_solution.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 100)
        self.numbre_solution.setStyleSheet("color: white; font-size: 16px;")
        self.numbre_solution.hide()


        self.view_best_case = QLabel("Best Case", self)
        self.view_best_case.setAlignment(Qt.AlignCenter)
        self.view_best_case.resize(300, 30)
        self.view_best_case.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 )
        self.view_best_case.setStyleSheet("color: white; font-size: 16px;")
        self.view_best_case.hide()


        self.view_worst_case = QLabel("Worst Case", self)
        self.view_worst_case.setAlignment(Qt.AlignCenter)
        self.view_worst_case.resize(300, 30)
        self.view_worst_case.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 )
        self.view_worst_case.setStyleSheet("color: white; font-size: 16px;")
        self.view_worst_case.hide()


        self.moves_left= QPushButton("<",self)
        self.moves_left.resize(70, 70)
        self.moves_left.move((self.width() - 70) // 2 + 335, (self.height() - 70) // 2 + 50)
        self.moves_left.hide()
        self.moves_left.clicked.connect(self.Left_Solution)

        self.moves_right= QPushButton(">",self)
        self.moves_right.resize(70, 70)
        self.moves_right.move((self.width() - 70) // 2 + 415, (self.height() - 70) // 2 + 50)
        self.moves_right.hide()
        self.moves_right.clicked.connect(self.Righ_Solution)


        #jugar 

        self.Button_start= QPushButton("play",self)
        self.Button_start.resize(300, 70)
        self.Button_start.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 100 )
        self.Button_start.clicked.connect(self.start_game)
        self.Button_start.show()

        # buttons up
        self.Button_up= QPushButton("^",self)
        self.Button_up.resize(70, 70)
        self.Button_up.move((self.width() - 70) // 2 + 365, (self.height() - 70) // 2 + 150)
        self.Button_up.clicked.connect(self.move_up)
        self.Button_up.hide()

        # buttons down
        self.Button_down= QPushButton("v",self)
        self.Button_down.resize(70, 70)
        self.Button_down.move((self.width() - 70) // 2 + 365, (self.height() - 70) // 2 + 225)
        self.Button_down.clicked.connect(self.move_down)
        self.Button_down.hide()

        # buttons right
        self.Button_right= QPushButton(">",self)
        self.Button_right.resize(70, 70)
        self.Button_right.move((self.width() - 70) // 2 + 440, (self.height() - 70) // 2 + 225)
        self.Button_right.clicked.connect(self.move_right)
        self.Button_right.hide()
       

        # buttons left
        self.Button_left= QPushButton("<",self)
        self.Button_left.resize(70, 70)
        self.Button_left.move((self.width() - 70) // 2 + 290, (self.height() - 70) // 2 + 225)
        self.Button_left.clicked.connect(self.move_left)
        self.Button_left.hide()

        self.Button_back_play= QPushButton("Back",self)
        self.Button_back_play.resize(300, 70)
        self.Button_back_play.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 300)
        self.Button_back_play.clicked.connect(self.Back_Game)
        self.Button_back_play.hide()

        #
        self.msg_best = QMessageBox(self)
        self.msg_best.setObjectName("CustomMessageBox")
        self.msg_best.setWindowFlags(self.msg_best.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.msg_best.setWindowTitle('Congratulations!')
        self.msg_best.setText('You escaped in the fastest way')
        self.msg_best.setIcon(QMessageBox.NoIcon)
        self.msg_best.setMinimumSize(450, 300)


        self.msg_bad = QMessageBox(self)
        self.msg_bad.setObjectName("CustomMessageBox")
        self.msg_bad.setWindowFlags(self.msg_bad.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.msg_bad.setWindowTitle('Congratulations!')
        self.msg_bad.setText('It wasnt bad but there is a faster way.')
        self.msg_bad.setIcon(QMessageBox.NoIcon)
        self.msg_bad.setMinimumSize(450, 300)

        self.Button_back_solution= QPushButton("Back",self)
        self.Button_back_solution.resize(300, 70)
        self.Button_back_solution.move((self.width() - 300) // 2 + 375, (self.height() - 70) // 2 - 300)
        self.Button_back_solution.clicked.connect(self.Back_Solution)
        self.Button_back_solution.hide()


    """
    tickets:

    Description:
    """
    def Back_Game(self):
        self.Button_back_play.show()
        
    """
    tickets:

    Description:
    """
    def start_game(self):
        self.Button_start.hide()
        self.Button_left.show()
        self.Button_right.show()
        self.Button_down.show()
        self.Button_up.show()
        self.Button_solution.hide()
        self.Button_start.hide()
        self.Button_back_play.show()
        self.adventurous =[]
        self.adventurous = self.start.copy() 
        self.route = []

        cells = QLabel()
        scaled_pixmap = self.images[10].scaled(
                        self.cell_size, self.cell_size, 
                        Qt.KeepAspectRatio, 
                        Qt.SmoothTransformation
                    )

        cells.setPixmap(scaled_pixmap)
        cells.setAlignment(Qt.AlignCenter)
        self.table.setCellWidget(self.adventurous[0], self.adventurous[1], cells)

    """
    tickets:

    Description:
    """
    def move_right(self):
        can = self.validation_x ("r")
        if can == False:
            print("pared")
        else:
            if ([self.adventurous[0], self.adventurous[1] + 1] == self.start):
                cells = QLabel()
                scaled_pixmap = self.images[10].scaled(
                        self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0], self.adventurous[1] + 1, cells)
            elif ([self.adventurous[0], self.adventurous[1] + 1] == self.end):
                cells = QLabel()
                scaled_pixmap = self.images[11].scaled(
                    self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0], self.adventurous[1] + 1, cells)
            else:
                cells = QLabel()
                scaled_pixmap = self.images[8].scaled(
                    self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0], self.adventurous[1] + 1, cells)

            
            cell_value = self.MatrixVL[self.adventurous[0]][self.adventurous[1]]
            cells = QLabel()
            scaled_pixmap = self.images[cell_value].scaled(
                self.cell_size, self.cell_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.adventurous[0], self.adventurous[1], cells)
            self.route.append([self.adventurous[0], self.adventurous[1]])
            self.adventurous[1] += 1
            self.Arrive()
    """
    tickets:

    Description:
    """
    def move_left(self):
        
        can = self.validation_x ("l")
        if can == False:
            
            print("pared")
        else:
            if ([self.adventurous[0], self.adventurous[1] - 1] == self.start):
                cells = QLabel()
                scaled_pixmap = self.images[10].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0], self.adventurous[1] - 1, cells)
            elif ([self.adventurous[0], self.adventurous[1] - 1] == self.end):
                cells = QLabel()
                scaled_pixmap = self.images[11].scaled(
                    self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0], self.adventurous[1] - 1, cells)
            else:
                cells = QLabel()
                scaled_pixmap = self.images[8].scaled(
                    self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0], self.adventurous[1] - 1, cells)

            cell_value = self.MatrixVL[self.adventurous[0]][self.adventurous[1]]
            cells = QLabel()
            scaled_pixmap = self.images[cell_value].scaled(
                self.cell_size, self.cell_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.adventurous[0], self.adventurous[1], cells)


            self.route.append([self.adventurous[0], self.adventurous[1]])
            self.adventurous[1] -= 1
            self.Arrive()
        

    """
    tickets:

    Description:
    """
    def move_down(self):
        can = self.validation_y("d")
        if can == False:
            print("pared")
        else:
            if ([self.adventurous[0] + 1, self.adventurous[1] ]== self.start):
                cells = QLabel()
                scaled_pixmap = self.images[10].scaled(
                    self.cell_size, self.cell_size, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0] + 1, self.adventurous[1], cells)
            elif ([self.adventurous[0] + 1, self.adventurous[1] ] == self.end):
                cells = QLabel()
                scaled_pixmap = self.images[11].scaled(
                    self.cell_size, self.cell_size, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0] + 1, self.adventurous[1], cells)
            else:
                cells = QLabel()
                scaled_pixmap = self.images[8].scaled(
                    self.cell_size, self.cell_size, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0] + 1, self.adventurous[1], cells)

            cell_value = self.MatrixVL[self.adventurous[0]][self.adventurous[1]]
            cells = QLabel()
            scaled_pixmap = self.images[cell_value].scaled(
                self.cell_size, self.cell_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.adventurous[0], self.adventurous[1], cells)

            self.route.append([self.adventurous[0], self.adventurous[1]])
            self.adventurous[0] += 1
            self.Arrive()



    """
    tickets:

    Description:
    """
    def move_up(self):
        can = self.validation_y ("u")
        if can == False:
            print("pared")
        else:
            if ([self.adventurous[0] - 1, self.adventurous[1] ] == self.start):
                cells = QLabel()
                scaled_pixmap = self.images[10].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0] - 1, self.adventurous[1], cells)
            elif ([self.adventurous[0] - 1, self.adventurous[1] ] == self.end):
                cells = QLabel()
                scaled_pixmap = self.images[11].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0] - 1, self.adventurous[1], cells)
            else: 
                cells = QLabel()
                scaled_pixmap = self.images[8].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(self.adventurous[0] - 1, self.adventurous[1], cells)

            cell_value = self.MatrixVL[self.adventurous[0]][self.adventurous[1]]
            cells = QLabel()
            scaled_pixmap = self.images[cell_value].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.adventurous[0], self.adventurous[1], cells)
            self.route.append([self.adventurous[0], self.adventurous[1]])
            self.adventurous[0] -= 1
            self.Arrive()
        """
    tickets:

    Description:
    """
    def validation_x (self,address):
        if address == "r":
            if self.adventurous[1] == len(self.MatrixVL) - 1 :
                return False
            elif self.MatrixVL[self.adventurous[0]] [self.adventurous[1]+1] == 0:
                return False
            else:
                return True
        else:
            if self.adventurous[1] == 0 :
                return False
            elif self.MatrixVL[self.adventurous[0]] [self.adventurous[1]-1] == 0:
                return False
            else:
                return True
            
    def validation_y (self,address):
        if address == "d":
            if self.adventurous[0] == len(self.MatrixVL) - 1 :
                return False
            elif self.MatrixVL[self.adventurous[0]+1] [self.adventurous[1]] == 0:
                return False
            else:
                return True
        else:
            if self.adventurous[0] == 0 :
                return False
            elif self.MatrixVL[self.adventurous[0]-1] [self.adventurous[1]] == 0:
                return False
            else:
                return True
    """
    tickets:

    Description:
    """   
    def Arrive(self):
        if self.adventurous == self.end :
            self.route +=[self.adventurous]
            if self.route == self.solution[1]:
                self.msg_best.exec_()
            else: 
                self.msg_bad.exec_()

            self.Button_start.show()
            self.Button_left.hide()
            self.Button_right.hide()
            self.Button_down.hide()
            self.Button_up.hide()
            self.Button_solution.show()
            self.Button_start.show()
            self.Button_back_play.hide()
            cells = QLabel()
            scaled_pixmap = self.images[3].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.end[0], self.end[1], cells)

    """
    tickets:

    Description:
    """
    def Sava_Labytint(self,Matrix):
        self.sava_Labytint.emit(Matrix)
    """
    tickets:

    Description:
    """
    def Restore_Path(self,path):
        for i in path[1:-1]:
            cells = QLabel()
            scaled_pixmap = self.images[1].scaled(
                            self.cell_size, self.cell_size, 
                            Qt.KeepAspectRatio, 
                            Qt.SmoothTransformation
                        )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(i[0], i[1]  , cells)
    """
    tickets:

    Description:
    """
    def See_Solution (self):
        self.Button_save.hide()
        self.Button_solution.hide()
        self.moves_left.show()
        self.moves_right.show()
        self.numbre_solution.show()
        self.Button_solution.hide()
        self.Button_back_solution.show()
        self.Button_start.hide()
    """
    tickets:

    Description:
    """
    def Back_Solution(self):
        self.Button_save.show()
        self.Restore_Path(self.solution[self.position])
        self.moves_left.hide()
        self.moves_right.hide()
        self.Button_back_solution.hide()
        self.numbre_solution.hide()
        self.Button_solution.show()
        self.view_best_case.hide()
        self.view_worst_case.hide()
        self.Button_start.show()

    """
    tickets:

    Description:
    """
    def Back_Game(self):
        self.Button_start.show()
        self.Button_left.hide()
        self.Button_right.hide()
        self.Button_down.hide()
        self.Button_up.hide()
        self.Button_solution.show()
        self.Button_start.show()
        self.Button_back_play.hide()
       
        if ([self.adventurous[0] , self.adventurous[1] ] == self.start):
            cells = QLabel()
            scaled_pixmap = self.images[2].scaled(
                self.cell_size, self.cell_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.adventurous[0], self.adventurous[1], cells)
        elif ([self.adventurous[0] , self.adventurous[1] ] == self.end):
            cells = QLabel()
            scaled_pixmap = self.images[3].scaled(
                self.cell_size, self.cell_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.adventurous[0] , self.adventurous[1], cells)
        else:
            cells = QLabel()
            scaled_pixmap = self.images[1].scaled(
                self.cell_size, self.cell_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            cells.setPixmap(scaled_pixmap)
            cells.setAlignment(Qt.AlignCenter)
            self.table.setCellWidget(self.adventurous[0] , self.adventurous[1], cells)
    """
    tickets:

    Description:
    """
    def Righ_Solution (self):
        self.Restore_Path(self.solution[self.position])
        if (self.position == len(self.solution)-1):
            self.position = 0
        else:
            self.position +=1
        self.See_Route (self.solution[self.position])

    """
    tickets:

    Description:
    """
    def Left_Solution (self):
        self.Restore_Path(self.solution[self.position])
        if (self.position == 0):
            self.position = len(self.solution)-1
        else:
            self.position -=1
        self.See_Route (self.solution[self.position])


    """
    tickets:

    Description:
    """
    def See_Route (self,path):
        if self.position == 0:
            self.view_best_case.hide()
            self.view_worst_case.hide()
            for i in path[1:-1]:
                cells = QLabel()
                scaled_pixmap = self.images[1].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i[0], i[1]  , cells)
        elif self.position == 1:
            self.view_best_case.show()
            self.view_worst_case.hide()
            for i in path[1:-1]:
                cells = QLabel()
                scaled_pixmap = self.images[6].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i[0], i[1]  , cells)
        elif self.position == len(self.solution)-1:
            self.view_best_case.hide()
            self.view_worst_case.show()
            for i in path[1:-1]:
                cells = QLabel()
                scaled_pixmap = self.images[9].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i[0], i[1]  , cells)
        else:
            self.view_best_case.hide()
            self.view_worst_case.hide()
            for i in path[1:-1]:
                cells = QLabel()
                scaled_pixmap = self.images[7].scaled(
                                self.cell_size, self.cell_size, 
                                Qt.KeepAspectRatio, 
                                Qt.SmoothTransformation
                            )
                cells.setPixmap(scaled_pixmap)
                cells.setAlignment(Qt.AlignCenter)
                self.table.setCellWidget(i[0], i[1],cells)
        


    

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
    show_labyrinth_personalized = pyqtSignal(list)
    
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

        

        Preview= QLabel("Preview",self)
        Preview.setAlignment(Qt.AlignCenter)
        Preview.resize(300, 30)
        Preview.move((self.width() - 300) // 2 + 220, (self.height() - 70) // 2 - 320)
        Preview.setStyleSheet("color: white; font-size: 20px;")
        Preview.show()

        self.labyrinth_list = QListWidget(self)
        self.labyrinth_list.setGeometry(50, 50, 300, 500)
        self.labyrinth_list.itemClicked.connect(self.Preview)
        

        self.cargar()
    
        Button_load= QPushButton("Load Automatic Labyrint",self)
        Button_load.resize(250, 50)
        Button_load.setProperty("class", "green")
        Button_load.move((self.width() - 250) // 2 + 70, (self.height() - 50) // 2 + 175)
        Button_load.clicked.connect(self.load)
        

        Button_load_Custom= QPushButton("Load Custom Labyrint",self)
        Button_load_Custom.resize(250, 50)
        Button_load_Custom.move((self.width() - 250) // 2 + 350, (self.height() - 50) // 2 + 175)
        Button_load_Custom.setProperty("class", "blue")
        Button_load_Custom.clicked.connect(self.load_custom)
            
        Button_delete= QPushButton("delete labyrint",self)
        Button_delete.resize(530, 50)
        Button_delete.move((self.width() - 510) // 2 + 200, (self.height() - 50) // 2 + 235)
        Button_delete.clicked.connect(self.delete_labyrinth)

        self.msg_delete = QMessageBox(self)
        self.msg_delete.setObjectName("CustomMessageBox")
        self.msg_delete.setWindowFlags(self.msg_delete.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.msg_delete.setWindowTitle('Delete')
        self.msg_delete.setText('has been successfully removed')
        self.msg_delete.setIcon(QMessageBox.NoIcon)
        self.msg_delete.setMinimumSize(450, 300)

    """
    tickets:

    Description:
    """
    def cargar (self):
        self.labyrinth_list.clear()  
        self.matrices = Backend.get_matrix_names_from_json()
        for nombre in self.matrices:
            self.labyrinth_list.addItem(nombre)

    """
    tickets:

    Description:
    """
    def  Preview(self, item):
        name = item.text()
        Matrix = Backend.load_matrix_from_json(name)
        # mini view  
        self.sup_container = QWidget(self)
        self.sup_container.setFixedSize(400, 400)
        self.sup_container.move((self.width() - 400) // 2 + 220, (self.height() - 400) // 2 - 100)
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

        available_size = 400  
        cell_size = available_size // matrix_size
        
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
                cells = QLabel()
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

        self.sup_container.show()



    """
    tickets:

    Description:
    """
    def load (self):
        items = self.labyrinth_list.selectedItems()
        name = items[0].text() 
        matrix = Backend.load_matrix_from_json(name)
        self.show_labyrinth.emit(matrix)

    """
    tickets:

    Description:
    """
    def load_custom (self):
        items = self.labyrinth_list.selectedItems()
        name = items[0].text() 
        matrix = Backend.load_matrix_from_json(name)

        for x in range(0, len(matrix)):
            for y in range(0, len(matrix)):
                if matrix[x][y] == 2:
                    matrix[x][y] = 1
                    break

        self.show_labyrinth_personalized.emit(matrix)
        

    """
    tickets:

    Description:
    """
    def delete_labyrinth(self):
        item = self.labyrinth_list.selectedItems()
        name = item[0].text()
        matrix = Backend.delete_matrix_from_json(name)
        self.msg_delete.exec()
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
    show_labyrinth_personalized = pyqtSignal(list) 


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


        #title source
        label_title = QLabel("Select the size and game mode of your choice", self)
        label_title.setStyleSheet("""
                    QLabel {
                        color: #ba9865;
                        font: 900 80px Garamond;  
                        font-weight: 900;         
                    }
                """)
        label_title.setFixedWidth(1000)  
        label_title.setFixedHeight(200)
        label_title.setWordWrap(True)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.move((self.width() - 1000) // 2, 30)
                                

        # Combobox requesting the size for the Labyrinth
        self.combo = QComboBox(self)
        self.combo.setFixedSize(300, 60)  # Ancho grande
        self.combo.addItems(["5x5", "10x10", "15x15", "20x20", "25x25"])
        self.combo.move((self.width() - 300) // 2, (self.height() - 60) // 2 - 100)


        # Button create Automatic Labyrinth
        self.Automatic = QPushButton("Create Labyrinth Automatic", self)
        self.Automatic.setFixedSize(300, 80)
        self.Automatic.setProperty("class", "green")
        self.Automatic.clicked.connect(self.toggle_combo)
        self.Automatic.move((self.width() - 300) // 2 - 200, (self.height() - 80) // 2 +100)

        # Button create Personalized Labyrinth
        self.Personalized = QPushButton("Create Labyrinth Custom", self)
        self.Personalized.setFixedSize(300, 80)
        self.Personalized.setProperty("class", "blue")
        self.Personalized.move((self.width() - 300) // 2 + 200, (self.height() - 80) // 2 + 100)
        self.Personalized.clicked.connect(self.toggle_combo_personalized)

    """
    tickets:

    Description:
    """
    def toggle_combo_personalized(self):
            selected_text = self.combo.currentText()
            size = int(selected_text.split('x')[0]) 
            "matrix = Backend.create_matrix_with_two_paths(size)"
            "matrix = Backend.remove_start(matrix)"
            matrix =[
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,1,0,1,0,0,0,0,0,0],
                [0,1,0,1,0,0,0,0,0,0],
                [0,1,1,1,1,1,1,1,3,0],
                [0,1,0,0,1,0,1,0,1,0],
                [0,1,0,0,1,0,1,0,1,0],
                [0,1,1,1,1,1,1,1,1,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                ]


            self.show_labyrinth_personalized.emit(matrix)

    """
    tickets:

    Description:
    """
    def toggle_combo(self):
        self.matrx = self.combo.currentText()  
        self.combo.hide()
        self.Automatic.hide()
        self.Personalized.hide()
        selected_text = self.combo.currentText()
        size = int(selected_text.split('x')[0]) 
        matrix = Backend.create_valid_matrix(size)
        self.show_labyrinth.emit(matrix)
            
    

    """
    tickets:

    Description:
    """
    def reset(self):
        self.combo.setCurrentIndex(0)  
        self.esconder = False
        self.combo.show()  
        self.Automatic.show()  
        self.Personalized.show()



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

         # View Labyrinth Automatic
        self.labyrinth_Create.show_labyrinth_personalized.connect(self.open_view_personalized)
        self.labyrinth_load.show_labyrinth_personalized.connect(self.open_view_personalized)


    #Create windows  SavaLabytint
    """
    tickets:

    Description:
    """
    def open_labyrinth_Save(self, matrix):
        self.save_labyrinth = SavaLabytint(matrix)
        self.stack.addWidget(self.save_labyrinth)
        self.save_labyrinth.back_to_main.connect(self.return_to_main)
        self.stack.setCurrentWidget(self.save_labyrinth)

    #Create windows ViewLabytint
    """
    tickets:

    Description:
    """
    def open_view_labyrinth(self, matrix):
        self.view_labyrinth = ViewLabytint(matrix)
        self.view_labyrinth.back_to_main.connect(self.return_to_main)
        self.view_labyrinth.sava_Labytint.connect(self.open_labyrinth_Save)
        self.stack.addWidget(self.view_labyrinth)
        self.stack.setCurrentWidget(self.view_labyrinth)


    #Create windows ViewLabytint
    """
    tickets:

    Description:
    """
    def open_view_personalized(self, matrix):
        self.view_labyrinth_personalized= ViewLabytintPersonalized(matrix)
        self.view_labyrinth_personalized.back_to_main.connect(self.return_to_main)
        self.view_labyrinth_personalized.sava_Labytint.connect(self.open_labyrinth_Save)
        self.stack.addWidget(self.view_labyrinth_personalized)
        self.stack.setCurrentWidget(self.view_labyrinth_personalized)


    #Create windows CreateLabyrinth
    """
    tickets:

    Description:
    """
    def open_labyrinth_Create(self):
        if not hasattr(self, 'labyrinth_Create') or self.labyrinth_Create is None:
            self.labyrinth_Create = CreateLabyrinth()
            self.labyrinth_Create.back_to_main.connect(self.return_to_main)
            self.stack.addWidget(self.labyrinth_Create)
        self.labyrinth_Create.reset()

        self.stack.setCurrentWidget(self.labyrinth_Create)

    """
    tickets:

    Description:
    """
    def open_labyrinth_Load(self):
        if not hasattr(self, 'labyrinth_load') or self.labyrinth_load is None:
            self.labyrinth_load = LoadLabytint()
            self.labyrinth_load.back_to_main.connect(self.return_to_main)
            self.stack.addWidget(self.labyrinth_load)
        
        self.labyrinth_load.cargar()  
        
        self.stack.setCurrentWidget(self.labyrinth_load)

    # resets CreateLabyrinth
    """
    tickets:

    Description:
    """
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

    
    icon_path = os.path.join(os.path.dirname(__file__), "../Resources/images/icono.png")
    app.setWindowIcon(QIcon(icon_path)) 
    window = WindowMain()
    window.setWindowIcon(QIcon(icon_path)) 

    window.show()
    sys.exit(app.exec_())
