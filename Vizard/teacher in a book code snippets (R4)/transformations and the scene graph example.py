import viz
viz.go()



#First add a few models to the world.
ground = viz.add('art/sphere_ground3.ive')
rod = viz.add('art/rod.ive')
fish = viz.add('art/pike.ive')
barrel = viz.add('art/barrel.ive')
avatar = viz.add('vcc_male.cfg')

#Give the background a blue hue.
viz.clearcolor( [ .5, .6, 1] )

#Make the fish a child node of the rod.
fish.parent( rod )
#Position and orient the fish on the rod.
fish.setPosition( [0.06, .04, 2.28], viz.ABS_PARENT )
fish.setEuler( [0,-45,180], viz.ABS_PARENT )
fish.setScale( [1,1,1.2], viz.ABS_LOCAL )


#Now move the rod up so that it's leaning against the barrel.
rod.setEuler([ 0.0 , -50.0 , 0.0 ], viz.ABS_GLOBAL )
rod.setPosition([ -0.04 , 0.13 , -1.14 ], viz.ABS_GLOBAL)
#Move the fisherman.
avatar.setPosition(2,0,0)


#Add bees as a child node of the fisherman.
bees = avatar.add('art/bees.ive')
#Place the bees at head level for the avatar.
bees.setPosition( [0,1.8,0], viz.ABS_PARENT )

#Now add a function that will make the bees spin.
def swarm():
    bees.setEuler( [5,0,0], viz.REL_PARENT )
vizact.ontimer( .01, swarm )

#And add a function that will 
#make the avatar run.
import math
import time
avatar.state(11)
def run_around():
	newX = -math.cos(time.clock()) * 2.1
	newZ = math.sin(time.clock()) * 2.2
	avatar.setPosition([newX, 0, newZ], viz.ABS_PARENT )
	avatar.setEuler( [time.clock()/math.pi*180,0,0], viz.ABS_PARENT )
vizact.ontimer(.01, run_around )

#Place the viewpoint so we can see everything.
viz.MainView.setPosition(-7,1.5,.33)
viz.MainView.setEuler(90,0,0)
