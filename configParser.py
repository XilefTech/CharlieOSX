'''
This file is just to offload some code and make it more organized.
The only method in this file is parseConfig()
'''


def parseConfig(configPath, logger):
    '''
        Loads the data from a config file based on my somewhat own syntax.

        Args:
            configPath (str): the path to the config file

        Returns:
            dict: The config from the file as a dict
    '''
    self = 'ConfigParser'
    logger.info(self, 'Started config parsing')
    keys, values = [], []
    tempArr = []
    configDict = {}
    arrMode = 0
    try:
        with open(configPath, 'r') as f:
            for line in f:
                l = line.rstrip()
                if l == '}':
                    arrMode = 0
                    values.append(tempArr)
                    tempArr = []

                elif arrMode == 1 and l.find('#') == -1 and l != '':
                    tempArr.append(l[l.find('-') + 2:])

                # normal entry
                elif l.find('#') == -1 and l != '' and l.find('{') == -1:
                    keys.append(l[:l.find(':')])
                    value = l[l.find(':') + 2:]

                    if value.find('[') != -1 and value.find(']') != -1:
                        # cut off first set of brackets []
                        value = value[1:len(value) - 1]
                        array = value.split(', ')
                        array = [] if array == [''] else array  # delete string in array if empty
                        for index, x in enumerate(array):
                            if x.find('[') != -1 and x.find(']') != -1:  # look for nested array
                                # cut off first set of brackets []
                                x = x[1:len(x) - 1]
                                arr = x.split(', ')
                                # convert ints to ints from str
                                for idx, y in enumerate(array):
                                    try:
                                        arr[index] = int(y)
                                    except:
                                        pass

                            try:
                                array[index] = int(x)
                            except:
                                pass
                        values.append(array)
                    else:
                        values.append(value)

                elif l.find('#') == -1 and l != '':
                    keys.append(l[:l.find(':')])
                    arrMode = 1
    except Exception as exception:
        logger.error(self, 'Error while Parsing config:', exception)

    for key in keys:
        try:
            element = int(values[keys.index(key)])
        except:
            try:
                element = float(values[keys.index(key)])
            except:
                if values[keys.index(key)] == 'True':
                    element = True
                elif values[keys.index(key)] == 'False':
                    element = False
                else:
                    element = values[keys.index(key)]
        configDict[key] = element
    logger.info(self, 'Finished config parsing')
    return configDict
