import multiprocessing as mp
import sys
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable, Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QRadioButton, QWidget


class PainType:
    """
    This class will contain the GUI and logic part for the Pain Type Selector
    """

    def __init__(self):
        logger.info("Initializing PainType")
        self.gui: PainTypeGUI = PainTypeGUI()
        self.logic: PainTypeLogic = PainTypeLogic(self, worker_frequency=30)

        self.gui.init_ui()
        self.gui.show()


class PainTypeGUI(QWidget):
    """
    This class will contain the GUI part for the Pain Type Selector
    """

    def __init__(self):
        super().__init__()

    # ---------- UI ----------
    def init_ui(self):
        self.setWindowTitle("Pain Type Selector")
        self.setFixedSize(400, 250)  # Similar size to the base GUI

        self.__init_header()
        self.__init_content()
        self.__init_footer()

    def __init_header(self) -> None:
        self.label = QLabel("Pain Type Selector", self)
        self.label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.label.setGeometry(10, 10, 380, 30)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.label.setOpenExternalLinks(True)
        self.label.setTextFormat(Qt.TextFormat.MarkdownText)

    def __init_content(self) -> None:
        self.radio_continuous = QRadioButton("Continuous Pain", self)
        self.radio_continuous.setGeometry(20, 60, 200, 30)
        self.radio_continuous.setChecked(True)

        self.radio_palpation = QRadioButton("Pain on Palpation", self)
        self.radio_palpation.setGeometry(20, 100, 200, 30)

        style = """
        QRadioButton {
            color: black;
            border: none;
            background: none;
            text-decoration: none;
        }
        QRadioButton:hover {
            color: black;
            background: none;
        }
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
        }
        """

        self.radio_continuous.setStyleSheet(style)
        self.radio_palpation.setStyleSheet(style)

    def __init_footer(self) -> None:
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(20, 150, 100, 30)
        self.ok_button.setStyleSheet("background-color: green; color: white;")
        self.ok_button.clicked.connect(self.on_ok_clicked)

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
