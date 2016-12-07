import viz
import viztask
viz.go()

### Add all the resources. ###############

#Add a sky with an environment map.
env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
dome = viz.add('skydome.dlc')
dome.texture(env)

#Add a maze model.
maze = viz.add('art/maze.ive')

#Add balloons.
balloons = []
for pos in [[.2,3.4],[-3.2,6.8],[-9.8,23.4],
	[6.4,30.2],[-13.0,33.4] ]:
	balloon = viz.add('art/balloon.ive' )
	balloon.setScale( 2,2,2 )
	balloon.setPosition( pos[0],1.7,pos[1] )
	balloon.color( viz.RED )
	balloon.specular( viz.WHITE )
	balloon.shininess( 128 )
	balloons.append( balloon )
	
#Add a popping sound.
pop = viz.addAudio( 'art/pop.wav' )

#Turn on viewpoint collision and set
#its distance buffer.
viz.collision( viz.ON )
viz.collisionbuffer( .1 )

#Add a subwindow and associated it 
#with a viewpoint.
subwindow = viz.addWindow()
subview = viz.addView()
subwindow.setView( subview )
subwindow.setSize( .35,.35 )
subwindow.setPosition( .65,1)
subwindow.visible( viz.OFF )

#Link the subview to the position 
#of the main view but put it up a distance.
subview_link = viz.link( viz.MainView, subview )
subview_link.setMask( viz.LINK_POS )
subview_link.setOffset( [0,8,0] )
subview.setEuler( [0, 90, 0 ])

#Link a dart to the main view.
dart = viz.add( 'art/dart.ive' )
dart.setScale( 2,2,2)
link = viz.link( viz.MainView, dart )
link.preTrans( [0,.15,0] )

#Add text fields to a dictionary.
text_dict = {}
for kind in ['score','instructions','time' ]:
	text = viz.addText('', viz.SCREEN )
	text.setScale( .5,.5)
	text.alignment( viz.TEXT_CENTER_BASE )
	text.alpha( 1 )
	text_dict[ kind ] = text
text_dict['score'].setPosition( .1,.9 )
text_dict['instructions'].setPosition( .5,.5 )
text_dict['time'].setPosition( .1,.85 )


#Add a blank screen to the viewpoint to 
#block out everything in the beginning.
blank_screen = viz.addTexQuad( viz.SCREEN )
blank_screen.color( viz.BLACK )
blank_screen.setPosition( .5, .5 )
blank_screen.setScale( 100,100 )

######################### Tasks ############################################

def set_the_stage():
	#Put the viewpoint in the right position and freeze
	#navigation.
	viz.MainView.setPosition(0,1.8,-3)
	viz.MainView.setEuler(0,0,0)
	viz.mouse( viz.OFF )
	#Make the instructions text appear.
	text = text_dict[ 'instructions' ]
	text.alpha( 1 )
	#Put a message in that text.
	text.message( 'Press s to begin.' )
	#Wait for the s key to be hit.
	yield viztask.waitKeyDown( 's' )
	text.message( '' )

##Schedule the above task.
#viztask.schedule( set_the_stage() )

def game_instructions():
	text = text_dict[ 'instructions' ]
	text.alpha( 1 )
	sentences = ['You will get one point for each balloon that you pop.', 
	'You are racing against the clock.',
	'Get ready . . .' ]
	for sentence in sentences:
		text.alpha(0)
		text.message( sentence )
		#Add a fading action to the text and wait.
		yield viztask.addAction( text, vizact.fadeTo(1, time = 1 ))
		#Wait a second.
		yield viztask.waitTime( 1 )
		#Wait to fade out.
		yield viztask.addAction( text, vizact.fadeTo(0, time = 1 ))

def game_timer_task():
	#Grab the text field for
	#time.
	text = text_dict[ 'time' ]
	time = 0
	text.message( 'Time: 0' )
	#Loop through as long as time
	#is under a certain number of
	#seconds.
	while time < 30:
		yield viztask.waitTime( 1 )
		time += 1
		text.message( 'Time: ' + str( time ) )
	
def balloon_popping_task():
	#Grab the text field for
	#the score.
	text = text_dict[ 'score' ]
	score = 0
	text.message( 'Score: 0' )
	#Loop through as long as the score
	#is below the winning limit.
	while score <5:
		#Create a data object to accept
		#data from the event.
		data = viz.Data()
		#Yield for collision events.
		yield viztask.waitEvent( viz.COLLISION_EVENT, data )
		#From the data object, get the object
		#that the viewpoint collided with.
		intersected_object = data.data[0].object
		#If it was a balloon, pop it and
		#add a point to the score.
		if balloons.count( intersected_object ):
			pop.play()
			score += 1
			text.message( 'Score: ' + str( score ) )
			intersected_object.visible( viz.OFF )


def game():
	#Begin the game.
	#Turn on mouse navigation.
	viz.mouse( viz.ON )
	#Make the subwindow visible.
	subwindow.visible( viz.ON )
	#Get rid of the blank screen
	#that blocks the view.
	blank_screen.visible( viz.OFF )
	
	#Create two tasks for two outcomes of game.
	balloon_popping = viztask.waitTask( balloon_popping_task() )
	time_passing = viztask.waitTask( game_timer_task() )
	
	#Wait for the game to end.
	#Create a data object that 
	#we can pass to the next yield
	#statement.
	data = viz.Data()
	#Wait for the game to end one way
	#or another.
	yield viztask.waitAny( [balloon_popping, time_passing], data )
	
	#Once the game has ended, hide things.
	viz.mouse( viz.OFF )
	blank_screen.visible( viz.ON )
	subwindow.visible( viz.OFF )
	viz.MainView.reset(viz.HEAD_ORI | viz.HEAD_POS| viz.BODY_ORI)
		
	#Give different feedback depending on 
	#how the game ended.
	text = text_dict[ 'instructions' ]
	if data.condition == balloon_popping:
		text.message( 'GAME OVER, YOU WON!' )
	elif data.condition == time_passing:
		text.message( 'GAME OVER, YOU LOST.' )
	text.alpha( 1 )
	
	#Wait a moment.
	yield viztask.waitTime( 4 )


def play_again():
	#Ask a question.
	text_dict[ 'instructions' ].message( 'Want to play again (y/n)?' )
	#Create a data object to accept the 
	#event's data.
	data = viz.Data()
	#Yield to a keydown event.
	yield viztask.waitKeyDown(('n','y'),data ) 
	#If the key that was pressed
	#is 'n', quit.
	if data.key == 'n':
		viz.quit()
	#Otherwise reset the world.
	if data.key == 'y':
		for balloon in balloons:
			balloon.visible( viz.ON )
		for value in text_dict.values():
			value.alpha(0)



#Set up a task to handle the main 
#sequence of events.
def main_sequence():
	while True:
		#Set the stage for the game.
		yield set_the_stage()
			
		#Begin with instructions.
		yield game_instructions()
		
		#Play the game.
		yield game()
		
		#See if the user wants to play 
		#again.
		yield play_again()

#Schedule the main sequence task.
viztask.schedule( main_sequence() )