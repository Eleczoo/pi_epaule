import multiprocessing as mp
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable, Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget


class PatientIdentification:
    """
    This class will contain the GUI and logic part for the PatientIdentification
    """

    def __init__(self):
        logger.info("Initializing PatientIdentification")
        self.gui: PatientIdentificationGUI = PatientIdentificationGUI()
        self.logic: PatientIdentificationLogic = PatientIdentificationLogic(self, worker_frequency=30)

        self.gui.init_ui()


class PatientIdentificationGUI(QWidget):
    """
    This class will contain the GUI part for the PatientIdentification
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    # ! ---------- UI ----------
    def init_ui(self):
        self.__init_header()
        self.__init_content()
        self.__init_footer()

    def __init_header(self) -> None:
        self.label = QLabel("Patient Identification", self)
        self.label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.label.setGeometry(10, 10, 300, 30)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.label.setOpenExternalLinks(True)
        self.label.setTextFormat(Qt.TextFormat.MarkdownText)

    def __init_content(self) -> None:
        self.name_label = QLabel("Nom:", self)
        self.name_label.setGeometry(10, 50, 100, 30)
        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(120, 50, 200, 30)
        self.name_input.setStyleSheet("border: 1px solid black;")

        self.firstname_label = QLabel("Prénom:", self)
        self.firstname_label.setGeometry(10, 90, 100, 30)
        self.firstname_input = QLineEdit(self)
        self.firstname_input.setGeometry(120, 90, 200, 30)
        self.firstname_input.setStyleSheet("border: 1px solid black;")

        self.date_naissance_label = QLabel("Date de naissance:", self)
        self.date_naissance_label.setGeometry(10, 130, 150, 30)
        self.date_naissance_input = QLineEdit(self)
        self.date_naissance_input.setGeometry(170, 130, 150, 30)
        self.date_naissance_input.setStyleSheet("border: 1px solid black;")

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(10, 170, 100, 30)
        self.ok_button.setStyleSheet("background-color: green; color: white;")
        self.ok_button.clicked.connect(self.on_ok_clicked)

    def on_ok_clicked(self) -> None:
        print("OK button clicked")

    def __init_footer(self) -> None:
        pass


class PatientIdentificationLogic(QRunnable):
    """
    Good Source : https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    """

    def __init__(self, parent: PatientIdentification, worker_frequency: int) -> None:
        super().__init__()
        self.parent: PatientIdentification = parent

        self.worker_frequency: int = worker_frequency
        self.worker_period: float = 1 / self.worker_frequency

        self.stopped: EventClass = mp.Event()

    def run(self) -> None:
        while not self.stopped.wait(timeout=self.worker_period):
            logger.debug(f"Running logic at {self.worker_frequency} Hz")

    def stop(self) -> None:
        self.stopped.set()
