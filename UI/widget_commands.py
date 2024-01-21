import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class Commands(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.button_1 = QPushButton("Button 1")
        self.button_2 = QPushButton("Button 2")
        self.button_3 = QPushButton("Button 3")
        self.button_4 = QPushButton("Button 4")

        self.button_1.clicked.connect(self.on_button_1_clicked)
        self.button_2.clicked.connect(self.on_button_2_clicked)
        self.button_3.clicked.connect(self.on_button_3_clicked)
        self.button_4.clicked.connect(self.on_button_4_clicked)
        

        layout.addWidget(self.button_1)
        layout.addWidget(self.button_2)
        layout.addWidget(self.button_3)  
        layout.addWidget(self.button_4)

        self.setLayout(layout)


    def on_button_1_clicked(self):
        print("Button 1 clicked")

    def on_button_2_clicked(self):
        print("Button 2 clicked") 

    def on_button_3_clicked(self):
        print("Button 3 clicked")

    def on_button_4_clicked(self):
        print("Button 4 clicked")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Commands()
    main.show()
    sys.exit(app.exec())