import _thread, time
from pybricks.parameters import Button, Color
from pybricks.media.ev3dev import Image, ImageFile, Font, SoundFile

class UI:
    def __init__(self, config, settings, brick, logger, settingsPath, storeSettings, applySettings):
        logger.info(self, 'Starting UI initialisation')
        self.__config = config
        self.__settings = settings
        self.__settingsPath = settingsPath
        self.__storeSettings = storeSettings
        self.__applySettings = applySettings
        self.__click = 'assets/media/click.wav'
        self.__confirm = 'assets/media/confirm.wav'
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
        menuState, oldMenuState, position, pos1 = 0, 0, 0, 0
        selected = False
        self.toAnimate = [10, 20, 30, 40, 50]
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

            elif menuState == 50: #settings Menu
                if Button.UP in self.brick.buttons.pressed() and selected:
                        if self.__settings['options'][keys[position]] < self.__settings['values']['max'][keys[position]]:
                            self.__settings['options'][keys[position]] += 1
                        elif self.__settings['options'][keys[position]] == self.__settings['values']['max'][keys[position]]:
                            self.__settings['options'][keys[position]] = self.__settings['values']['min'][keys[position]]
                    self.__sound(self.__click)
                    self.drawSettings(position, self.__settings, selected)
                if Button.DOWN in self.brick.buttons.pressed() and selected:
                        if self.__settings['options'][keys[position]] > self.__settings['values']['min'][keys[position]]:
                            self.__settings['options'][keys[position]] -= 1
                        elif self.__settings['options'][keys[position]] == self.__settings['values']['min'][keys[position]]:
                            self.__settings['options'][keys[position]] = self.__settings['values']['max'][keys[position]]
                        self.__sound('assets/media/click.wav')
                        self.drawSettings(position, self.__settings, selected)
                            
                if Button.CENTER in self.brick.buttons.pressed():
                    self.logger.debug(self, 'Center button pressed from %s' % selected)
                    if selected:
                        self.__storeSettings(self.__settings, self.__settingsPath)
                        self.__applySettings(self.__settings)
                    selected = not selected
                    self.drawMenu(menuState, position = position, selected = selected)
                    time.sleep(0.3)

            if Button.RIGHT in self.brick.buttons.pressed() and not selected:
                self.logger.debug(self, 'Right button triggered at %s' % menuState)
                menuState = menuState * 10
                if menuState in self.toAnimate:
                    self.__sound(self.__confirm)
                time.sleep(0.08)
                    position = 0
                self.animate(menuState, True)
                    self.drawMenu(menuState, position = position, selected = selected)
                else:
                    self.__sound(self.__click)
                self.drawMenu(menuState)
                oldMenuState = menuState ##### to be deleted
                time.sleep(0.4)

            if Button.LEFT in self.brick.buttons.pressed() and not selected:
                self.logger.debug(self, 'Left button triggered at %s' % menuState)
                if menuState in self.toAnimate:
                    self.__sound(self.__confirm)
                time.sleep(0.08)
                self.animate(menuState, False)
                else:
                    self.__sound(self.__click)
                    menuState = menuState / 10
                self.drawMenu(menuState, position = position, selected = selected)
                time.sleep(0.4)

            if Button.UP in self.brick.buttons.pressed() and not selected:
                self.logger.debug(self, 'Up button triggered at %s with position of %s' % (menuState, position))
                self.__sound(self.__click)
                if menuState == 50 and position == 0:
                    position = len(self.__settings['options']) - 1
                elif menuState == 50:
                    position -= 1
                elif menuState in [0, 1]:
                    menuState = 5
                else:
                    menuState -= 1
                if menuState == 50:
                    self.drawMenu(menuState, position = position, selected = selected)
                else:
                    self.drawMenu(menuState)
                time.sleep(0.3)

            if Button.DOWN in self.brick.buttons.pressed() and not selected:
                self.logger.debug(self, 'Down button triggered at %s with position of %s' % (menuState, position))
                self.__sound(self.__click)
                if menuState == 50 and position == len(self.__settings['options']) - 1:
                    position = 0
                elif menuState == 50:
                    position += 1
                elif menuState in [0, 5]:
                    menuState = 1
                else:
                    menuState += 1
                if menuState == 50:
                    self.drawMenu(menuState, position = position, selected = selected)
                else:
                self.drawMenu(menuState)
                time.sleep(0.3)

            if self.logger.getScreenRefreshNeeded() == 1:
                self.logger.setScreenRefreshNeeded(0)
                menuState = menuState / 10

    def drawMenu(self, menuState, **kwargs):
        menus = {0: 'assets/graphics/menus/mainMenu.png',
                1: 'assets/graphics/menus/programmingMainMenu.png',
                2: 'assets/graphics/menus/testingMainMenu.png',
                3: 'assets/graphics/menus/remoteMainMenu.png',
                4: 'assets/graphics/menus/competitionMainMenu.png',
                5: 'assets/graphics/menus/settingsMainMenu.png'
                }
        try:
            if menuState in range(0, 6):
            self.brick.screen.draw_image(0, 0, menus[menuState], transparent = Color.RED)
            elif menuState == 50:
                self.drawSettings(kwargs['position'], self.__settings, kwargs['selected'])
        except Exception as exception:
            self.logger.error(self, "Could not draw menu: %s:" % type(exception).__name__, exception)

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
                self.logger.error(self, "Could not animate menu: ", str(exception))

    def drawDictlist(self, pos, dictlist, selected):
        def drawOptions(value, *args):
            '''Subfunction that draws the 5 current options on the screen'''
            i = 0
            while i <= 4:
                if value + i == pos:
                    if selected:
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.BLACK)
                        self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], dictlist[keys[value + i]]), text_color = Color.WHITE, background_color = None)
                    else:
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.WHITE)
                        self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = False, color = Color.BLACK)
                        self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], dictlist[keys[value + i]]), text_color = Color.BLACK, background_color = None)
                else:
                    self.brick.screen.draw_box(26, 29 + i * 20, 170, 46 + i * 20, fill = True, color = Color.WHITE)
                    self.brick.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], dictlist[keys[value + i]]), text_color = Color.BLACK, background_color = Color.WHITE)
                i += 1

        keys = list(dictlist.keys())
        self.brick.screen.set_font(Font(family = 'arial', size = 13))

        self.drawScrollBar(len(dictlist), pos)

        if pos > 1 and pos < (len(dictlist) - 2):
            drawOptions(pos - 2)
        elif pos == 0:
            drawOptions(pos)
        elif pos == 1:
            drawOptions(pos - 1)
        elif pos == len(dictlist) - 2:
            drawOptions(pos - 3)
        elif pos == len(dictlist) - 1:
            drawOptions(pos - 4)

    def drawList(self, pos, llist):
        def drawOptions(value, *args):
            '''Subfunction that draws the 5 current options on the screen'''
            i = 0
            while i <= 4:
                if value + i == pos:
                    self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.WHITE)
                    self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = False, color = Color.BLACK)
                    self.brick.screen.draw_text(29, 30 + i * 20, llist[value + i], text_color = Color.BLACK, background_color = None)
                else:
                    self.brick.screen.draw_box(26, 29 + i * 20, 170, 46 + i * 20, fill = True, color = Color.WHITE)
                    self.brick.screen.draw_text(29, 30 + i * 20, llist[value + i], text_color = Color.BLACK, background_color = Color.WHITE)
                i += 1

        self.brick.screen.set_font(Font(family = 'arial', size = 13))

        self.drawScrollBar(len(llist), pos)

        if pos > 1 and pos < (len(llist) - 2):
            drawOptions(pos - 2)
        elif pos == 0:
            drawOptions(pos)
        elif pos == 1:
            drawOptions(pos - 1)
        elif pos == len(llist) - 2:
            drawOptions(pos - 3)
        elif pos == len(llist) - 1:
            drawOptions(pos - 4)

    def drawExtendableList(self, pos, llist):
        def drawOptions(value, *args):
            '''Subfunction that draws the 5 current options on the screen'''
            i = 0
            self.brick.screen.draw_box(26, 29, 168, 46 + 5 * 20, fill = True, color = Color.WHITE)
            while i <= 4:
                if value + i > len(llist):
                    pass
                elif value + i == pos:
                    #self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.WHITE)
                    self.brick.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = False, color = Color.BLACK)
                    self.brick.screen.draw_text(29, 30 + i * 20, llist[value + i], text_color = Color.BLACK, background_color = None) if (value + i != len(llist)) else self.brick.screen.draw_image(90, 30 + i * 20, 'assets/graphics/misc/plus-button_selected.png', transparent = Color.RED)
                else:
                    #self.brick.screen.draw_box(26, 29 + i * 20, 170, 46 + i * 20, fill = True, color = Color.WHITE)
                    self.brick.screen.draw_text(29, 30 + i * 20, llist[value + i], text_color = Color.BLACK, background_color = Color.WHITE) if (value + i != len(llist)) else self.brick.screen.draw_image(80, 30 + (i - 1) * 20, 'assets/graphics/misc/plus-button.png', transparent = Color.RED)
                i += 1
        llist.append('')

        self.brick.screen.set_font(Font(family = 'arial', size = 12))

        self.drawScrollBar(len(llist), pos)

        if pos > 1 and pos < (len(llist) - 2):
            drawOptions(pos - 2)
        elif pos == 0:
            drawOptions(pos)
        elif pos == 1:
            drawOptions(pos - 1)
        elif pos == len(llist) - 2:
            drawOptions(pos - 3)
        elif pos == len(llist) - 1:
            drawOptions(pos - 4)


