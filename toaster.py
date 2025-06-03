from PyQt6.QtWidgets import QMainWindow
from pyqttoast import Toast, ToastPreset


class Toaster:
    """
    This class will contain the GUI and logic part for the Toaster
    It will be used to show toast messages in the GUI
    """

    def __init__(self, window: QMainWindow):
        self.window = window

    def show_sucess(self, message: str) -> None:
        toast = Toast(self.window)
        toast.setDuration(2000)
        toast.setTitle("SUCESS")
        toast.setText(message)
        toast.applyPreset(ToastPreset.SUCCESS)
        toast.show()

    def show_error(self, message: str) -> None:
        toast = Toast(self.window)
        toast.setDuration(2000)
        toast.setTitle("ERROR")
        toast.setText(message)
        toast.applyPreset(ToastPreset.ERROR)
        toast.show()

    def show_info(self, message: str) -> None:
        toast = Toast(self.window)
        toast.setDuration(2000)
        toast.setTitle("INFO")
        toast.setText(message)
        toast.applyPreset(ToastPreset.INFORMATION)
        toast.show()

    def show_warning(self, message: str) -> None:
        toast = Toast(self.window)
        toast.setDuration(2000)
        toast.setTitle("WARNING")
        toast.setText(message)
        toast.applyPreset(ToastPreset.WARNING)
        toast.show()
