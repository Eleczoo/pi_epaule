import multiprocessing as mp
import sys
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QRadioButton, QVBoxLayout, QWidget


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

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.__init_header(layout)
        self.__init_content(layout)
        self.__init_footer(layout)

    def __init_header(self, layout: QVBoxLayout) -> None:
        title_label = QLabel("Select the type of pain")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(title_label)

    def __init_content(self, layout: QVBoxLayout) -> None:
        self.radio_continuous = QRadioButton("Continuous Pain")
        self.radio_palpation = QRadioButton("Pain on Palpation")
        self.radio_continuous.setChecked(True)

        # Remove underline on hover
        style = """
		QRadioButton {
			text-decoration: none;
			color: black;
		}
		QRadioButton:hover {
			text-decoration: none;
			color: black;
			background: transparent;
		}
		QRadioButton::indicator {
			width: 16px;
			height: 16px;
		}
		"""
        self.radio_continuous.setStyleSheet(style)
        self.radio_palpation.setStyleSheet(style)

        layout.addWidget(self.radio_continuous)
        layout.addWidget(self.radio_palpation)

    def __init_footer(self, layout: QVBoxLayout) -> None:
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.on_ok_clicked)
        layout.addWidget(ok_button)

    def on_ok_clicked(self):
        if self.radio_continuous.isChecked():
            self.choice = "Continuous Pain"
        else:
            self.choice = "Pain on Palpation"


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
    mp.set_start_method("spawn")  # Important for multiprocessing on some platforms
    app = QApplication(sys.argv)
    pain_type = PainType()
    sys.exit(app.exec())
