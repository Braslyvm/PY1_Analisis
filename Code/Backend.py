import sys
from PyQt5.QtWidgets import QApplication, QLabel

def main():
    app = QApplication(sys.argv)  # Crear la aplicación

    label = QLabel("Hola Mundo")  # Crear una etiqueta con el texto "Hola Mundo"
    label.resize(200, 50)  # Ajustar el tamaño de la ventana
    label.show()  # Mostrar la ventana

    sys.exit(app.exec_())  # Ejecutar el ciclo principal de la aplicación

if __name__ == "__main__":
    main()


print("hola")