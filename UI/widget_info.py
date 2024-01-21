import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class Information(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label_1 = QLabel("Label 1")
        self.label_2 = QLabel("Label 2")
        self.label_3 = QLabel("Label 3")
        self.label_4 = QLabel("Label 4")

        layout.addWidget(self.label_1)
        layout.addWidget(self.label_2)  
        layout.addWidget(self.label_3)
        layout.addWidget(self.label_4)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Information()
    main.show()
    sys.exit(app.exec())