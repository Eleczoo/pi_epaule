import multiprocessing as mp
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable, Qt
from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from toaster import Toaster


class PatientIdentification:
    """
    This class will contain the GUI and logic part for the PatientIdentification
    """

    def __init__(self, patient_data: dict, tab_widget: QWidget, toaster: Toaster):
        logger.info("Initializing PatientIdentification")
        # ! Get patient dictionary from main app
        self.patient_data: dict[str] = patient_data
        self.tab_widget: QWidget = tab_widget
        self.toaster: Toaster = toaster

        # ! Initialize the GUI and logic
        self.gui: PatientIdentificationGUI = PatientIdentificationGUI(self)
        self.logic: PatientIdentificationLogic = PatientIdentificationLogic(self, worker_frequency=30)


class PatientIdentificationGUI(QWidget):
    """
    This class will contain the GUI part for the PatientIdentification
    """

    def __init__(self, parent: PatientIdentification):
        super().__init__()
        self.parent: PatientIdentification = parent
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(100, 30, 100, 30)
        self.setLayout(self.main_layout)

        self.init_ui()

    # ! ---------- UI ----------
    def init_ui(self):
        self.__init_header()
        self.__init_content()
        self.__init_footer()

    def __init_header(self) -> None:
        self.header_label = QLabel("Identification du patient", self)
        self.header_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.header_label)

    def __init_content(self) -> None:
        center_layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        center_layout.addStretch(1)

        self.name_input = QLineEdit(self)
        self.name_input.setMinimumHeight(40)
        self.name_input.setStyleSheet("border: 1px solid black; font-size: 16pt;")
        form_layout.addRow("Prénom", self.name_input)

        self.firstname_input = QLineEdit(self)
        self.firstname_input.setMinimumHeight(40)
        self.firstname_input.setStyleSheet("border: 1px solid black; font-size: 16pt;")
        form_layout.addRow("Nom de famille", self.firstname_input)

        self.birthday_input = QLineEdit(self)
        self.birthday_input.setMinimumHeight(40)
        self.birthday_input.setStyleSheet("border: 1px solid black; font-size: 16pt;")
        self.birthday_input.setPlaceholderText("DD/MM/YYYY")
        self.birthday_input.setMaxLength(10)
        self.birthday_input.setInputMask("99/99/9999")
        self.birthday_input.setText("01/01/1900")
        form_layout.addRow("Date de naissance", self.birthday_input)

        center_layout.addLayout(form_layout, stretch=1)

        self.main_layout.addLayout(center_layout)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setStyleSheet("background-color: green; color: white;")
        self.ok_button.clicked.connect(self.on_ok_clicked)

        self.main_layout.addWidget(self.ok_button)

        self.setLayout(self.main_layout)

    def on_ok_clicked(self) -> None:
        self.parent.patient_data["firstname"] = self.name_input.text()
        self.parent.patient_data["lastname"] = self.firstname_input.text()
        self.parent.patient_data["data_of_birth"] = self.birthday_input.text()

        # Check if fields are filled
        if not self.parent.patient_data["firstname"]:
            self.parent.toaster.show_warning("Le prénom est manquant.")
            return

        if not self.parent.patient_data["lastname"]:
            self.parent.toaster.show_warning("Le nom de famille est manquant.")
            return

        # Check if birthday is filled and in the correct format
        # And not the default value
        if (
            not self.parent.patient_data["data_of_birth"]
            or len(self.parent.patient_data["data_of_birth"]) != 10
            or self.parent.patient_data["data_of_birth"] == "01/01/1900"
        ):
            self.parent.toaster.show_warning("La date de naissance n'est pas remplie correctement.")
            return

        #  Check if birthday does not make us older than 120 years or younger than 3 years
        from datetime import datetime, timedelta

        today = datetime.now()
        try:
            birthday = datetime.strptime(self.parent.patient_data["data_of_birth"], "%d/%m/%Y")
            age = today - birthday
            if age < timedelta(days=3 * 365) or age > timedelta(days=120 * 365):
                self.parent.toaster.show_warning(
                    "La date de naissance n'est pas valide, elle doit être comprise entre 3 et 120 ans."
                )
                return
        except ValueError:
            self.parent.toaster.show_warning(
                "La date de naissance n'est pas remplie correctement, elle doit être au format JJ/MM/AAAA."
            )
            return

        self.parent.tab_widget.setCurrentIndex(1)  # Switch to the next tab (Pain Type)

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
        print(self.parent.patient_data)
        self.stopped.set()
