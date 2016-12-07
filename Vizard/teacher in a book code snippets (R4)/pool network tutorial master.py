import viz
viz.go()

#Import the pool module and instantiate a game object.
import pool
game = pool.pool_game()

#Remove the cue.
game.cue.remove()

#Use the viz module to enable physics.
viz.phys.enable()

#Set the viewpoint in a good place.
viz.MainView.setPosition( 0,5,0 )
viz.MainView.setEuler(0,90,0)


#Name the client computers
CLIENT1 = 'WARRIOR'
CLIENT2 = 'CALEDONIA'
clients = [CLIENT1, CLIENT2 ]

#Get cueballs for each client.
cueballs = {}
cueballs[ CLIENT1 ] = game.cueball
cueballs[ CLIENT2 ] = pool.pool_ball( 0 )

#Set up a dictionary of networks with 
#an entry for each computer.
nets = {}
nets[ CLIENT1 ] = viz.addNetwork( CLIENT1 )
nets[ CLIENT2 ] = viz.addNetwork( CLIENT2 )

def ball_info():
	#Gather the orientation and positions of all the
	#non-cueballs.
	array = []
	for ball in game.balls:
		this_ball = []
		this_ball.append( ball.getEuler() )
		this_ball.append( ball.getPosition() )
		array.append( this_ball )
	return array

def send_box():
	#Send the data to the two clients.
	#We send them the positions and 
	#orientations of all the non-cueballs 
	#along with the position and orientation 
	#of the other client's cueball.
	b = ball_info()
	nets[ CLIENT1 ].send( balls_data = b, cue_pos = cueballs[ CLIENT2 ].getPosition() )
	nets[ CLIENT2 ].send( balls_data = b, cue_pos = cueballs[ CLIENT1 ].getPosition() )
#Send the data as frequently as possible.
vizact.ontimer(0, send_box )


def onNetwork(e):
	#This function will handle network events.
	if clients.count( e.sender ):
		print e.sender
		#If the data are from a known sender, use it
		#to translate and orient the sender's cueball.
		cueballs[ e.sender ].setPosition( e.cue_data )
#Callback for network events.
viz.callback(viz.NETWORK_EVENT,onNetwork) 

