# -*- coding: utf-8 -*-
# Project Name: Errorsia virus killer
# Version: 4.x.x
# Authors:
#   - Ariskanyaa <Ariskanyaa@outlook.com>
#   - Errorsia <Errorsia@outlook.com>
# License: GNU General Public License v3.0 or later (GPLv3+)
# See: https://www.gnu.org/licenses/gpl-3.0.html

# Project Name: Errorsia virus killer
# Copyright (C) 2024 Errorsia, Ariskanyaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# THE PROGRAMME ONLY RUNS ON WINDOWS(NT) !
# I don't think someone will run an EXE programme on Linux(except wine), MacOS etc.


"""
Main module for Errorsia virus killer
"""

# IMPORTANT NOTICE: This is a Test version. The programme is testing now.

import sys

from PySide6.QtWidgets import QApplication

import evk_build_config as evk_build_ver_config
from gui.mainwindow import MainWindow
# Private Libraries
# from . import evk_logic as logic_module
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))
# from .logic import evk_logic as logic_module
from logic import evk_logic as logic_module


class ErrorsiaVirusKillerApp:
    def __init__(self):
        self.logic = logic_module.ErrorsiaVirusKillerLogic(evk_build_ver_config)

        self.logic.initialization()

        self.logger = self.logic.logger

        self.app = QApplication(sys.argv)
        print(self.app.style().objectName())
        self.user_interface = MainWindow(evk_build_ver_config ,self.logger, self.logic)

        self.logger.info('Successfully initialized gui module')

        self.logic.gui = self.user_interface
        self.logger.info('Successfully loaded logic module')

        self.user_interface.show()
        sys.exit(self.app.exec())


if __name__ == '__main__':
    ErrorsiaVirusKillerApp()

# Project Name: [你的项目名称]
# Author: [你的名字或组织名] <[你的电子邮件或网站]>
# Copyright (C) [年份] [你的名字或组织名]
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
