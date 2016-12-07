import viz
viz.go()

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
