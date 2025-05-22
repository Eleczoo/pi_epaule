import multiprocessing as mp
from multiprocessing.synchronize import Event as EventClass

import cv2
from loguru import logger
from PyQt6.QtCore import QObject, QRunnable, Qt, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget


class PainLocalization:
    """
    This class will contain the GUI and logic part for the PainLocalization
    """

    def __init__(self):
        logger.info("Initializing PainLocalization")
        self.logic: PainLocalizationLogic = PainLocalizationLogic(
            self,
            worker_frequency=30,
            video_source="video.mp4",
        )
        self.gui: PainLocalizationGUI = PainLocalizationGUI(parent=self)


class PainLocalizationGUI(QWidget):
    """
    This class contains the GUI part for the PainLocalization
    """

    def __init__(self, parent: PainLocalization):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)
        self.pain_localization: PainLocalization = parent

        self.init_ui()

    def init_ui(self):
        self.__init_header()
        self.__init_content()
        self.__init_footer()
        self.setLayout(self.main_layout)

    def resizeEvent(self, a0):
        """
        Resize event to update the size of the capture
        :param a0: QResizeEvent
        """
        super().resizeEvent(a0)
        size = (self.flux_cam_label.width(), self.flux_cam_label.height())
        self.pain_localization.logic.set_size_capture(size)

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
        self.flux_cam_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.pain_localization.logic.signals.change_pixmap_signal.connect(self.update_image)

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

    def update_image(self, image: QImage):
        """
        Updates the image in the label
        :param image: QImage to be displayed
        """
        self.flux_cam_label.setPixmap(QPixmap.fromImage(image))

    def on_ok_clicked(self):
        print("Pain localization confirmed.")

    def __init_footer(self):
        pass


class PainLocalizationSignals(QObject):
    """
    Signals to communicate with the worker thread
    """

    change_pixmap_signal = pyqtSignal(QImage)


class PainLocalizationLogic(QRunnable):
    """
    Logic class for PainLocalization
    """

    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self, parent: PainLocalization, worker_frequency: int, video_source: str):
        super().__init__()
        self.parent = parent
        self.signals = PainLocalizationSignals()
        self.worker_frequency = worker_frequency
        self.worker_period = 1 / worker_frequency
        self.video_source = video_source
        self.stopped: EventClass = mp.Event()

        self.size_capture: tuple[int, int] = (640, 480)

    def set_size_capture(self, size: tuple[int, int]):
        """
        Set the size of the capture
        :param size: tuple of (width, height)
        """
        self.size_capture = size

    def run(self):
        self.cap = cv2.VideoCapture(self.video_source)
        while not self.stopped.wait(timeout=self.worker_period):
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            scaled_img = qt_image.scaled(self.size_capture[0], self.size_capture[1], Qt.AspectRatioMode.KeepAspectRatio)
            # scaled_img = qt_image.scaled(self.size_capture[0], self.size_capture[1])
            self.signals.change_pixmap_signal.emit(scaled_img)

    def stop(self):
        self.stopped.set()
        self.cap.release()

    #         cam.release()
    # out.release()
    # cv2.destroyAllWindows()
