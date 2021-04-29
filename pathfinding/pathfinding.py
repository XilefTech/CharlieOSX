import config as configDoc

config = configDoc.Conf()


# Configration check sequence

print("Current Configuration Settings")
print("+---------------------------------------")
print("|       Name        |        Value      ")
print("+-------------------+-------------------")
print("|      Start        |       " + str(config.start))
print("+-------------------+-------------------")
print("|      Obsticle     |        " + str(config.marginObs))
print("|       Margin      |")
print("+-------------------+-------------------")
print("|       OBSTACLE AVOIDENCE NODES        ")
print("|        Node 1     |       Node 2 ")
print("|---------------------------------------")

for i in config.obs:
    print("|       "+str(i[0])+","+str(i[1])+"        |        "+str(i[2])+","+str(i[3]))
    print("+-------------------+-------------------")

print("|       Area        |        " + str(config.area))
print("+-------------------+-------------------")

print("|    Edge Margin    |        " + config.marginBorder)
print("+-------------------+-------------------")


print("")