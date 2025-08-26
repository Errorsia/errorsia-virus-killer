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

    def init_ui(self):
        layout = QVBoxLayout()

        # 顶部标签
        self.label1 = QLabel()
        self.label1.setText(self.var)
        # self.label1.setAlignment(Qt.AlignCenter)
        # 这行代码的意思是将 label1（一个标签控件）中的文字居中对齐，也就是让文字在标签中水平和垂直方向都处于中间位置。
        self.label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label1.setStyleSheet(
            "background-color: lightcyan; font-size: 32px;")
        self.label1.setMinimumHeight(100)
        layout.addWidget(self.label1)

