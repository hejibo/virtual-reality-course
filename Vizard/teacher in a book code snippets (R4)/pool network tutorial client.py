import viz
viz.go()

#Import the pool module and 
#instantiate a game object.
import pool
game = pool.pool_game()

#Remove the cue.
game.cue.remove()

#Import your joystick navigator.
import joystick_navigator

#Link the cueball to the view.
link = viz.link( viz.MainView, game.cueball )
#Perform a pre transformation on 
#the link in order to put the head 
#in front of, and slightly below, 
#the viewpoint.
link.preTrans( [0,-.059,.2] )

#Make the cueball transparent so 
#we can see through it.
#game.cueball.alpha(.2)

#Set the viewpoint in a good place.
viz.MainView.setPosition( game.cueball.getPosition() )
viz.MainView.setEuler(-90,0,0, viz.BODY_ORI)

#Link the cueball to the view.
link = viz.link( viz.MainView, game.cueball )
link.preTrans( [0,-.059,.2] )


############# Add networking ####################
#Name the master computer.
MASTER = 'WARRIOR'

#Add a network for the master.
master_net = viz.addNetwork( MASTER )

#Add a cueball to represent 
#the other client.
other_cue = pool.pool_ball( 0 )


def send_box():
	#Send the position of the
	#cueball to the master.
	pos = game.cueball.getPosition()
	master_net.send( cue_data = pos )
#Send the data to the master as frequently as possible.
vizact.ontimer(0, send_box )

def onNetwork(e):
	#This function will handle network 
	#events.
	if e.sender == MASTER:
		#If the event is caused by a 
		#message from the master,
		#Take the data and animate 
		#all the non-cueballs.		
		for i in range(len( game.balls ) ):
			game.balls[ i ].setEuler( e.balls_data[ i ][ 0 ] )
			game.balls[ i ].setPosition( e.balls_data[ i ][ 1 ] )
		#and take the data about the 
		#other player's cueball to 
		#animate that cueball.
		other_cue.setPosition( e.cue_pos )
viz.callback(viz.NETWORK_EVENT,onNetwork) 

