from loguru import logger
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class PainIntensity:
    """
    This class will contain the GUI and logic part for the PainIntensity
    """

    def __init__(self):
        logger.info("Initializing PainIntensity")
        self.gui: PainIntensityGUI = PainIntensityGUI()
        self.logic: PainIntensityLogic = PainIntensityLogic(self)


class PainIntensityGUI(QWidget):
    """
    This class contains the GUI part for the PainIntensity
    """

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(self.main_layout)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #f8f9fa;")
        self.__init_header()
        self.__init_content()
        self.__init_footer()

    def __init_header(self):
        self.header_label = QLabel("Pain Intensity", self)
        self.header_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.header_label)

        self.sub_label = QLabel("Douleur n°1", self)
        self.sub_label.setStyleSheet("font-size: 14pt; font-weight: normal;")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.sub_label)

    def __init_content(self):
        # Central content layout
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        # --- First slider group ---
        slider1_layout = QVBoxLayout()
        slider1_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.slider_label = QLabel("Select Intensity :", self)
        self.slider_label.setStyleSheet("font-size: 12pt;")
        self.slider_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        slider1_layout.addWidget(self.slider_label)

        slider1_row = QHBoxLayout()
        slider1_row.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.intensity_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.intensity_slider.setMinimum(0)
        self.intensity_slider.setMaximum(10)
        self.intensity_slider.setTickInterval(1)
        self.intensity_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.intensity_slider.setStyleSheet("")  # Remove background
        self.intensity_slider.setFixedWidth(500)  # Bigger slider

        self.value_label = QLabel("0", self)
        self.value_label.setStyleSheet("font-size: 10pt; min-width: 18px;")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        slider1_row.addStretch(1)
        slider1_row.addWidget(self.intensity_slider, stretch=10)
        slider1_row.addWidget(self.value_label)
        slider1_row.addStretch(1)

        self.intensity_slider.valueChanged.connect(self.update_value_label)
        slider1_layout.addLayout(slider1_row)

        content_layout.addLayout(slider1_layout)

        # --- Second slider group ---
        slider2_layout = QVBoxLayout()
        slider2_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.slider_label2 = QLabel("Select Intensity 2 :", self)
        self.slider_label2.setStyleSheet("font-size: 12pt;")
        self.slider_label2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        slider2_layout.addWidget(self.slider_label2)

        slider2_row = QHBoxLayout()
        slider2_row.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.intensity_slider2 = QSlider(Qt.Orientation.Horizontal, self)
        self.intensity_slider2.setMinimum(0)
        self.intensity_slider2.setMaximum(10)
        self.intensity_slider2.setTickInterval(1)
        self.intensity_slider2.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self.intensity_slider2.setStyleSheet("")  # Remove background
        self.intensity_slider2.setFixedWidth(500)  # Bigger slider

        self.value_label2 = QLabel("0", self)
        self.value_label2.setStyleSheet("font-size: 10pt; min-width: 18px;")
        self.value_label2.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)

        slider2_row.addStretch(1)
        slider2_row.addWidget(self.intensity_slider2, stretch=10)
        slider2_row.addWidget(self.value_label2)
        slider2_row.addStretch(1)

        self.intensity_slider2.valueChanged.connect(self.update_value_label2)
        slider2_layout.addLayout(slider2_row)

        content_layout.addLayout(slider2_layout)

        # OK button centered in content
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Ok", self)
        self.ok_button.setStyleSheet("background-color: green; color: white;")
        self.ok_button.clicked.connect(self.on_ok_clicked)
        button_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(content_layout, stretch=1)
        self.main_layout.addLayout(button_layout)

    def update_value_label(self, value):
        self.value_label.setText(str(value))

    def update_value_label2(self, value):
        self.value_label2.setText(str(value))

    def on_ok_clicked(self):
        print(f"Pain intensity 1 confirmed: {self.intensity_slider.value()}")
        print(f"Pain intensity 2 confirmed: {self.intensity_slider2.value()}")

    def __init_footer(self):
        pass


class PainIntensityLogic:
    """
    Logic class for PainIntensity
    """

    def __init__(self, parent: PainIntensity):
        self.parent = parent

    def process_intensity(self, value: int):
        logger.debug(f"Processing pain intensity value: {value}")
