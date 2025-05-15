import multiprocessing as mp
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable, Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class PainLocalization:
    """
    This class will contain the GUI and logic part for the PainLocalization
    """

    def __init__(self):
        logger.info("Initializing PainLocalization")
        self.gui: PainLocalizationGUI = PainLocalizationGUI()
        self.logic: PainLocalizationLogic = PainLocalizationLogic(self, worker_frequency=30)


class PainLocalizationGUI(QWidget):
    """
    This class contains the GUI part for the PainLocalization
    """

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        self.init_ui()

    def init_ui(self):
        self.__init_header()
        self.__init_content()
        self.__init_footer()
        self.setLayout(self.main_layout)

    def __init_header(self):
        header_label = QLabel("Pain Localization", self)
        header_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.sub_label = QLabel("Douleur n°1", self)
        self.sub_label.setStyleSheet("font-size: 14pt; font-weight: normal;")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.main_layout.addWidget(header_label)
        self.main_layout.addWidget(self.sub_label)

    def __init_content(self):
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Flux cam placeholder
        self.flux_cam_label = QLabel("Video feed", self)
        self.flux_cam_label.setStyleSheet("background-color: #888; border-radius: 5px; color: white; font-weight: normal;")
        self.flux_cam_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 3D avatar placeholder
        self.avatar_placeholder = QFrame(self)
        self.avatar_placeholder.setStyleSheet("background-color: #888; border-radius: 5px;")

        content_layout.addWidget(self.flux_cam_label)
        content_layout.addWidget(self.avatar_placeholder)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.timer_button = QPushButton("Lancer un timer", self)
        self.timer_button.setStyleSheet("background-color: green; color: white;")
        self.timer_button.clicked.connect(lambda: print("Timer launched."))

        self.ok_button = QPushButton("Ok", self)
        self.ok_button.setStyleSheet("background-color: green; color: white;")
        self.ok_button.clicked.connect(self.on_ok_clicked)

        buttons_layout.addWidget(self.timer_button)
        buttons_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(content_layout, stretch=1)
        self.main_layout.addLayout(buttons_layout)

    def on_ok_clicked(self):
        print("Pain localization confirmed.")

    def __init_footer(self):
        pass


class PainLocalizationLogic(QRunnable):
    """
    Logic class for PainLocalization
    """

    def __init__(self, parent: PainLocalization, worker_frequency: int):
        super().__init__()
        self.parent = parent
        self.worker_frequency = worker_frequency
        self.worker_period = 1 / worker_frequency
        self.stopped: EventClass = mp.Event()

    def run(self):
        while not self.stopped.wait(timeout=self.worker_period):
            logger.debug("Running PainLocalization logic.")

    def stop(self):
        self.stopped.set()
