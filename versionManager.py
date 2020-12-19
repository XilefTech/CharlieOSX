import time, _thread, os
import urequests

class VersionManagment:
    '''
    
    '''
    def __init__ (self, settings, brick, config, logger):
        self.__settings = settings
        self.info(self, 'Initialisating VersionManagment')
        self.__brick = brick
        self.__config = config
        self.logger = logger
        logger.info(self, 'VersionManagment initialized')
        try:  
            ver = config["version"]
            logger.info(self, 'Using version ' + str(ver))
        except:
            logger.warn(self, "Error reading version!")

       
    
    def __repr__(self):
        return 'TODO'

    def __str__(self):
        return 'VersionManager'