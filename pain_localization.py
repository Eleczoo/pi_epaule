import multiprocessing as mp
import sys
import threading
from multiprocessing.synchronize import Event as EventClass

import cv2
import numpy as np
from loguru import logger
from PyQt6.QtCore import QObject, QRunnable, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QWidget
from ultralytics import YOLO

from toaster import Toaster

# Set the logger as enqueue
logger.remove()
logger.add(
    sys.stderr,
    level="DEBUG",
    colorize=True,
    enqueue=True,
    backtrace=True,
)


class PainLocalization:
    """
    This class will contain the GUI and logic part for the PainLocalization
    """

    def __init__(self, patient_data: dict, tab_widget: QWidget, toaster: Toaster):
        logger.info("Initializing PainLocalization")

        # ! Get patient dictionary from main app
        self.patient_data: dict[str] = patient_data
        self.tab_widget: QWidget = tab_widget
        self.toaster: Toaster = toaster

        # ! Initialize the GUI and logic
        self.logic: PainLocalizationLogic = PainLocalizationLogic(
            self,
            worker_frequency=30,
            video_source="assets/dispositif_quentin_down.mp4",
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
        self.captured_frame: QImage = None

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
        if self.captured_frame is not None:
            # Rescale the captured image to the new size
            scaled_img = self.captured_frame.scaled(
                size[0],
                size[1],
                Qt.AspectRatioMode.KeepAspectRatio,
            )
            self.captured_image.setPixmap(QPixmap.fromImage(scaled_img))

    def __init_header(self):
        header_label = QLabel("Localisation de la douleur", self)
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
        # self.flux_cam_label.setStyleSheet("background-color: #FFFFFF; border-radius: 5px; color: white; font-weight: normal;")
        self.flux_cam_label.setStyleSheet("border-radius: 5px; color: white; font-weight: normal;")
        self.flux_cam_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.flux_cam_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        self.pain_localization.logic.signals.change_pixmap_signal.connect(self.update_image)

        # Captured image placeholder
        # self.captured_image = QFrame(self)
        # self.captured_image.setStyleSheet("background-color: #888; border-radius: 5px;")
        self.captured_image = QLabel("Captured Image", self)
        self.captured_image.setStyleSheet("border-radius: 5px; color: white; font-weight: normal;")
        self.captured_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.captured_image.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        content_layout.addWidget(self.flux_cam_label)
        content_layout.addWidget(self.captured_image)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        self.timer_button = QPushButton("Lancer un timer", self)
        self.timer_button.setStyleSheet("background-color: green; color: white;")
        self.timer_button.clicked.connect(self.timer_clicked)

        self.ok_button = QPushButton("Ok", self)
        self.ok_button.setStyleSheet("background-color: gray; color: white;")
        self.ok_button.setEnabled(False)  # Initially disabled
        self.ok_button.clicked.connect(self.on_ok_clicked)

        buttons_layout.addWidget(self.timer_button)
        buttons_layout.addWidget(self.ok_button)

        self.main_layout.addLayout(content_layout, stretch=1)
        self.main_layout.addLayout(buttons_layout)

        # Timer Setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_timeout)

        self.timer_update_label = QTimer(self)
        self.timer_update_label.timeout.connect(self.set_current_timer_label)

    def update_image(self, image: QImage):
        """
        Updates the image in the label
        :param image: QImage to be displayed
        """
        self.flux_cam_label.setPixmap(QPixmap.fromImage(image))

    def on_ok_clicked(self):
        # Get the current pain index from the pain_count
        pain_index = self.pain_localization.patient_data.get("pain_count", 0)

        # TODO : Save the localization, elements and captured image in the patient_data dictionary
        self.pain_localization.patient_data[f"saved_img_{pain_index}"] = self.saved_image.copy()  # Save the captured image

        # ! Clear captured image
        self.captured_image.clear()
        self.captured_frame = None

        # Change the sub-label to indicate the next pain number (for the next pain type, if there is one)
        self.sub_label.setText(f"Douleur n°{pain_index + 2}")

        # Disable the OK button and reset its style
        self.ok_button.setEnabled(False)
        self.ok_button.setStyleSheet("background-color: gray; color: white;")

        # ! Change to next tab based on the pain type
        if self.pain_localization.patient_data[f"pain_type_{pain_index}"] == "Douleur Continue":
            self.pain_localization.tab_widget.setCurrentIndex(4)  # Switch to the next tab (Pain Intensity)
        else:
            self.pain_localization.tab_widget.setCurrentIndex(3)  # Switch to the next tab (Palpation)

    def timer_clicked(self):
        self.timer.start(1000)
        self.timer_update_label.start(100)  # Update label every 100ms
        print("Timer button clicked.")

    def set_current_timer_label(self):
        remaining_time = self.timer.remainingTime()
        if remaining_time > 0:
            self.timer_button.setText(f"{remaining_time / 1000:.1f} Secondes restantes")
        else:
            self.timer_button.setText("Lancer un timer")
            self.timer_update_label.stop()

    def timer_timeout(self):
        print("Timer finished.")
        self.timer_button.setText("Lancer un timer")
        self.timer_update_label.stop()
        self.timer.stop()

        # TODO Call the logic to get localization and elements
        marker_x, marker_y = self.pain_localization.logic.marker_coord
        # scale the coordinates to the static image (500x500)
        # marker_x = marker_x * 500 / self.flux_cam_label.width()
        # marker_y = marker_y * 500 / self.flux_cam_label.height()
        # send_pick_request(int(marker_x), int(marker_y))

        # ! Show the captured image
        captured_image = self.pain_localization.logic.frame.copy()
        self.saved_image = captured_image.copy()  # Save the captured image for dictionary
        if captured_image is not None:
            left_shoulder, right_shoulder = self.pain_localization.logic.detect_shoulders(captured_image)
            if left_shoulder is not None and right_shoulder is not None:
                self.left_shoulder_coord = tuple(left_shoulder)
                self.right_shoulder_coord = tuple(right_shoulder)
                # Draw shoulders on the captured image
                cv2.circle(captured_image, self.left_shoulder_coord, 15, (0, 0, 255), -1)  # Draw left shoulder
                cv2.circle(captured_image, self.right_shoulder_coord, 15, (0, 0, 255), -1)  # Draw right shoulder
            else:
                self.pain_localization.toaster.show_warning("Epaule non détectée, veuillez réessayer.")
                return

            # Detect marker
            marker_coord = self.pain_localization.logic.detect_marker(captured_image, left_shoulder, right_shoulder)
            if marker_coord is not None:
                self.marker_coord = tuple(marker_coord)
                # Draw marker on the captured image
                cv2.circle(captured_image, self.marker_coord, 10, (255, 0, 0), -1)  # Draw marker
            else:
                self.pain_localization.toaster.show_warning("Dispositif non détecté, veuillez réessayer.")
                return

            # Rescale and Convert the drawned image to QImage
            height, width, channel = captured_image.shape
            bytes_per_line = channel * width
            frame = cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB)
            self.captured_frame = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            scaled_img = self.captured_frame.scaled(
                self.pain_localization.logic.size_capture[0],
                self.pain_localization.logic.size_capture[1],
                Qt.AspectRatioMode.KeepAspectRatio,
            )

            self.captured_image.setPixmap(QPixmap.fromImage(scaled_img))

            # ! Enable the OK button and set it to green
            self.ok_button.setEnabled(True)
            self.ok_button.setStyleSheet("background-color: green; color: white;")
        else:
            self.pain_localization.toaster.show_warning("Aucune image capturée, veuillez réessayer.")
            return

    def __init_footer(self):
        pass


class PainLocalizationSignals(QObject):
    """
    Signals to communicate with the worker thread
    """

    change_pixmap_signal = pyqtSignal(QImage)
    start_new_computation_pos = pyqtSignal()


class PainLocalizationLogic(QRunnable):
    """
    Logic class for PainLocalization
    """

    def __init__(self, parent: PainLocalization, worker_frequency: int, video_source: str):
        super().__init__()
        self.parent = parent
        self.signals = PainLocalizationSignals()
        self.worker_frequency = worker_frequency
        self.worker_period = 1 / worker_frequency
        self.video_source = video_source
        self.stopped: EventClass = mp.Event()

        self.frame: cv2.Mat = None
        self.size_capture: tuple[int, int] = (640, 480)

        # ! MODELS
        PATH_MODELS = "models"
        self.yolo_keypoint_model = YOLO(f"{PATH_MODELS}/yolo11n-pose.pt")
        self.yolo_segmentation_model = YOLO(f"{PATH_MODELS}/best.pt")

        # ! Live position of the shoulders and marker
        # ! Used to show on the image
        self.count_frames: int = 0
        self.left_shoulder_coord: tuple[int, int] = (0, 0)
        self.right_shoulder_coord: tuple[int, int] = (0, 0)
        self.marker_coord: tuple[int, int] = (0, 0)

        self.compute_thread: threading.Thread = threading.Thread(
            target=self.routine_compute_new_positions,
            daemon=True,
        )
        self.compute_thread.start()

    def set_size_capture(self, size: tuple[int, int]):
        """
        Set the size of the capture
        :param size: tuple of (width, height)
        """
        self.size_capture = size

    def run(self):
        self.cap = cv2.VideoCapture(self.video_source)
        self.count_frames = 0

        while not self.stopped.wait(timeout=self.worker_period):
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            self.frame = frame.copy()
            self.count_frames += 1

            # ! Draw shoulders and marker on the frame
            cv2.circle(frame, self.left_shoulder_coord, 15, (0, 0, 255), -1)  # Draw left shoulder
            cv2.circle(frame, self.right_shoulder_coord, 15, (0, 0, 255), -1)  # Draw right shoulder
            cv2.circle(frame, self.marker_coord, 10, (255, 0, 0), -1)  # Draw marker

            # ? Rescale and Convert the drawned image to QImage
            height, width, channel = frame.shape
            bytes_per_line = channel * width
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            scaled_img = frame.scaled(self.size_capture[0], self.size_capture[1], Qt.AspectRatioMode.KeepAspectRatio)

            self.signals.change_pixmap_signal.emit(scaled_img)

    def detect_shoulders(self, raw_frame: cv2.Mat) -> tuple[np.ndarray, np.ndarray]:
        """
        This will take the raw frame from the camera and detect the shoulders
        with yolo model,

        It will then return the shoulders on the frame as coordinates:
        - The left shoulder coordinates
        - The right shoulder coordinates
        """
        keypoints_results = self.yolo_keypoint_model(
            source=raw_frame,
            verbose=False,
        )

        if not keypoints_results:
            logger.warning("No keypoints detected.")
            return None, None

        for result in keypoints_results:
            if hasattr(result, "keypoints"):
                keypoints = result.keypoints

                if keypoints is not None and keypoints.shape[0] > 0:
                    keypoints_numpy = keypoints.data.cpu().numpy()[0]

                    left_shoulder = keypoints_numpy[5][:2]
                    right_shoulder = keypoints_numpy[6][:2]

                    # cv2.circle(raw_frame, tuple(left_shoulder.astype(int)), 15, (0, 0, 255), -1)
                    # cv2.circle(raw_frame, tuple(right_shoulder.astype(int)), 15, (0, 0, 255), -1)

            else:
                logger.warning("No keypoints found in the results.")
                return None, None

        return left_shoulder.astype(int), right_shoulder.astype(int)

    def detect_marker(self, raw_frame: cv2.Mat, left_shoulder: np.ndarray, right_shoulder: np.ndarray) -> np.ndarray:
        """
        This will take the raw frame from the camera and detect the marker
        with yolo model,

        It will then return the marker on the frame as coordinates:
        """
        seg_results = self.yolo_segmentation_model(source=raw_frame, verbose=False)

        if not seg_results:
            logger.warning("No segmentation results found.")
            return None

        last_device_location = None

        for result in seg_results:
            masks = getattr(result, "masks", None)
            boxes = getattr(result, "boxes", None)

            if masks is not None and masks.data is not None and boxes is not None:
                classes = boxes.cls
                for i, mask in enumerate(masks.data):
                    cls_id = int(classes[i].item())
                    if cls_id == 2:  # Assuming class 2 is your "device"
                        mask_np = mask.cpu().numpy().astype(np.uint8)
                        ys, xs = np.where(mask_np > 0)
                        if len(xs) == 0:
                            continue

                        median_x = np.median(xs)
                        median_y = np.median(ys)

                        # ? Weird reshape, idk why
                        mask_h, mask_w = mask_np.shape
                        frame_h, frame_w = raw_frame.shape[:2]
                        median_x = int(median_x * frame_w / mask_w)
                        median_y = int(median_y * frame_h / mask_h)

                        last_device_location = (median_x, median_y)
                        # device_x, device_y = last_device_location
                        # avg_shoulder_y = (left_shoulder[1] + right_shoulder[1]) / 2
                        # y_on_static_img = int(100 + (device_y - avg_shoulder_y))
                        # min_x = min(left_shoulder[0], right_shoulder[0])
                        # max_x = max(left_shoulder[0], right_shoulder[0])
                        # percent = ((device_x - min_x) / (max_x - min_x + 1e-6)) * 100
                        # static_x_start = 100
                        # static_x_end = 377
                        # x_on_static_img = int(static_x_start + (percent / 100) * (static_x_end - static_x_start))
                        # print(x_on_static_img, y_on_static_img)
                        # cv2.circle(raw_frame, (int(median_x), int(median_y)), 10, (255, 0, 0), -1)
            else:
                # logger.warning("No masks or boxes found in the segmentation results.")
                return None

        if last_device_location is not None:
            return np.array([int(last_device_location[0]), int(last_device_location[1])])
        return None

    def routine_compute_new_positions(self):
        """
        This routine runs in a separate thread to compute the new positions of the shoulders and marker
        It will use the self.frame, make a copy to avoid changes
        and compute new positions of the shoulders and marker

        """

        while not self.stopped.is_set():
            if self.count_frames % 1 == 0:
                # Get the current frame
                if self.frame is not None:
                    copy_frame = self.frame.copy()

                    # logger.debug(f"Processing frame shape {copy_frame.shape} at frame count {self.count_frames}")

                    # Detect shoulders
                    left_shoulder, right_shoulder = self.detect_shoulders(copy_frame)
                    if left_shoulder is not None and right_shoulder is not None:
                        self.left_shoulder_coord = tuple(left_shoulder)
                        self.right_shoulder_coord = tuple(right_shoulder)

                    # Detect marker
                    marker_coord = self.detect_marker(copy_frame, left_shoulder, right_shoulder)
                    if marker_coord is not None:
                        self.marker_coord = tuple(marker_coord)

            self.count_frames += 1

    def stop(self):
        self.stopped.set()
        self.cap.release()
        # self.captured_image = QLabel("Captured Image", self)
