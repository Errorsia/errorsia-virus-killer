from PySide6.QtWidgets import QMainWindow
from .mainwidget import MainWidget
from PySide6.QtGui import QIcon, QPixmap
import base64
from . import images


class MainWindow(QMainWindow):
    def __init__(self, var, logger, logic):
        super().__init__()
        self.var = var

        self.initialization_window()

        # 设置 icon
        self.set_icon()

        # 设置 central widget
        self.main_widget = MainWidget(var, logic)
        self.setCentralWidget(self.main_widget)

        self.logger = logger
        self.logger.info("Window initialized")

        # 关闭事件绑定
        self.logic = logic


    def closeEvent(self, event):
        self.logic.handle_close_event()
        event.accept()

    def initialization_window(self):
        self.setWindowTitle(self.var)
        # self.setMinimumSize(1360, 720)
        # self.resize(1360, 720)
        self.setMinimumSize(960, 540)
        self.resize(960, 540)
        # self.setMaximumSize(3840, 2160)

    def set_icon(self):
        image_data = base64.b64decode(images.icon)  # 这是你的 .ico 文件的 base64
        qt_pixmap = QPixmap()
        qt_pixmap.loadFromData(image_data)  # 不指定格式，让 Qt 自动识别
        self.setWindowIcon(QIcon(qt_pixmap))