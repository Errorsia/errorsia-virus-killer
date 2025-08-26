from PySide6.QtWidgets import (
    QWidget, QPushButton, QLabel, QTextEdit,
    QComboBox, QGridLayout, QVBoxLayout, QHBoxLayout, QApplication  # , QFrame
)
from PySide6.QtCore import Qt

class MainWidget(QWidget):
    def __init__(self, var, logic, build_log):
        super().__init__()
        self.var = var
        self.logic = logic
        self.build_log = build_log
        self.label1 = None
        # self.debug_frame = self.debug_combobox1 = self.output_text = None
        self.debug_layout = self.debug_combobox1 = self.output_text = None
        self.button1 = self.button2 = self.button3 = self.button4 = self.button5 = None
        self.widgets = None

        self.init_ui()