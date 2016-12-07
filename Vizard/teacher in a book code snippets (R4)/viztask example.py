import viz
import viztask
viz.go()

#task
#subtask
#other task
#event within task


viz.add( 'court.ive' )

#Add a matrix of dots.
dots = []
for x in range(-2,3):
	for z in range(1,4):
		dot = viz.add('white_ball.wrl')
		dot.collideSphere()
		dot.disable( viz.DYNAMICS )
		dot.setPosition( x, 1.8, z )
		dots.append( dot )

#Add a text field.
text = viz.addText('', viz.SCREEN )
text.setPosition( .5,.5 )
text.setScale( .5,.5)
text.alignment( viz.TEXT_CENTER_BASE )
text.alpha( 0 )

#Set up a scoreboard.


#Node for our head.
head = viz.add('white_ball.wrl')
head.collideSphere()
head.enable( viz.COLLIDE_NOTIFY )
head.disable( viz.RENDERING )
head.disable( viz.DEPTH_WRITE )
viz.link( viz.MainView, head )

def game_task():
	while True:
		collision_data = viz.Data()
		yield viztask.waitEvent( viz.COLLIDE_BEGIN_EVENT, collision_data )
		collision_data.data[0].obj2.visible( viz.OFF )
viz.phys.enable()


def overview_task():
	#Get ready screen.
	text.alpha(1)
	text.message( 'Press s to begin' )
	#Wait for player to hit 's' key.
	yield viztask.waitKeyDown( 's' )
	#Provide the game instructions in a subtask.
	yield game_instructions() 
	#Begin the game.
	game = viztask.schedule( game_task() )
	#Wait for time to pass.
	yield viztask.waitTime( 10 )
	#End game.
	game.kill()
	text.alpha( 1 )
	text.message( 'GAME OVER' )

viztask.schedule( overview_task() )
#timer event
#keyboard event
#collision event
#action begin event
#button event


