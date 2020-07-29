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

  