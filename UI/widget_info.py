import sys
from multiprocessing import Queue

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import QTimer

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


def labels_main(queues):
    app = QApplication(sys.argv)
    labels = Information()
    
    info_queue:Queue = queues["info"]

    def check_queue():
        while not info_queue.empty():
            bar = info_queue.get()
            labels.label_1.setText(bar.timestamp.strftime("%M:%S"))
            
    timer = QTimer()
    timer.timeout.connect(check_queue)
    timer.start(1)  # Adjust the interval as needed

    labels.show()
    sys.exit(app.exec())
    
# if __name__ == "__main__":
#     queue = Queue()
#     labels_main(queue)
