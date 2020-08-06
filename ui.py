import _thread, time
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

class UI:
    def __init__(self, config, settings, brick, logger, settingsPath, storeSettings):
        logger.info(self, 'Starting UI initialisation')
        self.__config = config
        self.__settings = settings
        self.__settingsPath = settingsPath
        self.__storeSettings = storeSettings
        self.brick = brick
        self.logger = logger
        self.__sound_lock = _thread.allocate_lock()
        self.logger.info(self, 'UI initialized')
    #TODO
    def __repr__(self):
        return "TODO"
    #TODO
    def __str__(self):
        return "UI"

    def __sound(self, file):
        def __playSoundFile(soundFile):
            with self.__sound_lock:
                self.brick.speaker.play_file(soundFile)
        _thread.start_new_thread(__playSoundFile, (file, ))

    def mainLoop(self):
        menuState, oldMenuState, position = 0, 0, 0
        oldPos = 1
        loop, selected = True, False
        self.drawMenu(int(menuState))
        keys = list(self.__settings['options'].keys())
        self.__storeSettings(self.__settings, self.__settingsPath)
        while loop:
            # navigation inbetween main pages
            if menuState == 0:
                if Button.UP in self.brick.buttons.pressed():
                    menuState = 5
                elif Button.DOWN in self.brick.buttons.pressed():
                    menuState = 1
            elif menuState > 0 and menuState < 6:
                if Button.UP in self.brick.buttons.pressed() and menuState > 1:
                    menuState -= 1
                elif Button.UP in self.brick.buttons.pressed() and menuState == 1:
                    menuState = 5
                if Button.DOWN in self.brick.buttons.pressed() and menuState < 5:
                    menuState += 1
                elif Button.DOWN in self.brick.buttons.pressed() and menuState == 5:
                    menuState = 1
            
            # subMenus
            elif menuState == 50: #settings Menu

                if Button.UP in self.brick.buttons.pressed():
                    if not selected:
                        if position > 0:
                            position -= 1
                        elif position == 0:
                            position = len(self.__settings['options']) - 1
                    else:
                        if self.__settings['options'][keys[position]] < self.__settings['values']['max'][keys[position]]:
                            self.__settings['options'][keys[position]] += 1
                        elif self.__settings['options'][keys[position]] == self.__settings['values']['max'][keys[position]]:
                            self.__settings['options'][keys[position]] = self.__settings['values']['min'][keys[position]]
                        self.__sound('assets/media/click.wav')
                        drawSettings(position, self.__settings, selected)
                if Button.DOWN in self.brick.buttons.pressed():
                    if not selected:
                        if position < len(self.__settings['options']) - 1:
                            position += 1
                        elif position == len(self.__settings['options']) - 1:
                            position = 0
                    else:
                        if self.__settings['options'][keys[position]] > self.__settings['values']['min'][keys[position]]:
                            self.__settings['options'][keys[position]] -= 1
                        elif self.__settings['options'][keys[position]] == self.__settings['values']['min'][keys[position]]:
                            self.__settings['options'][keys[position]] = self.__settings['values']['max'][keys[position]]
                        self.__sound('assets/media/click.wav')
                        self.drawSettings(position, self.__settings, selected)
                            


                if Button.CENTER in self.brick.buttons.pressed():
                    if selected:
                        storeSettings(self.__settings)
                        applySettings(self.__settings)
                        
                    selected = not selected
                    oldPos += 1

                if position != oldPos:
                    self.__sound('assets/media/click.wav')
                    self.drawSettings(position, self.__settings, selected)
                    oldPos = position
                    time.sleep(0.07)

            # selection of pages
            if Button.RIGHT in self.brick.buttons.pressed() and menuState > 0 and menuState <= 5 and not selected:
                menuState = menuState * 10
                position, oldPos = 0, 1
                oldMenuState = menuState
                self.__sound('assets/media/confirm.wav')
                time.sleep(0.08)
                self.animate(menuState, True)
                self.drawMenu(menuState)
                time.sleep(0.4)

            if Button.LEFT in self.brick.buttons.pressed() and menuState >= 10 and not selected:
                self.__sound('assets/media/confirm.wav')
                time.sleep(0.08)
                self.animate(menuState, False)
                menuState = menuState / 10
                self.drawMenu(menuState)
                oldMenuState = menuState
                time.sleep(0.4)


            if oldMenuState != menuState:
                self.__sound('assets/media/click.wav')
                time.sleep(0.08)
                self.drawMenu(menuState)
                oldMenuState = menuState
                time.sleep(0.3)

            if self.logger.getScreenRefreshNeeded == 1:
                self.logger.setScreenRefreshNeeded = 0
                menuState = menuState / 10

    def drawMenu(self, menuState):
        menus = {0: 'assets/graphics/menus/mainMenu.png',
                1: 'assets/graphics/menus/programmingMainMenu.png',
                2: 'assets/graphics/menus/testingMainMenu.png',
                3: 'assets/graphics/menus/remoteMainMenu.png',
                4: 'assets/graphics/menus/competitionMainMenu.png',
                5: 'assets/graphics/menus/settingsMainMenu.png'
                }
        try:
            self.brick.screen.draw_image(0, 0, menus[menuState], transparent = Color.RED)
        except Exception as exception:
            self.logger.error(self, "Could not draw menu: ", str(exception))

    def drawScrollBar(self, totalLength, pos):
        self.brick.screen.draw_box(171, 25, 177, 127, r = 2, fill = False, color = Color.BLACK)
        self.brick.screen.draw_box(172, 26, 176, 126, r = 2, fill = True, color = Color.WHITE)
        self.brick.screen.draw_box(173, 27 + 102 / totalLength * pos, 175, 23 + 102 / totalLength * (pos + 1), r = 1, fill = True, color = Color.BLACK)

    def drawSettings(self, pos, settings, selected):
        def drawOptions(value, *args):
            '''Subfunction that draws the 5 current options on the screen'''
            i = 0
            while i <= 4:
                if value + i == pos:
                    if selected:
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.BLACK)
                        self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.WHITE, background_color = None) if settings['types'][keys[value + i]] == 'int' else self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.WHITE, background_color = None)
                    else:
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.WHITE)
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = False, color = Color.BLACK)
                        self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.BLACK, background_color = None) if settings['types'][keys[value + i]] == 'int' else self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.BLACK, background_color = None)
                else:
                    self.brick.screen.draw_box(26, 29 + i * 20, 170, 46 + i * 20, fill = True, color = Color.WHITE)
                    self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.BLACK, background_color = Color.WHITE) if settings['types'][keys[value + i]] == 'int' else self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.BLACK, background_color = Color.WHITE)
                i += 1

        keys = list(settings['options'].keys())
        self.brick.screen.set_font(Font(family = 'arial', size = 13))

        self.drawScrollBar(len(settings['options']), pos)

        if pos > 1 and pos < (len(settings['options']) - 2):
            drawOptions(pos - 2)
        elif pos == 0:
            drawOptions(pos)
        elif pos == 1:
            drawOptions(pos - 1)
        elif pos == len(settings['options']) - 2:
            drawOptions(pos - 3)
        elif pos == len(settings['options']) - 1:
            drawOptions(pos - 4)

    def animate(self, state, direction):
        menus = {10: 'mainProgram',
                20: 'mainTest',
                30: 'mainRemote',
                40: 'mainCompetition',
                50: 'mainSettings'}
        if direction:
            i = 1
            try:
                while i <= 10: 
                    self.brick.screen.draw_image(0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
                    i += 1
            except Exception as exception:
                self.logger.error(self, "Could not animate menu: ", str(exception))
        else:
            i = 10
            try:
                while i >= 1:
                    self.brick.screen.draw_image(0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
                    i -= 1
            except Exception as exception:
                self.logger.error("Could not animate menu: ", str(exception))
