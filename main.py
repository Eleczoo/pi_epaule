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

from other_pain import OtherPain
from pain_intensity import PainIntensity
from pain_localization import PainLocalization
from pain_type import PainType
from palpation import Palpation
from patient_identification import PatientIdentification
from toaster import Toaster

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
        # ! Init dictionary to store all patient data
        self.patient_data: dict[str] = {}
        self.patient_data["pain_count"] = 0

        # ! Init tab widget to switch between different tabs with buttons
        self.tab_widget: QWidget = QTabWidget()

        self.toaster = Toaster(self)

        # ! Init the different tabs
        self.patient_identification: PatientIdentification = PatientIdentification(
            self.patient_data,
            self.tab_widget,
            self.toaster,
        )
        self.pain_type: PainType = PainType(
            self.patient_data,
            self.tab_widget,
            self.toaster,
        )
        self.pain_localization: PainLocalization = PainLocalization(
            self.patient_data,
            self.tab_widget,
            self.toaster,
        )
        self.palpation: Palpation = Palpation(
            self.patient_data,
            self.tab_widget,
            self.toaster,
        )
        self.pain_intensity: PainIntensity = PainIntensity(
            self.patient_data,
            self.tab_widget,
            self.toaster,
        )
        self.other_pain: OtherPain = OtherPain(
            self.patient_data,
            self.tab_widget,
            self.toaster,
        )

        # ! Init the worker thread
        self.threadpool = QtCore.QThreadPool()
        self.threadpool.start(self.pain_localization.logic)

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
        main_layout.addWidget(self.tab_widget)
        self.tab_widget.tabBar().hide()  # hide the tab bar

        # ! First tab :Patient Identification
        self.tab_widget.addTab(self.patient_identification.gui, "Patient identification")

        # ! Second tab : Pain type
        self.tab_widget.addTab(self.pain_type.gui, "Pain type")

        # ! Third tab : Pain localization
        self.tab_widget.addTab(self.pain_localization.gui, "Pain localization")

        # ! Palpation
        self.tab_widget.addTab(self.palpation.gui, "Palpation")

        # ! Pain intensity
        self.tab_widget.addTab(self.pain_intensity.gui, "Pain intensity")

        # ! Pain intensity
        self.tab_widget.addTab(self.other_pain.gui, "Other pain")

        # ! --- simple label
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 20)
        label = QLabel("Other tab")
        header_layout.addWidget(label)

        self.show()

    def closeEvent(self, a0):
        print(self.patient_data)
        print("Closing app")
        self.pain_localization.logic.stop()
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
