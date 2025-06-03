import multiprocessing as mp
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable, Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from toaster import Toaster


class Palpation:
    """
    This class will contain the GUI and logic part for the Palpation page
    """

    def __init__(self, patient_data: dict, tab_widget: QWidget, toaster: Toaster):
        logger.info("Initializing Palpation")
        # ! Get patient dictionary from main app
        self.patient_data: dict[str] = patient_data
        self.tab_widget: QWidget = tab_widget

        self.toaster: Toaster = toaster

        # ! Initialize the GUI and logic
        self.gui: PalpationGUI = PalpationGUI(self)
        self.logic: PalpationLogic = PalpationLogic(self, worker_frequency=30)


class PalpationGUI(QWidget):
    """
    This class will contain the GUI part for the Palpation page
    """

    def __init__(self, parent):
        super().__init__()
        self.parent: Palpation = parent
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        self.init_ui()

    # ! ---------- UI ----------
    def init_ui(self):
        self.__init_header()
        self.__init_content()
        self.__init_footer()
        self.setLayout(self.main_layout)

    def __init_header(self) -> None:
        self.header_label = QLabel("Palpation", self)
        self.header_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.sub_label = QLabel("Douleur n°1", self)
        self.sub_label.setStyleSheet("font-size: 14pt; font-weight: normal;")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.main_layout.addWidget(self.header_label)
        self.main_layout.addWidget(self.sub_label)

    def __init_content(self) -> None:
        # Central content layout
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        self.central_text = QLabel("Effectuez la palpation du patient", self)
        self.central_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_text.setStyleSheet(
            "font-size: 20pt; font-weight: bold; color: #333; border: 1px solid #ccc; background: #f9f9f9;"
        )
        self.central_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout.addWidget(self.central_text, stretch=1)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.skip_button = QPushButton("Skip", self)
        self.skip_button.setStyleSheet("background-color: orange; color: white; font-size: 14pt;")
        self.skip_button.clicked.connect(self.on_skip_clicked)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setStyleSheet("background-color: green; color: white; font-size: 14pt;")
        self.ok_button.clicked.connect(self.on_ok_clicked)

        buttons_layout.addWidget(self.skip_button)
        buttons_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(content_layout, stretch=1)
        self.main_layout.addLayout(buttons_layout)

    def on_skip_clicked(self) -> None:
        print("Skip button clicked")

    def on_ok_clicked(self) -> None:
        self.parent.tab_widget.setCurrentIndex(4)  # Switch to the next tab (Pain Intensity)

    def __init_footer(self) -> None:
        pass


class PalpationLogic(QRunnable):
    """
    Worker logic for Palpation page
    """

    def __init__(self, parent: Palpation, worker_frequency: int) -> None:
        super().__init__()
        self.parent: Palpation = parent

        self.worker_frequency: int = worker_frequency
        self.worker_period: float = 1 / self.worker_frequency

        self.stopped: EventClass = mp.Event()

    def run(self) -> None:
        while not self.stopped.wait(timeout=self.worker_period):
            logger.debug(f"Running Palpation logic at {self.worker_frequency} Hz")

    def stop(self) -> None:
        self.stopped.set()
