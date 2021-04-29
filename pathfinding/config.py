class Conf:
    def __init__(self):
#Waypoints/roads enter
#

#Start point goes here ( [3, 2]  X,Y axis)
        self.start = [3,2] #Default Value 3,2


#===========================================#


# Obsticles
#
# List obsticles so the robot knows to avoid them. You can set the margin from your robots core to the obsticle using the 'margin' var.

        self.marginObs = 5  # Distance in centimeeters, no doubles or point valuses aloud. Default value is 5.

# Leave the obsticles in the format [X,Y,X,Y] 
# The first 2 values are one of the starting point, last two the ending point.
# Leave all the objects as an array. Make more if needed. Default value 5,10 and 10,15 as a example

        self.obs = [
            [5, 10, 10, 15],
            [30,20,20,30]
        ]

# Size of area (of mat, or area)  , and margin to border so your robot doesn't fall of the edge (Relitive to the size of your robot).

        self.area = [50,50] # Area in centmiters squared, Default value [50, 50]

        self.marginBorder = "5"
  
