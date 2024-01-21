import sys
from PyQt6.QtWidgets import QApplication

import sys
sys.path.insert(0, './UI')
from ui import UI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec())
