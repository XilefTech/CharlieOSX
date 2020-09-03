'''
This file is just to offload some code and make it more organized.
The only method in this file is parseConfig()
'''
def parseConfig(configPath):
    '''
        Loads the data from a config file based on my somewhat own syntax.
        
        Args:
            configPath (str): the path to the config file

        Returns:
            dict: The config from the file as a dict
    '''
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
                elif l.find('#') == -1 and l != '' and l.find('{') == -1:
                    keys.append(l[:l.find(':')])
                    values.append(l[l.find(':') + 2:])
                elif l.find('#') == -1 and l != '':
                    keys.append(l[:l.find(':')])
                    arrMode = 1
    except Exception as exception:
        print(exception, type(exception), str(exception))

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
    return configDict
