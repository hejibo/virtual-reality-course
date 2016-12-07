import viz
viz.go()


##############################################
#
##Add a model.
#balloon = viz.add( 'art/balloon.ive' )
##Set the position of the balloon.
#balloon.setPosition( 0, 1.8, 1  )
##
#
#
################################

#Add an empty array for the balloons.
balloons = []

#Use a loop to add 3 balloons to the world.
for i in [-1,0,1]:
	#Add a model.
	balloon = viz.add( 'art/balloon.ive' )
	#Set the position of the balloon.
	balloon.setPosition( i, 1.8, 3  )
	
	#Append the balloon to our array.
	balloons.append( balloon )
#	
###################################################

#Change each balloon's color.
balloons[ 0 ].color( viz.GREEN )
balloons[ 1 ].color( viz.RED )
balloons[ 2 ].color( viz.BLUE )
#
#
############################################
#Define a function.
def inflate( who ):
	#Define the inflating action.
	inflate_animation = vizact.size(2,2,2)
	#Add the action to the node.
	who.addAction( inflate_animation )
	
#Call our function and pass it a balloon.
inflate( balloons[1] )
#	
	

