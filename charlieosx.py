import json
from robot import Charlie
from logging import Logger
from ui import UI
from pybricks.hubs import EV3Brick
from configParser import parseConfig
from collections import OrderedDict


class CharlieOSX:
    '''TODO'''
    def __init__(self, configPath, settingsPath, logfilePath):
        order = ['Debug Driving', 'Audio-Volume', 'EFX-Volume', 'Logging-level', 'Show Warnings', 'Show Errors']
        try:
            with open(settingsPath, 'r') as f:
                settings = json.load(f)
                sorted_settings = OrderedDict()
                sorted_settings['options'] = OrderedDict()
                for i in range(len(order)):
                    sorted_settings['options'][order[i]] = settings['options'][order[i]]
                sorted_settings['values'] = settings['values']
                sorted_settings['types'] = settings['types']
            self.__settings = sorted_settings
        except Exception as exception:
            print('No settings found, falling back to default values \t caused by:', exception)
            settings = OrderedDict({'options': OrderedDict({'Debug Driving': 2, 'Audio-Volume': 80, 'EFX-Volume': 25, 'Logging-level': 0, 'Show Warnings': True, 'Show Errors': True}),
                                    'values': {
                                        'min': {'Debug Driving': 0, 'Audio-Volume': 0, 'EFX-Volume': 0, 'Logging-level': 0, 'Show Warnings': False, 'Show Errors': False},
                                        'max': {'Debug Driving': 2, 'Audio-Volume': 100, 'EFX-Volume': 100, 'Logging-level': 3, 'Show Warnings': True, 'Show Errors': True}},
                                    'types': {'Debug Driving': 'int', 'Audio-Volume': 'int', 'EFX-Volume': 'int', 'Logging-level': 'int', 'Show Warnings': 'bool', 'Show Errors': 'bool'}})
            with open(settingsPath, 'w') as f:
                f.write(json.dumps(settings, sort_keys = False))
            self.__settings = settings
        self.__logfilePath = logfilePath
        self.brick = EV3Brick()
        self.__config = parseConfig(configPath)
        self.logger = Logger(self.__config, self.__settings, self.__logfilePath, self.brick)
        self.robot = Charlie(self.__config, self.__settings, self.brick, self.logger)
        self.ui = UI(self.__config, self.__settings, self.brick, self.logger)
    #TODO
    def __repr__(self):
        return "TODO"
    #TODO
    def __str__(self):
        return "CharlieOSX"   

    def storeSettings(self, data, path):
        try:
            with open(path, 'w') as f:
                f.write(json.dumps(data, sort_keys = False))
            self.logger.info(self, 'Successfully stored settings')
        except Exception as exception:
            self.logger.error(self, 'Failed to store settings to %s' % path, exception)

    def applySettings(self, settings):
        charlie.speaker.set_volume(settings['options']['Audio-Volume'] * 0.9, 'Beep')
        charlie.speaker.set_volume(settings['options']['EFX-Volume'] * 0.9, 'PCM')
        self.logger.debug(self, 'Applied settings')


