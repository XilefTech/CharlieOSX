from robot import Charlie
from logging import Logger
from ui import UI
from pybricks.hubs import EV3Brick
import yaml

class CharlieOSX:
    def __init__(self, configPath, settingsPath, logfilePath):
        self.__settings = loadSettings(settingsPath)
        self.__logfilePath = logfilePath
        with open(configPath, 'r') as f
            self.__config = yaml.load(f)
        self.brick = EV3Brick()
        self.logger = Logger(self.__config, self.__logfilePath, brick)
        self.robot = Charlie(self.__config, self.__settings, self.brick, self.logger)
        self.ui = UI(self.__config, self.__settings, self.brick, self.logger)
    #TODO
    def __repr__(self):
        return "TODO"
    #TODO
    def __str__(self):
        return "TODO"

    def loadSettings(path):
        order = ['Debug Driving', 'Audio-Volume', 'EFX-Volume', 'Console-Log', 'Show Warnings', 'Show Errors']
        try:
            with open(path, 'r') as f:
                settings = json.load(f)
                sorted_settings = OrderedDict()
                sorted_settings['options'] = OrderedDict()
                for i in range(len(order)):
                    sorted_settings['options'][order[i]] = settings['options'][order[i]]
                sorted_settings['values'] = settings['values']
                sorted_settings['types'] = settings['types']
                return sorted_settings
        except:
            settings = OrderedDict({'options': OrderedDict({'Debug Driving': 2, 'Audio-Volume': 80, 'EFX-Volume': 25, 'Console-Log': True, 'Show Warnings': True, 'Show Errors': True}),
                                    'values': {
                                        'min': {'Debug Driving': 0, 'Audio-Volume': 0, 'EFX-Volume': 0, 'Console-Log': False, 'Show Warnings': False, 'Show Errors': False},
                                        'max': {'Debug Driving': 2, 'Audio-Volume': 100, 'EFX-Volume': 100, 'Console-Log': True, 'Show Warnings': True, 'Show Errors': True}},
                                    'types': {'Debug Driving': 'int', 'Audio-Volume': 'int', 'EFX-Volume': 'int', 'Console-Log': 'bool', 'Show Warnings': 'bool', 'Show Errors': 'bool'}})
            storeSettings(settings, path)
            return settings

    def storeSettings(data, path):
        with open(path, 'w') as f:
            f.write(json.dumps(data, sort_keys = False))

    def applySettings(settings):
        charlie.speaker.set_volume(settings['options']['Audio-Volume'] * 0.9, 'Beep')
        charlie.speaker.set_volume(settings['options']['EFX-Volume'] * 0.9, 'PCM')

