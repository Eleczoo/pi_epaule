import multiprocessing as mp
from multiprocessing.synchronize import Event as EventClass

from loguru import logger
from PyQt6.QtCore import QRunnable
from PyQt6.QtWidgets import QWidget


class Avatar:
    """
    This class will contain the GUI and logic part for the Avatar 3D
    """

    def __init__(self):
        logger.info("Initializing Avatar")
        self.gui: AvatarGUI = AvatarGUI()
        self.logic: AvatarLogic = AvatarLogic(self, worker_frequency=30)

        self.gui.init_ui()


class AvatarGUI(QWidget):
    """
    This class will contain the GUI part for the Avatar 3D
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    # ! ---------- UI ----------
    def init_ui(self):
        self.__init_header()
        self.__init_content()
        self.__init_footer()

    def __init_header(self) -> None:
        pass

    def __init_content(self) -> None:
        pass

    def __init_footer(self) -> None:
        pass


class AvatarLogic(QRunnable):
    """
    Good Source : https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
    """

    def __init__(self, parent: Avatar, worker_frequency: int) -> None:
        super().__init__()
        self.parent: Avatar = parent

        self.worker_frequency: int = worker_frequency
        self.worker_period: float = 1 / self.worker_frequency

        self.stopped: EventClass = mp.Event()

    def run(self) -> None:
        while not self.stopped.wait(timeout=self.worker_period):
            logger.debug(f"Running logic at {self.worker_frequency} Hz")

    def stop(self) -> None:
        self.stopped.set()
