def parseConfig(configPath):
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
        if str(exception) == '[Errno 2] ENOENT':
            print(exception)
        else:
            print(exception, type(exception), str(exception))


    for key in keys: 
        configDict[key] = values[keys.index(key)]

    return configDict
