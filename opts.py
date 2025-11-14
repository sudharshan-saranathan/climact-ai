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

from PySide6.QtGui import QFont

# Global configuration dictionary:
GlobalConfig = {
    'name': 'Climate Action Tool',
    'font': QFont('Cascadia Mono', 8) if platform.system() == 'Windows' else QFont('Monaco', 12),
    'root': os.getcwd(),
    'logo': os.getcwd() + '/rss/icons/logo.png',
    'qss' : os.getcwd() + '/rss/style/climact.qss',
}

GlobalIcons = {
    'NavBar': {
                'home'  : GlobalConfig['root'] + '/rss/icons/pack-three/home.png',
                'open'  : GlobalConfig['root'] + '/rss/icons/pack-two/open.png',
                'save'  : GlobalConfig['root'] + '/rss/icons/pack-two/save.png',
                'draw'  : GlobalConfig['root'] + '/rss/icons/pack-two/hammer.png',
                'conf'  : GlobalConfig['root'] + '/rss/icons/pack-two/config.png',
                'plot'  : GlobalConfig['root'] + '/rss/icons/pack-two/plot.png',
                'libs'  : GlobalConfig['root'] + '/rss/icons/pack-two/library.png',
                'python': GlobalConfig['root'] + '/rss/icons/pack-two/python.png',
            },
}