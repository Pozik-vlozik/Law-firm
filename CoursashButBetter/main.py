from control_classes.controller_class import Controller
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ctrl = Controller()
    ctrl.start_programm()
    sys.exit(app.exec_())
