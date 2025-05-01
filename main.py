# import sys

# from PyQt6.QtWidgets import QApplication
import sys

import qdarktheme
from loguru import logger
from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from pain_type import PainType
from patient_identification import PatientIdentification

# ! ---------- Logger ----------
# Set the logger as enqueue
logger.remove()
logger.add(
    sys.stderr,
    level="DEBUG",
    colorize=True,
    enqueue=True,
    backtrace=True,
)

MAIN_MARGINS: tuple[int, int, int, int] = (10, 10, 10, 10)


class MainApp(QMainWindow):
    """
    This is the main App that will contain the GUI
    It's setup as a Main window containing tabs
    Each tab is a different device:
    - Force balance
    - Optitrack (soon)
    - Robot (soon)

    It also starts the needed workers:
    - Force balance worker

    """

    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self.setWindowTitle("TEST GUI")
        self.setGeometry(
            100,
            100,
            800,
            600,
        )

        self.patient_identification: PatientIdentification = PatientIdentification()
        self.pain_type: PainType = PainType()

        # ! Init the worker thread
        self.threadpool = QtCore.QThreadPool()
        # self.threadpool.start(self.patient_identification.logic)

        self.init_ui()

    def handle_signal_disconnected(self):
        """
        TODO
        """
        print("Worker finished")

    def init_ui(self):
        # ! Base widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # ! Full main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(*MAIN_MARGINS)
        central_widget.setLayout(main_layout)

        # ! Main layout will only contain a tab widget
        tab_widget = QTabWidget()
        main_layout.addWidget(tab_widget)

        # ! First tab :Patient Identification
        tab_widget.addTab(self.patient_identification.gui, "Patient identification")

        # ! Second tab : Other
        tab_widget.addTab(self.pain_type.gui, "Pain type")

        # ! --- simple label
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 20)
        label = QLabel("Other tab")
        header_layout.addWidget(label)

        self.show()

    def closeEvent(self, a0):
        print("Closing app")
        self.patient_identification.logic.stop()
        self.threadpool.clear()
        self.threadpool.waitForDone()

        if a0 is not None:
            a0.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = MainApp(app)

    app.setStyleSheet(qdarktheme.load_stylesheet("light"))

    ret = app.exec()

    print("Exiting")
    exit(ret)
