import multiprocessing as mp
import sys
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable, Qt
from PyQt6.QtWidgets import QApplication, QButtonGroup, QHBoxLayout, QLabel, QPushButton, QRadioButton, QVBoxLayout, QWidget

from toaster import Toaster


class PainType:
    """
    This class will contain the GUI and logic part for the Pain Type Selector
    """

    def __init__(self, patient_data: dict, tab_widget: QWidget, toaster: Toaster):
        logger.info("Initializing PainType")
        # ! Get patient dictionary from main app
        self.patient_data: dict[str] = patient_data
        self.tab_widget: QWidget = tab_widget
        self.toaster: Toaster = toaster

        # ! Initialize the GUI and logic
        self.gui: PainTypeGUI = PainTypeGUI(self)
        self.logic: PainTypeLogic = PainTypeLogic(self, worker_frequency=30)


class PainTypeGUI(QWidget):
    """
    This class will contain the GUI part for the Pain Type Selector
    """

    def __init__(self, parent):
        super().__init__()
        self.pain_type: PainType = parent
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
        self.header_label = QLabel("Type de douleur", self)
        self.header_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.sub_label = QLabel("Douleur n°1", self)
        self.sub_label.setStyleSheet("font-size: 14pt; font-weight: normal;")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.main_layout.addWidget(self.header_label)
        self.main_layout.addWidget(self.sub_label)

    def __init_content(self) -> None:
        # Centered radio buttons in a vertical layout
        radio_layout = QVBoxLayout()
        radio_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        self.radio_group = QButtonGroup(self)
        self.radio_continuous = QRadioButton("La douleur est constamment présente", self)
        self.radio_continuous.setChecked(True)
        self.radio_palpation = QRadioButton("La douleur n'est présente qu'à la palpation", self)

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
        # Get the current pain index from the pain_count
        pain_index = self.pain_type.patient_data.get("pain_count", 0)
        print(f"Current pain index: {pain_index}")

        # Store the pain type for the current pain index
        if self.radio_continuous.isChecked():
            self.pain_type.patient_data[f"pain_type_{pain_index}"] = "Douleur Continue"
        else:
            self.pain_type.patient_data[f"pain_type_{pain_index}"] = "Douleur à la Palpation"

        # Change the sub-label to indicate the next pain number (for the next pain type, if there is one)
        self.sub_label.setText(f"Douleur n°{pain_index + 2}")

        # Switch to the next tab (Pain Localization)
        self.pain_type.tab_widget.setCurrentIndex(2)


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
