# -*- coding: utf-8 -*-
# Authors:
#   - Ariskanyaa <Ariskanyaa@outlook.com>
#   - Errorsia <Errorsia@outlook.com>
# License: GNU General Public License v3.0 or later (GPLv3+)
# See: https://www.gnu.org/licenses/gpl-3.0.html
# Copyright (C) 2024 Errorsia, Ariskanyaa
#
# This file is part of the xyzvk project and is distributed under
# the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.


"""
Logic module for xyzvk
"""

# Update:
# Rebuild get_removable_drives function
# Rebuild get_volume_label function

import os
import subprocess
import time
import tkinter as tk
from tkinter import messagebox

import win32api
import win32file

# Mudules
import xyzvk_config as config


class ErrorsiaVirusKillerLogic:
    def __init__(self, gui):
        self.gui = gui
        self.logging = self.logger = self.handler = None
        self._log_ready = False

        # Whether TSET ENVIRONMENT
        # test = True

        self.disable_debug_frame = True

        # Get the value of the environment variable %appdata%
        self.appdata = os.getenv("APPDATA")
        # appdata = os.path.expandvars("%APPDATA%")
        self.file_directory = self.appdata + '/Arthur/VirusKiller'

        # Whether show Easter Egg
        # Current condition: On (If Easter_Egg_Index < 0, it's Off)
        self.Easter_Egg = 0

    def set_log(self, log):
        # self.logging = log['logging']
        # self.logger = log['logger']
        # self.handler = log['handler']
        # Safer
        self.logging = log.get('logging')
        self.logger = log.get('logger')
        self.handler = log.get('handler')
        self._log_ready = all([self.logger, self.handler])

    def initialization(self):
        self.check_operate_system()

        self.run_command('chcp 65001')

        self.check_path()