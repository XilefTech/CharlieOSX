import json
from robot import Charlie
from logging import Logger
from ui import UI
from pybricks.hubs import EV3Brick
from configParser import parseConfig
from collections import OrderedDict
from webremote import Webremote

from UI.uiManager import UIManager


class CharlieOSX:
    '''
    CharlieOSX is the Head-Class of this project.
    Here all the other classes get initialited accordingly and all strings come together.
    Also this class should be used to access all the subclasses and its functions.

    Args:
        configPath (str): The path to the config file. Default: 'config.cfg'
        settingsPath (str): The path to the settings file. Default: 'settings.json'
        logfilePath (str): The path to the folder for the log files. Default: ''

    Attributes: 
        brick (EV3Brick): EV3Brick class
        logger (Logger): Logger class
        robot (Charlie): Robot class
        ui (UI): UI class
    '''

    def __init__(self, configPath, settingsPath, logfilePath):
        self.__settings = self.loadSettings(settingsPath)
        self.brick = EV3Brick()
        self.logger = Logger(self.__settings, logfilePath, self.brick)
        self.__config = parseConfig(configPath, self.logger)

        self.robot = Charlie(self.__config, self.brick, self.logger)
        self.webremote = Webremote(self.__config, self.robot, self.brick)
        self.ui = UIManager(self.__config, self.__settings, self.brick, self.logger, settingsPath)

        self.applySettings(self.__settings)
    # TODO

    def __repr__(self):
        return "TODO"
    # TODO

    def __str__(self):
        return "CharlieOSX"

    def storeSettings(self, data, path):
        '''
        Stores given data as a Json stream into a file at the given path

        Args:
            data (dict): The Settings dict that sould be stored
            path (str): The path to the settings file
        '''
        try:
            with open(path, 'w') as f:
                f.write(json.dumps(data, sort_keys=False))
            self.logger.info(self, 'Successfully stored settings')
        except Exception as exception:
            self.logger.error(
                self, 'Failed to store settings to %s' % path, exception)

    def applySettings(self, settings):
        '''
        Applies the settings from the given dict to (currently only) the volume of sounds.
        In other places, the data is often directly taken from the dict.

        Args:
            settings (dict): The Settings dict that sould be used for applying the settings
        '''
        self.brick.speaker.set_volume(
            settings['options']['Audio-Volume'] * 0.9, 'Beep')
        self.brick.speaker.set_volume(
            settings['options']['EFX-Volume'] * 0.9, 'PCM')
        self.logger.debug(self, 'Applied settings')

    def loadSettings(self, settingsPath):
        '''
        Loads the settings from the given Json file into a dict.
        If the given file does not exist, it will restore the default settings and create a new file with them.

        Args:
            settingsPath (str): The path to the Json file to read from.
        '''
        print('[%s] [Debug]' % '[ChalieOSX]', 'Started loading settings')
        order = ['Debug Driving', 'Audio-Volume', 'EFX-Volume',
                 'Logging-level', 'Show Warnings', 'Show Errors']
        try:
            with open(settingsPath, 'r') as f:
                settings = json.load(f)
                sorted_settings = OrderedDict()
                sorted_settings['options'] = OrderedDict()
                for i in range(len(order)):
                    sorted_settings['options'][order[i]
                                               ] = settings['options'][order[i]]
                sorted_settings['values'] = settings['values']
                sorted_settings['types'] = settings['types']
            print('[%s] [Debug]' % '[ChalieOSX}',
                  'Successfully loaded settings')
            return sorted_settings
        except Exception as exception:
            print('[%s] [Debug]' % '[ChalieOSX]',
                  'No settings found, falling back to default values \t caused by:', exception)
            settings = OrderedDict({'options': OrderedDict({'Debug Driving': 2, 'Audio-Volume': 80, 'EFX-Volume': 25, 'Logging-level': 0, 'Show Warnings': True, 'Show Errors': True}),
                                    'values': {
                                        'min': {'Debug Driving': 0, 'Audio-Volume': 0, 'EFX-Volume': 0, 'Logging-level': 0, 'Show Warnings': False, 'Show Errors': False},
                                        'max': {'Debug Driving': 2, 'Audio-Volume': 100, 'EFX-Volume': 100, 'Logging-level': 3, 'Show Warnings': True, 'Show Errors': True}},
                                    'types': {'Debug Driving': 'int', 'Audio-Volume': 'int', 'EFX-Volume': 'int', 'Logging-level': 'int', 'Show Warnings': 'bool', 'Show Errors': 'bool'}})
            with open(settingsPath, 'w') as f:
                f.write(json.dumps(settings, sort_keys=False))
            return settings
