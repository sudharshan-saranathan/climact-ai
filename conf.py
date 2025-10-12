# Encoding: utf-8
# Module name: conf
# Description: Global configuration options and flags

# Imports:
import os
import platform

from PySide6.QtGui import QFont

# Global configuration dictionary:
GlobalConfig = {
    'name': 'CLIMACT',
    'font': QFont('Trebuchet MS', 9 if platform.system() == 'Windows' else 13),
    'root': os.getcwd(),
    'logo': os.getcwd() + '/rss/icons/logo.png',
    'qss' : os.getcwd() + '/rss/style/climact.qss',
}

GlobalIcons = {
    'NavBar': {
                'open'  : GlobalConfig['root'] + '/rss/icons/pack-two/open.png',
                'save'  : GlobalConfig['root'] + '/rss/icons/pack-two/save.png',
                'draw'  : GlobalConfig['root'] + '/rss/icons/pack-two/hammer.png',
                'conf'  : GlobalConfig['root'] + '/rss/icons/pack-two/config.png',
                'plot'  : GlobalConfig['root'] + '/rss/icons/pack-two/plot.png',
                'libs'  : GlobalConfig['root'] + '/rss/icons/pack-two/library.png',
                'python': GlobalConfig['root'] + '/rss/icons/pack-two/python.png',
            },
}

