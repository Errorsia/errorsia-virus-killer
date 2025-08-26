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

        # 按钮区域
        button_layout = QGridLayout()

        self.button1 = QPushButton("Kill Viruses")
        self.button1.clicked.connect(self.kill_virus_main)

        self.button2 = QPushButton("Repair Infected Files")
        self.button2.clicked.connect(self.logic.repair_infected_files)

        self.button3 = QPushButton("Auto Kill (Do #1 And #2)")
        self.button3.clicked.connect(self.auto_kill_main)

        self.button4 = QPushButton("Clean Screen")
        self.button4.clicked.connect(self.logic.clean_button)

        # self.button5 = QPushButton("Debugger")
        # self.button5.clicked.connect(self.logic.debugger_button)

        # for i, btn in enumerate([self.button1, self.button2, self.button3, self.button4, self.button5]):
        for i, btn in enumerate([self.button1, self.button2, self.button3, self.button4]):
            btn.setMinimumHeight(50)
            button_layout.addWidget(btn, i // 2, i % 2)

        layout.addLayout(button_layout)

        # Debug Frame
        self.debug_layout = QVBoxLayout()
        debug_label = QLabel("Debugger Output:")
        debug_label.setStyleSheet("font-size: 18px;")
        self.debug_layout.addWidget(debug_label)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.debug_layout.addWidget(self.output_text)

        log_selector_layout = QHBoxLayout()
        log_label = QLabel("Select log output level:")
        self.debug_combobox1 = QComboBox()
        self.debug_combobox1.addItems(
            ["Debug", "Info", "Warning", "Error", "Critical", "Silent"])
        self.debug_combobox1.setCurrentIndex(0 if self.build_log else 5)
        self.debug_combobox1.currentIndexChanged.connect(self.debug_combobox_on_select)
        log_selector_layout.addWidget(log_label)
        log_selector_layout.addWidget(self.debug_combobox1)

        self.debug_layout.addLayout(log_selector_layout)
        layout.addLayout(self.debug_layout)

        # self.widgets = [
        #     self.button1, self.button2, self.button3, self.button4, self.button5, self.debug_combobox1]
        self.widgets = [
            self.button1, self.button2, self.button3, self.button4, self.debug_combobox1]

        self.setLayout(layout)