import time, _thread, os
import customUrequest as urequests
import os
class VersionManagment:
    '''
    
    '''
    def __init__ (self, settings, brick, config, logger):
        logger.info(self, 'Initialisating VersionManagment')
        logger.info(self, "LOOOKKKK %s" % os.getcwd())
        self.wkPath = os.getcwd()
        self.__settings = settings
        self.__brick = brick
        self.__config = config
        self.logger = logger
        self.newAvai = False # As a fallback
        try:
            f = open("VERSION", "r")
            lns = f.readlines()
            f.close()
            ln = lns[0]
            ln = ln.replace("\n", "").replace("\r", "").replace(" ", "")
            self.version = VersionObject()
            self.version.parseFromString(ln)
            self.logger.info(self, 'Using version ' + str(self.version))
        except:
            self.logger.warn(self, "Error reading version!")
        
        ## Check if there is a new version
        self.checkForUpdates()

    def checkForUpdates(self, force=False):
        if(self.__config["checkForUpdates"] or force):
            repoPath = "https://raw.githubusercontent.com/TheGreyDiamond/CharlieOSX/versioningNew/VERSION" ### !!!!! CHANGE IN MERGE TO MAIN REPO !!!!!
            try:
                self.logger.info(self, 'Checking if a new version is avaiable')
                try:
                    os.mkdir(self.wkPath + "/download")
                except:
                    pass
                os.system("rm " + self.wkPath + "/download/VERSION")
                os.system("wget -P " + self.wkPath + "/download " + repoPath + " ")
                f = open("download/VERSION", "r")
                lns = f.readlines()
                ln = lns[0]
                f.close()
                remoteVersion = ln
                remoteVersion = remoteVersion.replace("\n", "").replace("\r", "").replace(" ", "")
                remoteVersionObj = VersionObject()
                remoteVersionObj.parseFromString(remoteVersion)
                self.logger.debug(self, "Done with remote version creation")
                newAvai = not(self.version.isNewer(remoteVersionObj))
                self.newAvai = newAvai
                if(newAvai):
                    self.logger.info(self, "A new version if ready to be downloaded, current version: %s remote version: %s" % (self.version, remoteVersionObj))
                else:
                    self.logger.info(self, "CharlieOSX is up to date with version %s, remote-version: %s" % (self.version, remoteVersionObj))
            except Exception as ex:
                self.logger.error(self, "Unable to check for updates: %s" % ex, ex)

        else:
            self.logger.info(self, 'Skipping update check')
        return self.newAvai
    
    def getUpdateStatus(self):
        ''' 
        Returns True if there is a newer version ready
        '''
        return self.newAvai
    
    def __repr__(self):
        return 'TODO'

    def __str__(self):
        return 'VersionManager'

class VersionObject():
    def __init__(self, major=0, minor=0, fix=0):
        try:
            self.major = int(major)
            self.minor = int(minor)
            self.fix = int(fix)
        except ValueError:
            self.major = 0
            self.minor = 0
            self.fix = 0
    
    def __str__(self):
        return(str(self.major) + "." + str(self.minor) + "." + str(self.fix))

    def __repr__(self):
        return(str(self.major) + "." + str(self.minor) + "." + str(self.fix))
    
    def parseFromString(self, string):
        parts = string.split(".")
        try:
            self.major = int(parts[0])
            self.minor = int(parts[1])
            self.fix = int(parts[2])
        except ValueError:
            return(False)
        else:
            return(True)

    
    def getMajor(self):
        return(self.major)

    def getMinor(self):
        return(self.minor)

    def getFix(self):
        return(self.fix)

    def isNewer(self, remoteVersion):
        '''
        Returns True if the the local version is newer then `remoteVersion`
        '''
        isNewerB = False
        # Starting with Major
        if(self.major >= remoteVersion.getMajor()):
            isNewerB = True
        
        # Then Minor
        if(self.minor >= remoteVersion.getMinor() and self.major >= remoteVersion.getMajor()):
            isNewerB = True
        
        if(self.fix >= remoteVersion.getFix() and self.minor >= remoteVersion.getMinor() and self.major >= remoteVersion.getMajor()):
            isNewerB = True
        
        return(isNewerB)