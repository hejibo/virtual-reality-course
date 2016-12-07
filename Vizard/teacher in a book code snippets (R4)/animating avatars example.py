import viz
viz.go()

#Add the models. 
ground = viz.add('art/sphere_ground3.ive')
male = viz.add('vcc_male.cfg')
female = viz.add('vcc_female.cfg')
female.setPosition(-1,0,1 )

#Add a sky.
env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
dome = viz.add('skydome.dlc')
dome.texture(env)

#Set the viewpoint.
viz.MainView.setPosition(0,1.8,5)
viz.MainView.setEuler(180,0,0)

#Start the avatars in an idling animation. 
#This will loop.
female.state(1)
male.state(1)

#Get a handle on the male avatar's head 
#and lock it.
bone_head = male.getBone( 'Bip01 Head' )
bone_head.lock()
def follow_target():
	#This function will rotate the male's 
	#head to face the female.
	#First get the position of the female 
	#and male.
	f_pos = female.getPosition()
	m_pos = male.getPosition()
	#Pull out their x and z.
	f_point = [f_pos[0], f_pos[2]]
	m_point = [m_pos[0], m_pos[2]]
	#Get the angle between those.
	angle = vizmat.AngleToPoint( m_point, f_point ) 
	#Rotate the male's head that angle 
	#(as long as it's in the natural 
	#range.
	if angle < 90 and angle >-90:
		bone_head.setEuler( angle,0,0, viz.AVATAR_LOCAL )
vizact.ontimer(.01,follow_target )

#Blend in the male avatar dancing 
vizact.onkeydown( 'd', male.blend, 5,1,5 )
#Blend out the male's idle animation.
vizact.onkeydown( 's', male.blend, 1,0,5 )

#Put the female avatar into position and 
#define some walking actions for her.
female.setPosition(5,0,4)
walk_left = vizact.walkTo([-2,0,1])
walk_right = vizact.walkTo([3,0,1])
walking_sequence = vizact.sequence( [walk_left, walk_right], viz.FOREVER )
female.addAction( walking_sequence )



#Define some physics components.	
male.collideMesh()
ground.collideMesh()
#Add a ball whose collisions we will watch for.
ball = viz.add('soccerball.IVE')
ball.collideSphere()
ball.enable( viz.COLLIDE_NOTIFY )
ball.setPosition(100,100,100)

#When the ball hits the male avatar, have him look around and then stand still.
#Also, clear the female avatar's actions and have her clap.
def onCollideBegin(e):
	if e.obj2 == male:
		male.execute(9, freeze = True )
		female.clearActions()
		female.execute(4)
viz.callback(viz.COLLIDE_BEGIN_EVENT,onCollideBegin)

#Shoot the ball with a keypress.
def shoot_ball():
	ball.reset()
	ball.setPosition( [1,2,5])
	ball.setVelocity([-2.8,.8,-15])
vizact.onkeydown(' ',shoot_ball )

#Reset the avatars to 
def reset():
	male.stopAction(16)
	male.state(1)
	female.addAction( walking_sequence )
vizact.onkeydown( 'r', reset )

#Enable the physics engine.
viz.phys.enable()



#head = viz.addFace( 'morph_head.vzf' ) 
#male.setFace( head )
#def smile():
#	head.addAction( vizact.morph(0,1,1))
#	head.addAction( vizact.waittime( 1 ))
#	head.addAction( vizact.morph(0,0,1) )
#vizact.onkeydown( 's', smile)


#import viztask
#def scene():
#	yield viztask.addAction( female, walk_left )
#	dance()
#	yield viztask.waitTime(2)
#	yield viztask.addAction( female, sneak_away )
#vizact.onkeydown( 't', viztask.schedule, scene() )

#sneak_away = vizact.parallel( vizact.animation(12), vizact.move(-.20,0,0,2) )