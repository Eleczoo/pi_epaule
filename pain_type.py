import multiprocessing as mp
import sys
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable, Qt
from PyQt6.QtWidgets import QApplication, QButtonGroup, QHBoxLayout, QLabel, QPushButton, QRadioButton, QVBoxLayout, QWidget


class PainType:
    """
    This class will contain the GUI and logic part for the Pain Type Selector
    """

    def __init__(self):
        logger.info("Initializing PainType")
        self.gui: PainTypeGUI = PainTypeGUI()
        self.logic: PainTypeLogic = PainTypeLogic(self, worker_frequency=30)


class PainTypeGUI(QWidget):
    """
    This class will contain the GUI part for the Pain Type Selector
    """

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.init_ui()

    # ---------- UI ----------
    def init_ui(self):
        self.__init_header()
        self.__init_content()
        self.__init_footer()
        self.setLayout(self.main_layout)

    def __init_header(self) -> None:
        self.header_label = QLabel("Pain Type", self)
        self.header_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.header_label)

    def __init_content(self) -> None:
        # Centered radio buttons in a vertical layout
        radio_layout = QVBoxLayout()
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        self.radio_group = QButtonGroup(self)
        self.radio_continuous = QRadioButton("Continuous Pain", self)
        self.radio_continuous.setChecked(True)
        self.radio_palpation = QRadioButton("Pain on Palpation", self)

        style = """
        QRadioButton {
            color: black;
            border: none;
            background: none;
            text-decoration: none;
            min-width: 220px;
            min-height: 32px;
            font-size: 13pt;
            padding: 8px 24px;
            border-radius: 8px;
        }
        QRadioButton:hover {
            color: black;
            background: #e6f2e6;
        }
        QRadioButton::indicator {
            width: 20px;
            height: 20px;
        }
        """

        self.radio_continuous.setStyleSheet(style)
        self.radio_palpation.setStyleSheet(style)

        self.radio_group.addButton(self.radio_continuous)
        self.radio_group.addButton(self.radio_palpation)

        # Add stretch before and after to center vertically
        radio_layout.addStretch(1)
        radio_center_layout = QHBoxLayout()
        radio_center_layout.addStretch(1)
        radio_center_layout.addWidget(self.radio_continuous)
        radio_center_layout.addStretch(1)
        radio_layout.addLayout(radio_center_layout)

        radio_center_layout2 = QHBoxLayout()
        radio_center_layout2.addStretch(1)
        radio_center_layout2.addWidget(self.radio_palpation)
        radio_center_layout2.addStretch(1)
        radio_layout.addLayout(radio_center_layout2)
        radio_layout.addStretch(1)

        self.main_layout.addLayout(radio_layout, stretch=1)

        # Add OK button
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setStyleSheet("background-color: green; color: white;")
        self.ok_button.clicked.connect(self.on_ok_clicked)

        self.main_layout.addWidget(self.ok_button)

    def __init_footer(self) -> None:
        pass

    def on_ok_clicked(self):
        if self.radio_continuous.isChecked():
            self.choice = "Continuous Pain"
        else:
            self.choice = "Pain on Palpation"
        print(f"User selected: {self.choice}")


class PainTypeLogic(QRunnable):
    """
    Logic thread running at a given frequency
    """

    def __init__(self, parent: PainType, worker_frequency: int) -> None:
        super().__init__()
        self.parent: PainType = parent
        self.worker_frequency: int = worker_frequency
        self.worker_period: float = 1 / self.worker_frequency
        self.stopped: EventClass = mp.Event()

    def run(self) -> None:
        while not self.stopped.wait(timeout=self.worker_period):
            logger.debug(f"Running logic at {self.worker_frequency} Hz")

    def stop(self) -> None:
        self.stopped.set()


if __name__ == "__main__":
    mp.set_start_method("spawn")
    app = QApplication(sys.argv)
    pain_type = PainType()
    sys.exit(app.exec())
