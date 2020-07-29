class UI:
    def __init__(self, configPath, settingsPath, brick, logger):
        self.__configPath = configPath
        self.__settingsPath = settingsPath
        self.brick = brick
        self.logger = logger
    #TODO
    def __repr__(self):
        return "TODO"
    #TODO
    def __str__(self):
        return "TODO"

    def mainLoop():
        menuState, oldMenuState, position = 0, 0, 0
        oldPos = 1
        loop, selected = True, False
        tools.drawMenu(int(menuState))
        keys = list(settings['options'].keys())
        applySettings(settings)
        while loop:
            # navigation inbetween main pages
            if menuState == 0:
                if Button.UP in charlie.buttons.pressed():
                    menuState = 5
                elif Button.DOWN in charlie.buttons.pressed():
                    menuState = 1
            elif menuState > 0 and menuState < 6:
                if Button.UP in charlie.buttons.pressed() and menuState > 1:
                    menuState -= 1
                elif Button.UP in charlie.buttons.pressed() and menuState == 1:
                    menuState = 5
                if Button.DOWN in charlie.buttons.pressed() and menuState < 5:
                    menuState += 1
                elif Button.DOWN in charlie.buttons.pressed() and menuState == 5:
                    menuState = 1
            
            # subMenus
            elif menuState == 50: #settings Menu

                if Button.UP in charlie.buttons.pressed():
                    if not selected:
                        if position > 0:
                            position -= 1
                        elif position == 0:
                            position = len(settings['options']) - 1
                    else:
                        if settings['options'][keys[position]] < settings['values']['max'][keys[position]]:
                            settings['options'][keys[position]] += 1
                        elif settings['options'][keys[position]] == settings['values']['max'][keys[position]]:
                            settings['options'][keys[position]] = settings['values']['min'][keys[position]]
                        tools.sound('assets/media/click.wav')
                        tools.drawSettings(position, settings, selected)
                if Button.DOWN in charlie.buttons.pressed():
                    if not selected:
                        if position < len(settings['options']) - 1:
                            position += 1
                        elif position == len(settings['options']) - 1:
                            position = 0
                    else:
                        if settings['options'][keys[position]] > settings['values']['min'][keys[position]]:
                            settings['options'][keys[position]] -= 1
                        elif settings['options'][keys[position]] == settings['values']['min'][keys[position]]:
                            settings['options'][keys[position]] = settings['values']['max'][keys[position]]
                        tools.sound('assets/media/click.wav')
                        tools.drawSettings(position, settings, selected)
                            


                if Button.CENTER in charlie.buttons.pressed():
                    if selected:
                        storeSettings(settings)
                        applySettings(settings)
                        
                    selected = not selected
                    oldPos += 1

                if position != oldPos:
                    tools.sound('assets/media/click.wav')
                    tools.drawSettings(position, settings, selected)
                    oldPos = position
                    time.sleep(0.07)

            # selection of pages
            if Button.RIGHT in charlie.buttons.pressed() and menuState > 0 and menuState <= 5 and not selected:
                menuState = menuState * 10
                position, oldPos = 0, 1
                oldMenuState = menuState
                tools.sound('assets/media/confirm.wav')
                time.sleep(0.08)
                tools.animate(menuState, True)
                time.sleep(0.4)

            if Button.LEFT in charlie.buttons.pressed() and menuState >= 10 and not selected:
                tools.sound('assets/media/confirm.wav')
                time.sleep(0.08)
                tools.animate(menuState, False)
                menuState = menuState / 10
                oldMenuState = menuState
                time.sleep(0.4)


            if oldMenuState != menuState:
                tools.sound('assets/media/click.wav')
                time.sleep(0.08)
                tools.drawMenu(menuState)
                oldMenuState = menuState
                time.sleep(0.3)

            if self.logger.getScreenRefreshNeeded == 1:
                self.logger.setScreenRefreshNeeded = 0
                menuState = menuState / 10

    # method for displaying the right contents of the menu on the Display
    def drawMenu(menuState, *args):
        menus = {0: 'assets/graphics/menus/mainMenu.png',
                1: 'assets/graphics/menus/programmingMainMenu.png',
                2: 'assets/graphics/menus/testingMainMenu.png',
                3: 'assets/graphics/menus/remoteMainMenu.png',
                4: 'assets/graphics/menus/competitionMainMenu.png',
                5: 'assets/graphics/menus/settingsMainMenu.png'
                }

        
        try:
            charlie.screen.draw_image(0, 0, menus[menuState], transparent = Color.RED)
        except Exception as exception:
            log.error("Could not draw menu: ", str(exception))

    # method for the settings selection menu
    def drawSettings(pos, settings, selected, *args):

        def drawOptions(value, *args):
            '''Function that draws the 5 current options on the screen'''
            i = 0
            while i <= 4:
                if value + i == pos:
                    if selected:
                        charlie.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.BLACK)
                        charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.WHITE, background_color = None) if settings['types'][keys[value + i]] == 'int' else charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.WHITE, background_color = None)
                    else:
                        charlie.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = True, color = Color.WHITE)
                        charlie.screen.draw_box(26, 29 + i * 20, 168, 46 + i * 20, r = 3, fill = False, color = Color.BLACK)
                        charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.BLACK, background_color = None) if settings['types'][keys[value + i]] == 'int' else charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.BLACK, background_color = None)
                else:
                    charlie.screen.draw_box(26, 29 + i * 20, 170, 46 + i * 20, fill = True, color = Color.WHITE)
                    charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], settings['options'][keys[value + i]]), text_color = Color.BLACK, background_color = Color.WHITE) if settings['types'][keys[value + i]] == 'int' else charlie.screen.draw_text(29, 30 + i * 20, '%s: %s' % (keys[value + i], bool(settings['options'][keys[value + i]])), text_color = Color.BLACK, background_color = Color.WHITE)
                i += 1

        keys = list(settings['options'].keys())
        charlie.screen.set_font(Font(family = 'arial', size = 13))

        # the slider bar indicator
        charlie.screen.draw_box(171, 25, 177, 127, r = 2, fill = False, color = Color.BLACK)
        charlie.screen.draw_box(172, 26, 176, 126, r = 2, fill = True, color = Color.WHITE)
        charlie.screen.draw_box(173, 27 + 102 / len(settings['options']) * pos, 175, 23 + 102 / len(settings['options']) * (pos + 1), r = 1, fill = True, color = Color.BLACK)

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

    # method for animating transitions between menus
    def animate(state, direction, *args):
        menus = {10: 'mainProgram',
                20: 'mainTest',
                30: 'mainRemote',
                40: 'mainCompetition',
                50: 'mainSettings'}

        
        if direction:
            i = 1
            try:
                while i <= 10: 
                    charlie.screen.draw_image(0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
                    i += 1
            except Exception as exception:
                log.error("Could not animate menu: ", str(exception))
                return(RobotError.Display.Animation.generalError)
    
        else:
            i = 10
            try:
                while i >= 1:
                    charlie.screen.draw_image(0, 0, 'assets/graphics/animations/%s/%s.png' % (menus[state], i), transparent = Color.RED)
                    i -= 1
            except Exception as exception:
                log.error("Could not animate menu: ", str(exception))
                return(RobotError.Display.Animation.generalError) 
