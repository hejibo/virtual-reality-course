import viz
import math
viz.go()

#Import the pool module and instantiate a game object.
import pool
game = pool.pool_game()

#Enable physics.
viz.phys.enable()

#Place the viewpoint in position.
viz.MainView.setPosition(0,4,-1.7)
viz.MainView.setEuler(0,68,0)

########### Use joystick events to control cue.##########
#Import the vizjoy module and add one joystick.
import vizjoy
joy = vizjoy.add()

#This function will handle hat events.
def joyhat( e ):
	game.cue.setEuler( e.hat,0,0 ) 
#Place a callbacks to watch for hat events.
#These will call joyhat whenever a hat event
#occurs.
viz.callback(vizjoy.HAT_EVENT,joyhat)	

#This function will handle joystick 
#button events.
def joybutton( e ):
	#Depending upon which button is 
	#used, called one of the pool 
	#methods.
	if e.button == 7:
		game.set_up_shot()
	elif e.button == 8:
		game.shoot()
	elif e.button == 1:
		game.rack_balls()
	elif e.button == 2:
		game.set_cueball()
#Place a callbacks to watch for 
#joystick button events. These will 
#call joybutton whenever a hat event
#occurs.
viz.callback(vizjoy.BUTTONDOWN_EVENT,joybutton)


############ Use joystick sampling to control cue.##########

#This function will handle sampling joystick movement.
def joymove():
	position_threshold = .2
	#Get the joystick position.
	pos = joy.getPosition()
	#Look at the first two elements of the position array.
	for i in range(2):
		#Only set the cue if joystick movement passes a threshold.
		if abs(pos[i]) > position_threshold:
			game.cue.setPosition( [pos[0]*.01, 0, -pos[1]*.01], viz.REL_LOCAL )
vizact.ontimer(.01,joymove )

#This function will handle joystick rotations.
def joyrotate():
	orientation_threshold = .2
	#Get the joystick orientation.
	ori = joy.getRotation()
	#If the orientation is over a threshold, rotate the cue.
	if abs( ori[2] ) > orientation_threshold:
		game.cue.setEuler([ori[2],0,0], viz.REL_PARENT )
vizact.ontimer(.01,joyrotate )
