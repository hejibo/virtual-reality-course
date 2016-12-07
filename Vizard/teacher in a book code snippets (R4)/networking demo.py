import viz
viz.go()



def change_net():
	global other, network
	other = tb.get()
	wb_text.message( other )
	network = viz.addNetwork( other )

def send_box():
	#Send the data to the two clients.
	#We send them the positions and orientations of all
	#the non-cueballs along with the position and orientation 
	#of the other client's cueball.
	for network in networks:
		network.send( pos = viz.MainView.getPosition(), ori = viz.MainView.getEuler(), shout = 1 )
		
def add_somebody( name ):
	global wheelbarrows, others, networks, waitings
	others.append( name )
	wheelbarrow = viz.add('wheelbarrow.ive')
	wb_text = wheelbarrow.add( viz.TEXT3D, name)
	wb_text.alignment( viz.TEXT_CENTER_BASE )
	wb_text.setScale( .1, .1, 1 )
	wb_text.setEuler( 180,0,0)
	wb_text.setPosition(0,.75,0 )
	wheelbarrows[ name ] = wheelbarrow 
	waitings.remove( name )
	networks.append( viz.addNetwork( name ) )
	

def onNetwork(e):
	try:
		if e.pos and others.count( e.sender ) == 0:
			add_somebody( e.sender )
	except:
		pass
	
	#This function will handle network events.
	if others.count( e.sender ):
		#If the data are from a known sender, use it
		#to translate and orient the sender's cueball.
		wheelbarrow.setPosition( e.pos[0], e.pos[1]- .5, e.pos[2] )
		wheelbarrow.setEuler( e.ori )


	
wheelbarrows = {}	
others = []
networks = []
waitings = []


import vizinfo
info = vizinfo.add( 'Network with: ')
tb = info.add( viz.TEXTBOX, 'other client IP' )
tb_button = info.add( viz.BUTTON, 'submit' )
vizact.onbuttondown( tb_button, change_net )

#Send the data as frequently as possible.
vizact.ontimer(0, send_box )
#Callback for network events.
viz.callback(viz.NETWORK_EVENT,onNetwork) 