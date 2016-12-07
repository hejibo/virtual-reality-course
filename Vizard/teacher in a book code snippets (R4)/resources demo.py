import viz
import math
viz.go()  

#Import the pool module and instantiate a game object.
import pool
game = pool.pool_game()

USING_JOYSTICK = True

#Remove the cue.
game.cue.remove()

if USING_JOYSTICK:
	#Import your joystick navigator.
	import joystick_navigator

#Link the cueball to the view.
link = viz.link( viz.MainView, game.cueball )
#Perform a pre transformation on the link in order
#to put the head in front of, and slightly below, the viewpoint.
link.preTrans( [0,-.059,.2] )

#Make the cueball transparent so we can see through it.
#game.cueball.alpha(.2)

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
	if game.balls.count( e.obj1 ): #If one of the balls hits,
		#Play a sound at the node.
		s = e.obj1.playsound( 'art/pool ball sound.wav' )
		#Set the min and max distances for the sound.
		s.minmax(0,.2)
	if e.obj2 == game.cueball: #If the object that gets hit 
		#is the cueball, then schedule the force_task to 
		#apply a force to the joystick.
		if USING_JOYSTICK:
			viztask.schedule( force_task() )
		else:
			pass
viz.callback(viz.COLLIDE_BEGIN_EVENT, collision )



#Make a game out of it.######
import viztask

#Add some text to communicate with user.
text = viz.addText( '', viz.SCREEN )
text.setPosition(.5,.5)
text.setScale( 1,1 )
text.alignment( viz.TEXT_CENTER_BASE )

#Add a condition to watch for all the balls to be off the table.
class wait_for_8( viztask.Condition ):
	def __init__( self ):
		#Set the limit for the balls to go below.
		self.limit = .90
	def update( self ):
	#This function will run about every frame, returning True or False
	#to the yield statement.
		if game.balls[10].getPosition()[1] < self.limit:
			return True
		return False

def ref():
	if game.balls[10].getPosition()[1]< .90:
		return 'won'
	else:
		return 'lost'


def game_task():
	while True:
		yield viztask.waitKeyDown( 'g' )
		#Set up the balls.
		game.set_cueball
		game.rack_balls()
		
		#Set the viewpoint in a good place.
		viz.MainView.setPosition( game.cueball.getPosition() )
		viz.MainView.setEuler(-90,0,0, viz.BODY_ORI)
		viz.mouse.setOverride( viz.ON )
		
		#Let the user know they are about to begin.
		text.message( 'Get ready!' )
		yield viztask.waitTime( 3 )
		text.message( 'GO!' )
		viz.mouse.setOverride( viz.OFF )
		yield viztask.waitTime( 1 )
		text.message( ' ')
		
		#Wait for the 8 ball to go down. 
		yield viztask.waitAny( [wait_for_8(), viztask.waitTime( 30 )] )
		text.message( 'Game over, you ' + ref() )

#Schedule the task.
viztask.schedule( game_task() )

