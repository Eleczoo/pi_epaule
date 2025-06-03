import multiprocessing as mp
from multiprocessing.synchronize import Event as EventClass

import cv2 as cv
from loguru import logger
from PyQt6.QtCore import QRunnable, Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget

from report_creator import ReportCreator
from toaster import Toaster


class OtherPain:
    def __init__(self, patient_data: dict, tab_widget: QWidget, toaster: Toaster):
        logger.info("Initializing OtherPain")
        # ! Get patient dictionary from main app
        self.patient_data: dict[str] = patient_data
        self.tab_widget: QWidget = tab_widget
        self.toaster: Toaster = toaster

        # ! Initialize the GUI and logic
        self.gui: OtherPainGUI = OtherPainGUI(self)
        self.logic: OtherPainLogic = OtherPainLogic(self, worker_frequency=30)


class OtherPainGUI(QWidget):
    """
    This class will contain the GUI part for the OtherPain page
    """

    def __init__(self, parent):
        super().__init__()
        self.other_pain: OtherPain = parent
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setLayout(self.main_layout)
        self.init_ui()

    # ! ---------- UI ----------
    def init_ui(self):
        self.__init_header()
        self.__init_content()
        self.__init_footer()

    def __init_header(self) -> None:
        self.header_label = QLabel("Autres douleurs", self)
        self.header_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.main_layout.addWidget(self.header_label)

    def __init_content(self) -> None:
        # Central content layout
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

        self.central_text = QLabel("Avez-vous une autre douleur à nous indiquer ?", self)
        self.central_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_text.setStyleSheet(
            "font-size: 20pt; font-weight: bold; color: #333; border: 1px solid #ccc; background: #f9f9f9;"
        )
        self.central_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        content_layout.addWidget(self.central_text, stretch=1)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.no_button = QPushButton("Finir le test", self)
        self.no_button.setStyleSheet("background-color: orange; color: white; font-size: 14pt;")
        self.no_button.clicked.connect(self.on_no_clicked)

        self.yes_button = QPushButton("Ajouter une douleur", self)
        self.yes_button.setStyleSheet("background-color: green; color: white; font-size: 14pt;")
        self.yes_button.clicked.connect(self.on_yes_clicked)

        buttons_layout.addWidget(self.yes_button)
        buttons_layout.addWidget(self.no_button)
        self.main_layout.addLayout(content_layout, stretch=1)
        self.main_layout.addLayout(buttons_layout)

    def on_no_clicked(self) -> None:
        logger.info("No button clicked, generating report...")

        template_dir = "report_template"
        report_temp_dir = "report_temp_dir"

        report_creator = ReportCreator(
            template_dir=template_dir,
            report_temp_dir=report_temp_dir,
            report_output_pdf=f"{self.other_pain.patient_data['firstname']}_{self.other_pain.patient_data['lastname']}_report.pdf",
        )

        report_creator.add_title("Rapport de douleur")

        report_creator.add_subtitle("Identification du patient")

        report_creator.add_list(
            [
                f"Prenom: {self.other_pain.patient_data['firstname']}\r",
                f"Nom de famille: {self.other_pain.patient_data['lastname']}\r",
                f"Date de naissance: {self.other_pain.patient_data['data_of_birth']}\r",
            ]
        )

        pain_count = self.other_pain.patient_data.get("pain_count", 0)
        logger.debug(f"Number of pains to report: {pain_count}")
        for i in range(pain_count + 1):
            report_creator.add_pagebreak()
            report_creator.add_subtitle(f"Douleur n°{i + 1}")
            report_creator.add_paragraph(
                f"Type de douleur: {self.other_pain.patient_data.get(f'pain_type_{i}', 'Non spécifié')}\r",
            )

            if self.other_pain.patient_data.get(f"pain_type_{i}") == "Douleur Continue":
                report_creator.add_paragraph(
                    f"Intensité de la douleur: {self.other_pain.patient_data.get(f'pain_intensity1_{i}', 'Non spécifié')}\r"
                )
            else:
                report_creator.add_list(
                    [
                        f"Intensité de la douleur continue : {self.other_pain.patient_data.get(f'pain_intensity1_{i}', 'Non spécifié')}\r",
                        f"Intensité de la douleur à la palpation : {self.other_pain.patient_data.get(f'pain_intensity2_{i}', 'Non spécifié')}\r",
                    ]
                )

            ff = f"saved_img_{i}"
            pain_localization_image: cv.Mat = self.other_pain.patient_data.get(ff, None)
            logger.debug(f"{ff = }")
            logger.debug(f"{self.other_pain.patient_data[ff].sum()=}")
            # logger.debug(f"img sum {self.other_pain.patient_data[f'saved_img_{0}'].sum()}")
            # logger.debug(f"img sum {self.other_pain.patient_data[f'saved_img_{1}'].sum()}")

            path = report_creator.save_image(
                filename=f"image_{i + 1}.png",
                image_data=pain_localization_image,
            )

            logger.debug(f"Image saved at {path}")

            report_creator.add_image(
                image_path=path,
                caption=f"Localisation Douleur N°{i + 1}",
            )

        logger.info("Starting to compile the report...")
        report_creator.compile_report()
        logger.info("Report compiled successfully.")

    def on_yes_clicked(self) -> None:
        # Get the current pain index from the pain_count
        pain_index = self.other_pain.patient_data.get("pain_count", 0)
        # Increment the pain_count for the next pain
        self.other_pain.patient_data["pain_count"] = pain_index + 1

        # Come back to pain type tab
        self.other_pain.tab_widget.setCurrentIndex(1)

    def __init_footer(self) -> None:
        pass


class OtherPainLogic(QRunnable):
    """
    Worker logic for OtherPain page
    """

    def __init__(self, parent: OtherPain, worker_frequency: int) -> None:
        super().__init__()
        self.parent: OtherPain = parent

        self.worker_frequency: int = worker_frequency
        self.worker_period: float = 1 / self.worker_frequency

        self.stopped: EventClass = mp.Event()

    def run(self) -> None:
        while not self.stopped.wait(timeout=self.worker_period):
            logger.debug(f"Running OtherPain logic at {self.worker_frequency} Hz")

    def stop(self) -> None:
        self.stopped.set()
