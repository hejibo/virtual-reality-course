import viz
viz.go()

#Add spotlights and remove the head light.
viz.MainView.getHeadLight().disable()
spot_light = viz.addLight()
spot_light.position( 0, 0,0, 1)
spot_light.setEuler( 180,65,180)
spot_light.setPosition(0,4.55,2.5)
spot_light.spread(45)
spot_light.spotexponent(5)
spot_light.intensity(1.5)

#Set up the viewpoint.
viz.MainView.setEuler(180,0,0)
viz.MainView.setPosition(0,1.5,6)

#Disable mouse navigation
viz.mouse(viz.OFF)

#Add the models.
tent = viz.add('art/tent.ive')
stand = viz.add('art/stand.ive')
wheel = viz.add('art/wheel.ive')
avatar = viz.add( 'vcc_male.cfg' )
knife = viz.add('art/knife.ive')

#Put the wheel in position.
wheel.setPosition([.02,1.62,.24])
wheel.setEuler([0,-20,0])

#Link the avatar to the wheel.
link = viz.link( wheel, avatar  )
#Use a pre-translation on the link to get the avatar
#in the correct position on the wheel.
link.preTrans( [0,-1,.1 ])
#Get the wheel spinning.
wheel.addAction( vizact.spin(0,0,1,90) )


#Grab a few of the avatar's bones and put them into position.
bones = [' L Thigh', ' R Thigh', ' L UpperArm', ' R UpperArm' ]
rolls = [-20,20,-40,40 ]
for i in range(len(bones)):
	bone = avatar.getBone( 'Bip01' + bones[i] )
	bone.lock()
	bone.setEuler( [0,0,rolls[i]], viz.AVATAR_LOCAL)
#Set the idlepose of the avatar to -1 so that it doesn't go to 
#animation #1 when it is idleing. 
avatar.idlepose( -1 )

#Add the balloons.
import random
balloons = []
balloon_coords =  [[0,-.75],[.75,-.75],
[-.75,-.75],[.5,0],[-.5,0],[.4,.9],
[-.4,.9], [.9,.45],[-.9,.45]]
for coord in balloon_coords:
	balloon = viz.add('art/balloon2.ive')
	R = random.random()
	G = random.random()
	B = random.random()
	balloon.color( R, G, B )
	balloon.alpha(.8)
	balloon.specular( viz.WHITE )
	balloon.shininess(128)
	#Link the balloons to the wheel. 
	link = viz.link( wheel, balloon )
	#Do pre transformations on the link
	#to put them in different places.
	link.preTrans( [coord[0],coord[1],0] )
	link.preEuler( [random.randrange(-60,60),random.randrange(100,150),0] )
	balloons.append( balloon )

#Add audio for the avatar.
cry = viz.addAudio( 'art/grunt.wav' )
#Create the actions for a wounded avatar.
avatar_hit  = vizact.parallel(  vizact.fadeTo(0,speed=1), vizact.call( cry.play ))
avatar_sequence = vizact.sequence([ avatar_hit, vizact.fadeTo(1,speed=1)], 1 )


#Create the actions for popping balloons.
popping_sound = viz.addAudio('art/pop.wav')
play_pop = vizact.call( popping_sound.play )
popping_action = vizact.sizeTo([.1,.2,.1],time=.5 )
popping = vizact.parallel( [play_pop, popping_action] )




#Add a collide mesh for the wheel, balloons and avatar.
wheel.collideMesh()
for balloon in balloons:
	balloon.collideMesh()
avatar.collideMesh()
#Grab the ground and add a collision plane.
ground = tent.getChild( 'ground' )
ground.collidePlane(0,1,0,0)
#Add a collide box for the knife.
knife.collideBox()
#Add a collide notify flag so that collisions with the knife will trigger events.
knife.enable( viz.COLLIDE_NOTIFY  )


#Name a variable for the link that 
#will be created whenever the knife
#sticks to the wheel.
knife_link = 0
#Define a function that will stick 
#the knife to something.
def stick_knife( into_what ):
	global knife_link
	#Disable the knife's physics so 
	#that the link won't compete with forces.
	knife.disable( viz.PHYSICS )
	#If the knife is linked to anything else, 
	#remove that link.
	if knife_link:
		knife_link.remove()
	#Create a new link to whatever the 
	#knife has struck.	
	knife_link = viz.grab(into_what, knife )

#This function will throw the knife when the 
#mouse is clicked.
def throw_knife():
	#Convert the current mouse position from 
	#screen coordinates to world coordinates
	line = viz.screentoworld(viz.mousepos())
	#Create a vector that points along the 
	#line pointing from the screen into the world.
	vector = viz.Vector(line.dir)
	#Set length of this vector.
	vector.setLength(20)
	#Remove the link if the knife is linked 
	#to something.
	if knife_link:
		knife_link.remove()
	#Reset the knife. This will get rid of any 
	#forces being applied to the knife.
	knife.reset()
	#Enable physics on the knife in case 
	#they've been disabled.
	knife.enable(viz.PHYSICS)
	#Move the knife into position at the 
	#beginning of our line.
	knife.setPosition( line.begin )
	#Set the orientation of the knife.
	knife.setEuler(180,90,0)
	#Set the velocity for the knife to travel
	#in (the vector we calculated above).
	knife.setVelocity( vector )
vizact.onmouseup(viz.MOUSEBUTTON_LEFT,throw_knife)

#Define a function to handle collision events. 
def onCollideBegin(e):
	#If the knife hits the avatar or the wheel, 
	#stick it to them.
	if e.obj2 == avatar:
		avatar.addAction(avatar_sequence)
		stick_knife( avatar )
	if e.obj2 == wheel:
		stick_knife( wheel )
	#If the knife hits a balloon, pop it and 
	#disable its physics
	#so it can't get hit again.
	if balloons.count( e.obj2 ):
		e.obj2.disable( viz.PHYSICS )
		e.obj2.addAction( popping )
		stick_knife( e.obj2 )
#Callback for collision events. 
viz.callback(viz.COLLIDE_BEGIN_EVENT,onCollideBegin)

#Define a function to reset the balloons.
def reset_balloons():
	for balloon in balloons:
		balloon.addAction( vizact.sizeTo([1,1,1], time=.5))
		balloon.enable( viz.PHYSICS )
vizact.onkeydown('r', reset_balloons )

#Enable the physics engine.
viz.phys.enable()



