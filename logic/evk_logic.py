# -*- coding: utf-8 -*-
# Authors:
#   - Ariskanyaa <Ariskanyaa@outlook.com>
#   - Errorsia <Errorsia@outlook.com>
# License: GNU General Public License v3.0 or later (GPLv3+)
# See: https://www.gnu.org/licenses/gpl-3.0.html
# Copyright (C) 2024 Errorsia, Ariskanyaa
#
# This file is part of the Errorsia virus killer project and is distributed under
# the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.


"""
Logic module for Errorsia virus killer
"""
import logging
import os
import subprocess
import sys
import time
import tkinter as tk
import tomllib
from copy import deepcopy
from enum import Enum
from tkinter import messagebox

import tomli_w
import win32api
import win32file

# Mudules
import evk_build_config as evk_build_ver_config


class ErrorsiaVirusKillerLogic:
    def __init__(self, gui):
        self.build_Log = None
        self.formatter = None
        self.gui = gui
        self.logging = self.logger = self.handler = None
        # self._log_ready = False

        self.runtime_config_object = self.runtime_config = self.runtime_config_modified = None

        self.disable_debug_frame = True

        # Get the value of the environment variable %appdata%
        self.appdata = os.getenv("APPDATA")
        # appdata = os.path.expandvars("%APPDATA%")
        self.file_directory = os.path.join(self.appdata, 'Errorsia', 'VirusKiller')
        print(self.file_directory)

        # Whether show Easter Egg
        # Current condition: On (If Easter_Egg_Index < 0, it's Off)
        self.Easter_Egg = 0

    # Bad
    # def set_log(self, log):
    #     # Safer
    #     self.logging = log.get('logging')
    #     self.logger = log.get('logger')
    #     self.file_handler = log.get('file_handler')
    #     self._log_ready = all([self.logger, self.file_handler])
    # End

    def initialization(self):
        self.check_operate_system()

        self.run_command('chcp 65001')

        self.check_path()

        self.initialization_runtime_config()

        self.log_initialization()

        self.check_update()

        self.runtime_config_object.auto_decide_write_config()

        self.logger.info('Successfully initialized logic module')

    # Check whether OS is Windows nt
    @staticmethod
    def check_operate_system():
        if os.name != 'nt':
            sys.exit('UNSUPPORTED SYSTEMS')

    # Check the working directories
    def check_path(self):
        father_directory = self.appdata + '/Errorsia'
        dir_list = ['', '/VirusKiller', '/VirusKiller/Config', '/VirusKiller/Log']

        for dir_tmp in dir_list:
            dir_tmp = father_directory + dir_tmp
            if not os.path.exists(dir_tmp):
                os.mkdir(dir_tmp)
                # try:
                #     os.mkdir(dir_tmp)
                #     raise PermissionError
                # except PermissionError as err:
                #     raise PermissionError(f'Cannot create Directory: {dir_tmp} | {err}')

    def initialization_runtime_config(self):
        self.runtime_config_object = ErrorsiaVirusKillerRuntimeConfig(self.file_directory)
        self.runtime_config_object.read_and_analysis_config()
        self.runtime_config = self.runtime_config_object.runtime_config_dict
        print(self.runtime_config)

    @staticmethod
    def run_command(command):
        return subprocess.call(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    @staticmethod
    def subprocess_run(command):
        return subprocess.run(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    def log_initialization(self):
        # Set logger and file file_handler
        self.logger = logging.getLogger(__name__)
        # self.file_handler = logging.FileHandler(f'{self.file_directory}/Log/Log_{time.time():.7f}.evc')
        self.handler = logging.FileHandler(
            os.path.join(self.file_directory, 'Log', 'errorsia_virus_killer_log.evk4logtestv1')
        )

        self.formatter = logging.Formatter(
            '%(asctime)s - %(pathname)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

        match self.runtime_config_object.read_condition:
            case RuntimeFunctionStatus.WARNING:
                build_log = False

            case RuntimeFunctionStatus.SUCCESS:
                log_config = self.runtime_config.get("logging")
                # print(id(log_config), id(self.runtime_config.get("logging")))

                if log_config != {} and log_config:

                    if isinstance(log_config.get("enable_log"), bool):
                        build_log = log_config["enable_log"]

                    else:
                        build_log = self.ask_enable_log()
                        log_config["enable_log"] = build_log
                        self.runtime_config_object.modified = True

                        print(self.runtime_config.get("logging"))
                else:
                    build_log = self.set_log_dict()

            case RuntimeFunctionStatus.FAILURE:
                build_log = self.set_log_dict()

            case _:
                build_log = False

        self.build_Log = build_log

        self.initialization_logger_level(build_log)

    def set_log_dict(self):
        # Create log dict
        self.runtime_config['logging'] = {}
        build_log = self.ask_enable_log()
        # self.runtime_config['logging']['enable_log'] = build_log
        print(self.runtime_config)
        self.runtime_config['logging'].update({'enable_log': build_log})
        print(self.runtime_config)
        self.runtime_config_object.modified = True
        return build_log

    @staticmethod
    def ask_enable_log():
        return tk.messagebox.askokcancel(
            title="Save log or not",
            message="Do you want to save log?\n你想要保存日志吗?"
        )

    def initialization_logger_level(self, build_log):
        if build_log:
            self.handler.setLevel(logging.DEBUG)
            self.logger.setLevel(level=logging.DEBUG)
        else:
            self.handler.setLevel(100)
            self.logger.setLevel(100)

        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    ###############################################################################################
    # Bad
    # def handle_log_config(self):
    #     ask_enable_log = self.read_log_config()
    #     match ask_enable_log:
    #         case 1:
    #             self.build_Log = True
    #         case 0:
    #             self.build_Log = False
    #         case -1:
    #             self.build_Log = tk.messagebox.askokcancel(
    #                 title="Save log or not",
    #                 message="Do you want to save log?\n你想要保存日志吗?"
    #             )
    #         case -2:
    #             self.build_Log = False
    #             # tk.messagebox.showerror("PermissionError")
    #     self.write_log_config(self.build_Log)
    #
    # # Config Module: Read & Check Config
    # def read_log_config(self):
    #     config_path = f'{self.file_directory}/Config/VirusKiller_Configuration.Elysia'
    #
    #     # Try to read evk_build_ver_config
    #     if not os.path.isfile(config_path):
    #         return -1
    #
    #     try:
    #         with open(config_path, "r", encoding="UTF-8") as file:
    #             read_config = file.read()
    #     except PermissionError:
    #         return -2
    #
    #     enable_log = read_config[0]
    #
    #     if enable_log == "1":
    #         return 1
    #     elif enable_log == "0":
    #         return 0
    #     else:
    #         return -1
    #
    # def write_log_config(self, build_log):
    #     log_cfg_content = 1 if build_log else 0
    #     config_path = f'{self.file_directory}/Config/VirusKiller_Configuration.Elysia'
    #
    #     self.run_command(f"attrib -s -r -h {config_path}")
    #     with open(f"{config_path}", "w", encoding="UTF-8") as file:
    #         file.write(f"{log_cfg_content}")
    #     self.run_command(f"attrib +s +r +h {config_path}")
    #
    # def easy_clean_log(self):
    #     # Create a bat to clean all the Logs
    #     if not os.path.exists(f"{self.file_directory}/Log/Clean_Log.bat"):
    #         with open(f"{self.file_directory}/Log/Clean_Log.bat", "w", encoding="UTF-8") as file:
    #             file.write(f"del /f /q *.avk \ndel /f /q *.bat")
    ###############################################################################################

    # Check for updates
    def check_update(self):
        internal_version = int(evk_build_ver_config.INTERNAL_VERSION)
        online_update_version = -1
        local_update_version = int(self.get_local_version())
        # print(local_update_version)

        if internal_version >= online_update_version and internal_version >= local_update_version:
            return

        if online_update_version >= local_update_version:

            execute_update = tk.messagebox.askokcancel(
                'Update Available',
                'A new version is available.\n'
                'Do you want to download the new version?\n\n'
                'You can also ask Errorsia<Errorsia@outlook.com> for the update.\n\n'
            )

            if execute_update:
                print('⚠☣Downloading☣⚠')

                return

            else:
                tk.messagebox.showwarning(
                    'Update Available',
                    'A new version is available.\n'
                    'Please ask Errorsia<Errorsia@outlook.com> for the update.\n\n'
                )

        else:
            tk.messagebox.showwarning(
                'Update Available',
                'A new version is available.\n'
                'Please ask Errorsia<Errorsia@outlook.com> for the update.\n\n'
            )

        sys.exit('UPDATE AVAILABLE')

    def local_update_old(self):
        if os.path.exists(f'{self.file_directory}/Config/Local_Update.Elysia'):

            with open(f'{self.file_directory}/Config/Local_Update.Elysia', 'r') as local_update_config:
                local_version = local_update_config.read()

            if self.is_legal_version(local_version):

                if int(evk_build_ver_config.INTERNAL_VERSION) <= int(local_version):
                    return local_version

        self.build_local_update_config()
        return -1

    def get_local_version(self):
        if self.runtime_config_object.read_condition == RuntimeFunctionStatus.WARNING:
            return -1

        local_update_config = self.runtime_config.get('app')
        if local_update_config:
            if local_update_config.get('internal_version') and self.is_legal_version(
                    local_update_config.get('internal_version')):
                return local_update_config.get('internal_version')
            else:
                local_update_config['internal_version'] = evk_build_ver_config.INTERNAL_VERSION
        else:
            self.runtime_config['app'] = {}
            self.runtime_config['app']['internal_version'] = evk_build_ver_config.INTERNAL_VERSION
            self.runtime_config_object.modified = True
        return -1

    # Check whether local_version is legal
    @staticmethod
    def is_legal_version(local_version):
        local_version = str(local_version)
        digit_is_int = 0

        if len(local_version) != 9:
            return False

        for tmp_local_version in local_version:
            for tmp_num in range(10):
                if tmp_local_version == str(tmp_num):
                    digit_is_int += 1
                    break

        if digit_is_int == 9:
            return True
        else:
            return False

    #     return local_version.isdigit()

    def build_local_update_config(self):
        if os.path.exists(f'{self.file_directory}/Config/Local_Update.Elysia'):
            self.run_command(f'attrib -r -h {self.file_directory}/Config/Local_Update.Elysia')

        with open(f'{self.file_directory}/Config/Local_Update.Elysia', 'w', encoding="UTF-8") as local_version:
            local_version.write(evk_build_ver_config.INTERNAL_VERSION)

        self.run_command(f'attrib +r +h {self.file_directory}/Config/Local_Update.Elysia')

    @staticmethod
    def get_removable_drives():
        drives = []
        drive_bits = win32file.GetLogicalDrives()
        for i in range(26):
            if drive_bits & (1 << i):
                drive_letter = f"{chr(65 + i)}"
                drive_path = f"{chr(65 + i)}:\\"
                drive_type = win32file.GetDriveType(drive_path)
                # DRIVE_REMOVABLE = 2
                if drive_type == win32file.DRIVE_REMOVABLE:
                    drives.append(drive_letter)
        return drives

    # Virus killer main module
    def kill_viruses(self):
        self.set_insert_simplified('\nKilling Processes:')

        # If you want to add more viruses' processes. Add them in here.
        virus_processes = ['Rundll32.exe', 'AvastSvc.exe', 'wscript.exe', 'Autolt3.exe']  # 'cmd.exe'

        for processes in virus_processes:
            self.taskkill_processes(processes)

        self.handle_virus_files()

    # Virus killer module: Taskkill virus processes
    def taskkill_processes(self, process_name):
        module_name = 'taskkill_processes'
        result_taskkill = self.run_command(f"TASKKILL -F -IM {process_name} -T")

        if result_taskkill == 0:
            condition = 'success'
            output_content = f'The process has been terminated'
            self.logger.info(f'The process ({process_name}) has been terminated (Return code {result_taskkill})')

        elif result_taskkill == 128:
            condition = 'failed'
            output_content = f'The process not found'
            self.logger.warning(f'The process ({process_name}) not found (Return code {result_taskkill})')

        elif result_taskkill == 1:
            condition = 'failed'
            output_content = 'The process could not be terminated'
            self.logger.warning(f'The process ({process_name}) could not be terminated (Return code {result_taskkill})')

        else:
            condition = 'failed'
            output_content = 'Unknown Error: Please tell developers!!'
            self.logger.warning(f'Unknown Error (Return code {result_taskkill})')

        self.set_insert(module_name, condition, output_content)

    def get_volume_label(self, drive_letter):
        drive = drive_letter.upper().rstrip(':\\') + ':\\'
        try:
            # noinspection PyUnresolvedReferences
            volume_info = win32api.GetVolumeInformation(drive)
            return volume_info[0]  # 第一个元素是卷标
        except Exception as err:
            print(f"An error occurred: {err}")
            self.logger.error(f"An error occurred: {err}")
            return None

    # Virus Files Rename Module: Rename the Virus Files
    def handle_virus_files(self):
        module_name = 'handle_virus_files'
        condition_list = []
        log_content_list = []

        self.set_insert_simplified('\nRenaming Files:')

        # If you want to add more dirs. Add them in here. <--Old comment
        # Auto get removable drives
        removable_drives = self.get_removable_drives()

        if removable_drives:
            for disk in removable_drives:
                current_disk_name = self.get_volume_label(disk)

                if os.path.exists(f'{disk}:\\{current_disk_name}.lnk'):
                    os.remove(f'{disk}:\\{current_disk_name}.lnk')
                    condition_list.append('success')
                    log_content_list.append(f'Success to remove virus files in {disk}-disk')
                    self.logger.info(f'Success to rename virus files in {disk}-disk')
                else:
                    condition_list.append('failed')
                    log_content_list.append(f'Virus files not found')
                    self.logger.warning(f'Virus files not found')

        else:
            condition_list.append('failed')
            self.logger.warning(f'Removable disk not found')
            log_content_list.append(f'Removable disk not found')

        for cnt in range(0, len(log_content_list)):
            log_content = log_content_list[cnt]
            condition = condition_list[cnt]

            self.set_insert(module_name, condition, log_content)

    # Virus File Repair Module: Show hidden files
    def repair_infected_files(self):
        self.set_insert_simplified('\nShowing Hidden Files:')

        # If you want to add other dirs. Add it in here.
        disks = self.get_removable_drives()

        module_name = 'repair_infected_files'

        condition_list = []
        log_content_list = []

        if disks:
            for disk in disks:
                infected_folder_path = f'{disk}:\\ '
                result_repair_infected_folder = None

                if os.path.exists(infected_folder_path):
                    self.subprocess_run(['attrib', '-r', infected_folder_path, '/d', '/s'])
                    result_repair_infected_folder = self.subprocess_run(
                        ['attrib', '-s', '-h', '-r', infected_folder_path, '/d']).returncode

                    if result_repair_infected_folder == 0:
                        self.logger.info(
                            f'The attribute of the Infected folder in {disk}-disk has been changed (Return code {result_repair_infected_folder})')
                        condition_list.append('success')
                        log_content_list.append(f'The attribute of the Infected folder in {disk}-disk was changed')

                    else:
                        self.logger.warning(f'The attribute of the Infected folder cannot be changed')
                        condition_list.append('failed')
                        log_content_list.append(f'The attribute of the Infected folder cannot be changed')

                if os.path.exists(f'{disk}:\\ \\desktop.ini'):
                    result_change_attrib_of_virus_files = self.subprocess_run(
                        ['attrib', '-s', '-h', '-R', f'{disk}:\\ \\desktop.ini', "/d"])

                    if result_change_attrib_of_virus_files.returncode == 0:
                        self.logger.info(
                            f'The attribute of the virus file ({disk}:\\xa0\\desktop.ini) has been changed (Return {result_change_attrib_of_virus_files})')
                        condition_list.append('success')
                        log_content_list.append(f'The attribute of the virus file in {disk}-disk was changed')

                        os.remove(f'{disk}:\\ \\desktop.ini')
                        self.logger.info(f'Virus file ({disk}:\\xa0\\desktop.ini) has been removed')
                        condition_list.append('success')
                        log_content_list.append(f'Virus file in {disk}-disk was renamed')

                    else:
                        self.logger.warning(f'The attribute of the virus file cannot be changed')
                        condition_list.append('failed')
                        log_content_list.append(f'The attribute of the virus file cannot be changed')

                if result_repair_infected_folder == 0 and os.path.exists(infected_folder_path):
                    # os.rename(infected_folder_path, f'{disk}:\\Files Hidden by Viruses')
                    # os.rename(infected_folder_path, f'{disk}:\\被病毒隐藏的文件')

                    # self.logger.info(f'Infected folder in {disk}-disk has been renamed')
                    # condition_list.append('success')
                    # log_content_list.append(f'Infected folder in {disk}-disk was renamed')

                    try:
                        os.rename(infected_folder_path, f'{disk}:\\Files Hidden by Viruses')
                        # os.rename(infected_folder_path, f'{disk}:\\被病毒隐藏的文件')
                        self.logger.info(f'Infected folder in {disk}-disk has been renamed')
                    except PermissionError as error:
                        self.logger.error(f'Permission denied: {error}')
                        condition_list.append('failed')
                        log_content_list.append(f'Permission denied')
                        # print('Permission denied. Please run the script as an administrator.')
                    except FileNotFoundError:
                        self.logger.error(f'The directory does not exist')
                        condition_list.append('failed')
                        log_content_list.append(f'The directory does not exist')
                        # print(f'The directory does not exist.')
                    except Exception as error:
                        self.logger.error(f'An error occurred: {error}')
                        condition_list.append('failed')
                        log_content_list.append(f'An error occurred: {error}')
                        # print(f'An error occurred: {error}')

                else:
                    self.logger.warning(f'The directory does not exist')
                    condition_list.append('failed')
                    log_content_list.append(f'The directory does not exist')
                    # print(f'The directory does not exist.')

        else:
            self.logger.warning(f'Removable disk not found')
            condition_list.append('failed')
            log_content_list.append(f'Removable disk not found')

        for cnt in range(0, len(log_content_list)):
            log_content = log_content_list[cnt]
            condition = condition_list[cnt]

            output_content = log_content
            self.set_insert(module_name, condition, output_content)

    # Call two functions
    def auto_kill(self):
        self.kill_viruses()
        self.repair_infected_files()

    # Clean Screen Module: Clean Screen & Output
    def clean_button(self):
        self.gui.main_widget.label_top.setText(evk_build_ver_config.FULL_VERSION)
        self.gui.main_widget.output_text.setText('')
        print('-' * 20)

        self.easter_egg()

    # Easter_Egg_Index module
    def easter_egg(self):
        if self.Easter_Egg < 0:
            pass
        elif self.Easter_Egg < 4:
            self.Easter_Egg += 1
        else:
            self.gui.main_widget.label_top.setText("Copyright (C) 2025 Errorsia ")

            self.logger.debug('=' * 37)
            self.logger.debug('Copyright 2025 Errorsia')
            self.logger.debug('The Easter Egg was discovered by you!')
            self.logger.debug('Developer:\tErrorsia')
            self.logger.debug('Email:\tErrorsia@outlook.com')
            self.logger.debug('=' * 37)

            self.Easter_Egg = 0

    def debugger_button(self):
        if self.disable_debug_frame:
            self.gui.main_widget.settings_page_layout.hide()
            self.disable_debug_frame = False
        else:
            self.gui.main_widget.settings_page_layout.show()
            self.disable_debug_frame = True

    # Get the value of the combobox automatically and set the level of the logger & file_handler
    # noinspection PyUnusedLocal
    # def set_log_level(self, level):
    #     if level == 'Debug':
    #         self.file_handler.setLevel(self.logging.DEBUG)
    #         self.logger.setLevel(level=self.logging.DEBUG)
    #     elif level == 'Info':
    #         self.file_handler.setLevel(self.logging.INFO)
    #         self.logger.setLevel(level=self.logging.INFO)
    #     elif level == 'Warning':
    #         self.file_handler.setLevel(self.logging.WARNING)
    #         self.logger.setLevel(level=self.logging.WARNING)
    #     elif level == 'Error':
    #         self.file_handler.setLevel(self.logging.ERROR)
    #         self.logger.setLevel(level=self.logging.ERROR)
    #     elif level == 'Critical':
    #         self.file_handler.setLevel(self.logging.CRITICAL)
    #         self.logger.setLevel(level=self.logging.CRITICAL)
    #     elif level == 'Silent':
    #         self.file_handler.setLevel(100)
    #         self.logger.setLevel(100)
    #     else:
    #         # This won't happen
    #         self.file_handler.setLevel(self.logging.INFO)
    #         self.logger.setLevel(level=self.logging.INFO)

    # Get the value of the combobox automatically and set the level of the logger & file_handler
    # noinspection PyUnusedLocal
    def set_log_level(self, level_index):
        if level_index > 5 or level_index < 0:
            # This won't happen
            self.handler.setLevel(self.logging.INFO)
            self.logger.setLevel(level=self.logging.INFO)

        logging_level = [
            self.logging.DEBUG,
            self.logging.INFO,
            self.logging.WARNING,
            self.logging.ERROR,
            self.logging.CRITICAL,
            100
        ]

        self.handler.setLevel(logging_level[level_index])
        self.logger.setLevel(level=logging_level[level_index])

    def set_insert_simplified(self, content):
        minus_sign_quantity = '-' * 50
        output = f'{minus_sign_quantity} <b>{content}</b> {minus_sign_quantity}<br>'

        self.gui.main_widget.output_text.append(output)

    def set_insert(self, module, condition, content):
        current_time = time.asctime()[-13:-5]

        module = module.upper()
        condition = condition.upper()

        output = f'{current_time} | [{module}]\t|\t{condition}\t|\t{content}'

        self.gui.main_widget.output_text.append(output)

    def handle_close_event(self):
        self.logger.info('Application shutdown initiated by user')
        self.logger.info('Graceful termination completed')


class RuntimeFunctionStatus(Enum):
    SUCCESS = 1
    FAILURE = 2
    WARNING = 3


class ErrorsiaVirusKillerRuntimeConfig:
    def __init__(self, file_directory):
        self.runtime_config_dict = {}
        self.runtime_config_dict_original = None
        self.modified = False
        self.file_directory = file_directory
        self.read_condition = None
        self.write_condition = None
        self.condition = False
        self.config_path = os.path.join(self.file_directory, 'Config', 'ErrorsiaVirusKillerConfig.evk4configtestv1')  # evc

    def flush_condition(self):
        # self.condition = all(cond == RuntimeConfigStatus.SUCCESS for cond in [self.read_condition, self.write_condition])
        self.condition = self.all_success(
            self.read_condition,
            self.write_condition,
            # self.execute_condition
        )

    def all_success(*statuses):
        return all(s == RuntimeFunctionStatus.SUCCESS for s in statuses)

    def read_and_analysis_config(self):
        """
        Read config file and analysis data from it.
        
        :return: SUCCESS if successfully loads the config file, FAILURE otherwise.
            If confile doesn't exist,WARNING if errors are recorded.
        """
        if not os.path.exists(self.config_path):
            self.read_condition = RuntimeFunctionStatus.FAILURE
            self.runtime_config_dict_original = deepcopy(self.runtime_config_dict)
            return RuntimeFunctionStatus.FAILURE
        if os.path.getsize(self.config_path) > 8192:
            # Config won't be that large
            self.read_condition = RuntimeFunctionStatus.FAILURE
            self.runtime_config_dict_original = deepcopy(self.runtime_config_dict)
            return RuntimeFunctionStatus.FAILURE
        # noinspection PyBroadException
        try:
            # Analysis toml file, write the data into dictionary
            with open(self.config_path, "rb") as runtime_config_file:
                self.runtime_config_dict = tomllib.load(runtime_config_file)

            self.read_condition = RuntimeFunctionStatus.SUCCESS
        except PermissionError:
            self.read_condition = RuntimeFunctionStatus.WARNING
        except tomllib.TOMLDecodeError:
            # Incorrect format of TOML file
            self.read_condition = RuntimeFunctionStatus.FAILURE
        except Exception as err:
            print(err, type(err))
            print('Invalid value' in err)
            self.read_condition = RuntimeFunctionStatus.WARNING
        finally:
            self.flush_condition()
            print(self.read_condition)
            self.runtime_config_dict_original = deepcopy(self.runtime_config_dict)

            return self.read_condition

    def auto_decide_write_config(self):
        if self.modified or self.runtime_config_dict != self.runtime_config_dict_original:
            if self.runtime_config_dict == {}:
                self.write_condition = RuntimeFunctionStatus.WARNING
                raise FileNotFoundError('Empty runtime config')
            else:
                # Write runtime config into toml file
                # noinspection PyBroadException
                try:
                    with open(self.config_path, "wb") as runtime_config_file:
                        tomli_w.dump(self.runtime_config_dict, runtime_config_file)
                    self.write_condition = RuntimeFunctionStatus.SUCCESS
                except PermissionError:
                    self.write_condition = RuntimeFunctionStatus.WARNING
                except Exception:
                    self.write_condition = RuntimeFunctionStatus.WARNING
                finally:
                    self.flush_condition()
                    return self.write_condition
