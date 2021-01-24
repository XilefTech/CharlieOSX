import os
from copy import deepcopy

class ProfileHelper():
    '''
    ProfileHelper is a helper class to load and save the profiles to a file and load them from that file.

    Args:
        logger (Logger): initialized Logger class used for logging
        config (dict): The path to the config file.
    '''
    def __init__(self, logger, config):
        logger.info(self, 'Initialisating ProfileHelper...')
        self.logger = logger
        self.__config = config
        self.foldername = self.__config['profileFolderName']
        self._data = {}
        self.logger.info(self, 'Done initialisating ProfileHelper...')
        self.loadProfiles()
    
    def __repr__(self):
        return 'TODO'

    def __str__(self):
        return 'ProfileHelper'

    def loadProfiles(self):
        '''
        Loads the data from all the Profiles stored on the brick.
        '''
        self.logger.info(self, 'Loading profiles...')
        try:
            if not self.foldername in os.listdir():
                os.mkdir(self.foldername)
            os.chdir(self.foldername)
            for k in self.__config['profileNames']:
                if not '%s.dat' % k in os.listdir():
                    open('%s.dat' % k, 'a').close()
                self._data[k] = []
                with open('%s.dat' % k, 'r') as dat:
                    for line in dat:
                        l = line.split(', ')
                        intList = [int(s) for s in l]
                        self._data[k].append(intList)
            self.logger.info(self, 'Loaded profiles sucessfully')
        except Exception as exception:
            self.logger.error(self, 'Failed to load Profiles', exception)
        os.chdir('..')

    def _saveProfiles(self):
        '''
        Saves the data of all the Profiles to the brick.
        '''
        self.logger.info(self, 'Saving profiles....')
        try:
            if not self.foldername in os.listdir():
                os.mkdir(self.foldername)
            os.chdir(self.foldername)
            for k in self.__config['profileNames']:
                if not '%s.dat' % k in os.listdir():
                    open('%s.dat' % k, 'a').close()
                ffile = open('%s.dat' % k, 'w')
                strArr = ''
                for l in self._data[k]:
                    for i in l:
                        strArr += str(i) + ', '
                    strArr = strArr[:-2]
                    ffile.write(strArr + '\n')
                    strArr = ''
                ffile.close()
        except Exception as exception:
            self.logger.error(self, 'Failed to save Profiles', exception)
        os.chdir('..')

    def getProfileData(self, profile):
        '''
        Function to get the data of a given profile. WIP

        Args:
            profile (str): The name of the profile

        Returns:
        array: The array of number code arrays frome the given profile
        '''
        try:
            x = deepcopy(self._data[profile])
            return x
        except KeyError as excpetion:
            self.logger.warn(self, 'Couldn\'t get profile data for %s: No such profile in data' % str(exception))
    
    def setProfileData(self, profile, data):
        '''
        Function to set the data of a given profile. WIP

        Args:
            profile (str): The name of the profile
            data (array): The array with the data
        '''
        self.logger.debug(self, 'Setting Profile data for profile "%s"' % profile)
        self._data[profile] = deepcopy(data)
        self._saveProfiles()
