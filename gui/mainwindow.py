from PySide6.QtWidgets import QMainWindow
from .mainwidget import MainWidget
from PySide6.QtGui import QIcon, QPixmap
import base64
from . import icon


class MainWindow(QMainWindow):
    def __init__(self, var, logger, build_log, logic):
        super().__init__()
        self.var = var

        self.initialization_window()

        # 设置 icon
        self.set_icon()

        # 设置 central widget
        self.main_widget = MainWidget(var, logic, build_log)
        self.setCentralWidget(self.main_widget)

        self.logger = logger
        self.logger.info("Window initialized")

        # 关闭事件绑定
        self.logic = logic