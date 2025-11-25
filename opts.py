# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: conf
# Description: Global options and flags
# ----------------------------------------------------------------------------------------------------------------------

# Global variable(s):
__author__      = 'EnERG Lab, IIT Madras'
__version__     = '1.0'
__license__     = 'N/A'

# Imports:
import os
import platform

from PySide6 import QtGui

# Global configuration dictionary:
GlobalConfig = {
    'name': 'Climate Action Tool',
    'font': QtGui.QFont('Cascadia Mono', 8) if platform.system() == 'Windows' else QtGui.QFont('Monaco', 12),
    'root': os.getcwd(),
    'logo': os.getcwd() + '/rss/icons/logo.png',
    'qss' : os.getcwd() + '/rss/style/climact.qss',
}