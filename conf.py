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
    'font': QFont('Trebuchet MS', 9) if platform.system() == 'Windows' else QFont('Trebuchet MS', 13),
    'root': os.getcwd(),
    'logo': os.getcwd() + '/rss/icons/logo.png',
    'qss' : os.getcwd() + '/rss/style/climact.qss',
}

GlobalIcons = {
    'NavBar': {
                'home'  : GlobalConfig['root'] + '/rss/icons/pack-three/home.png',
                'open'  : GlobalConfig['root'] + '/rss/icons/pack-three/open.png',
                'save'  : GlobalConfig['root'] + '/rss/icons/pack-three/cloud.png',
                'build' : GlobalConfig['root'] + '/rss/icons/pack-three/hammer.png',
                'conf'  : GlobalConfig['root'] + '/rss/icons/pack-three/config.png',
                'plot'  : GlobalConfig['root'] + '/rss/icons/pack-three/plot.png',
                'libs'  : GlobalConfig['root'] + '/rss/icons/pack-three/libs.png',
                'python': GlobalConfig['root'] + '/rss/icons/pack-three/python.png',
                'play'  : GlobalConfig['root'] + '/rss/icons/pack-three/execute.png',
                'check' : GlobalConfig['root'] + '/rss/icons/pack-three/check.png',
            },

    'Vertex': {
                'default': GlobalConfig['root'] + '/rss/icons/pack-three/node.svg',
                'router' : GlobalConfig['root'] + '/rss/icons/pack-three/split.svg',
            },

    'SearchBar': GlobalConfig['root'] + '/rss/icons/pack-three/search.png',
}
