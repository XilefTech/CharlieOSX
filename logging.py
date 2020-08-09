import time, _thread, os
from pybricks.parameters import Color, Button
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

#TODO Logging into Log file
class Logger:
    '''Logging method for CharlieOSX'''
    def __init__ (self, config, settings, fileLocation, brick):
        self.__config = config
        self.__settings = settings
        if fileLocation == '':
            if not 'logs' in os.listdir():
                os.mkdir('logs')
            os.chdir('logs')

            ts = time.localtime(time.time())
            timeString = ''
            format = [2, 1, 0, '-', 3, '-', 4, '-', 5]
            for i in format:
                if type(i) == int:
                    if len(str(ts[i])) < 2:
                        timeString += '0' + str(ts[i])
                    else:
                        timeString += str(ts[i])
                else:
                    timeString += i
            self.__logFile = open('%s.log' % timeString, 'w')
            os.chdir('..')
        self.info(self, 'Initialisating Logger')
        self.__brick = brick
        self.__refreshScreenNeeded = 0
        self.__sound_lock = _thread.allocate_lock()
        self.info(self, 'Logger initialized')  
    
    def __repr__(self):
        return 'TODO'

    def __str__(self):
        return 'Logger'

    def __sound(self, file):
        def __playSoundFile(soundFile):
            with self.__sound_lock:
                self.__brick.speaker.play_file(soundFile)
        _thread.start_new_thread(__playSoundFile, (file, ))

    def getFormattedTime(self):
        ts = time.localtime(time.time())
        timeString = '['
        format = [2, '.', 1, '.', 0, '-', 3, ':', 4, ':', 5]
        for i in format:
            if type(i) == int:
                if len(str(ts[i])) < 2:
                    timeString += '0' + str(ts[i])
                else:
                    timeString += str(ts[i])
            else:
               timeString += i
        timeString += ']'
        return timeString

    def debug(self, method, msg):
        if self.__settings['options']['Logging-level'] <= 0:
            print(self.getFormattedTime(), '[%s] [Debug]' % str(method), msg)
            self.__logFile.write('%s [%s] [Debug] %s\n' % (self.getFormattedTime(), str(method), msg))

    def info(self, method, msg):
        ''' Makes a log output, without showing anything on the EV3 screen'''
        if self.__settings['options']['Logging-level'] <= 1:
            print(self.getFormattedTime(), '[%s] [Info]' % str(method), msg)
            self.__logFile.write('%s [%s] [Info] %s\n' % (self.getFormattedTime(), str(method), msg))

    def warn(self, method, msg):
        if self.__settings['options']['Logging-level'] <= 2:
            print(self.getFormattedTime(), '[%s] [Warning]' % str(method), msg)
            self.__logFile.write('%s [%s] [Warning] %s\n' % (self.getFormattedTime(), str(method), msg))
        
        if self.__settings['options']['Show Errors']:
            self.__sound(SoundFile.GENERAL_ALERT)
            self.__brick.screen.draw_image(26, 24, 'assets/graphics/notifications/warn.png', transparent = Color.RED)
            self.__brick.screen.draw_text(31, 34, msg, text_color = Color.BLACK)

            if Font.text_width(Font(family = 'arial', size = 7), exception) <= 90:
                self.__brick.screen.draw_text(32, 47, msg, text_color = Color.BLACK)
            elif len(exception) <= 30 * 2:
                msg1, msg2 = msg[:27], msg[27:]
                self.__brick.screen.draw_text(32, 47, msg1, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 57, msg2, text_color = Color.BLACK)
            else:
                msg1, msg2, msg3 = exception[:27], exception[27:53], exception[53:]
                self.__brick.screen.draw_text(32, 47, msg1, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 57, msg2, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 67, msg3, text_color = Color.BLACK)
            
            #wait for user to press middle button
            while not Button.CENTER in self.__brick.buttons.pressed():
                pass
            self.__brick.screen.draw_image(26, 24, 'assets/graphics/notifications/warnSel.png', transparent = Color.RED)
            #wait for user letting button go
            while Button.CENTER in self.__brick.buttons.pressed():
                pass
            self.__refreshScreenNeeded = 1

    def error(self, method, msg, exception):
        if self.__settings['options']['Logging-level'] <= 3:
            print(self.getFormattedTime(), '[%s] [Error]' % str(method), msg, type(exception).__name__, str(exception))
            self.__logFile.write('%s [%s] [Error] %s: %s: %s\n' % (self.getFormattedTime(), str(method), msg, type(exception).__name__, str(exception)))
        
        if self.__settings['options']['Show Errors']:
            self.__sound(SoundFile.GENERAL_ALERT)
            self.__brick.screen.draw_image(26, 24, 'assets/graphics/notifications/error.png', transparent = Color.RED)
            self.__brick.screen.set_font(Font(family = 'arial', size = 7))
            if Font.text_width(Font(family = 'arial', size = 7), exception) <= 90:
                self.__brick.screen.draw_text(32, 47, exception, text_color = Color.BLACK)
            elif len(exception) <= 30 * 2:
                exception1, exception2 = exception[:27], exception[27:]
                self.__brick.screen.draw_text(32, 47, exception1, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 57, exception2, text_color = Color.BLACK)
            else:
                exception1, exception2, exception3 = exception[:27], exception[27:53], exception[53:]
                self.__brick.screen.draw_text(32, 47, exception1, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 57, exception2, text_color = Color.BLACK)
                self.__brick.screen.draw_text(32, 67, exception3, text_color = Color.BLACK)
            
            #wait for user to press middle button
            while not Button.CENTER in self.__brick.buttons.pressed():
                pass
            self.__brick.screen.draw_image(26, 24, 'assets/graphics/notifications/errorSel.png', transparent = Color.RED)
            #wait for user letting button go
            while Button.CENTER in self.__brick.buttons.pressed():
                pass
            self.__refreshScreenNeeded = 1

    def getScreenRefreshNeeded(self):
        return self.__refreshScreenNeeded
    
    def setScreenRefreshNeeded(self, value):
        self.__refreshScreenNeeded = value

    