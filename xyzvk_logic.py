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

    # Check whether OS is Windows nt
    @staticmethod
    def check_operate_system():
        if os.name != 'nt':
            exit('UNSUPPORTED SYSTEMS')

    # Check the working directories
    def check_path(self):
        father_directory = self.appdata + '/Arthur'
        dir_list = ['', '/VirusKiller', '/VirusKiller/Config', '/VirusKiller/Log']

        for dir_tmp in dir_list:
            dir_tmp = father_directory + dir_tmp
            if not os.path.exists(dir_tmp):
                os.mkdir(dir_tmp)

    @staticmethod
    def run_command(command):
        return subprocess.call(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    @staticmethod
    def subprocess_run(command):
        return subprocess.run(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    # Config Module: Read & Check Config
    def read_log_config(self):
        config_path = f'{self.file_directory}/Config/VirusKiller_Configuration.Elysia'

        # Try to read evk_build_ver_config
        if not os.path.isfile(config_path):
            return -1

        try:
            with open(config_path, "r", encoding="UTF-8") as file:
                read_config = file.read()
        except PermissionError:
            return -2

        enable_log = read_config[0]

        if enable_log == "1":
            return 1
        elif enable_log == "0":
            return 0
        else:
            return -1

    def write_log_config(self, build_log):
        log_cfg_content = 1 if build_log else 0
        config_path = f'{self.file_directory}/Config/VirusKiller_Configuration.Elysia'

        self.run_command(f"attrib -s -r -h {config_path}")
        with open(f"{config_path}", "w", encoding="UTF-8") as file:
            file.write(f"{log_cfg_content}")
        self.run_command(f"attrib +s +r +h {config_path}")