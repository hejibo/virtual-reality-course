import viz
import math
viz.go( viz.ANAGLYPHIC )  #viz.go( viz.HMD | viz.STEREO ) #

#Import the pool module and instantiate a game object.
import pool
game = pool.pool_game()

#Remove the cue.
game.cue.remove()

#Import your joystick navigator.
import joystick_navigator

#Link the cueball to the view.
link = viz.link( viz.MainView, game.cueball )
#Perform a pre transformation on the link in order
#to put the head in front of, and slightly below, the viewpoint.
link.preTrans( [0,-.059,.2] )

#Make the cueball transparent so we can see through it.
game.cueball.alpha(.2)

#Set the viewpoint in a good place.
viz.MainView.setPosition( game.cueball.getPosition() )
viz.MainView.setEuler(-90,0,0, viz.BODY_ORI)

#Use the viz module to enable physics.
viz.phys.enable()


#Add ambient noise. Set it to a looping mode
#play it and set the volume with methods
#from the multimedia:av library.
ambient_noise = viz.addAudio( 'art/pool hall.wav' )
ambient_noise.loop( viz.ON )
ambient_noise.play( )
ambient_noise.volume( .5 )


#Define a task to handle the force feedback.
import viztask
def force_task():
	#Add the force to the joystick. Since we
	#already added a joystick with joystick_navigator
	#we'll use that one.
	joystick_navigator.joy.addForce(0,1)
	#Wait .2 seconds.
	yield viztask.waitTime(.2)
	#Set the joystick's force at 0.
	joystick_navigator.joy.setForce(0,0)

def collision(e):
	#If one of the balls hits,
	if game.balls.count( e.obj1 ): 
		#Play a sound at the node.
		s = e.obj1.playsound( 'art/pool ball sound.wav' )
		#Set the min and max distances 
		#for the sound.
		s.minmax(0,.2)
	#If the object that gets hit 
	if e.obj2 == game.cueball: 
		#is the cueball, then schedule the force_task to 
		#apply a force to the joystick.
		viztask.schedule( force_task() )
viz.callback(viz.COLLIDE_BEGIN_EVENT, collision )

