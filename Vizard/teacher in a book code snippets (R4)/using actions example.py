import viz
viz.go()

#Add the ground and an avatar.
ground = viz.add('art/sphere_ground.ive')
avatar = viz.addAvatar( 'vcc_female.cfg' )
#Make the avatar idle.
avatar.state(1)

#Add some balloons.
balloons = []
#Import the python random module to make 
#some features of the balloon random.
import random
for i in range(-5,6):
	for j in range(1,6):
		#Add and adjust the appearance and 
		#position of several balloons.
		balloon = viz.add('art/balloon.ive')
		balloon.setPosition( i*.8,.1,j*.8 )
		R = random.random()
		G = random.random()
		B = random.random()
		balloon.color( R, G, B )
		balloon.specular( viz.WHITE )
		balloon.shininess( 128 )
		balloons.append( balloon )

#Add a sky with an environment map.
env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
dome = viz.add('skydome.dlc')
dome.texture(env)

#Add some audio files.
inflate_sound = viz.addAudio( 'art/blowballoon.wav')
deflate_sound = viz.addAudio( 'art/deflateballoon.wav')

#Add lighting and remove the head light.
for p in [1,-1]:
	light = viz.addLight()
	light.position( p,1,p,0 ) 
viz.MainView.getHeadLight().disable()

#Position the viewpoint.
viz.MainView.setPosition([0,1.2,-8.9])
viz.MainView.setEuler([0,-12,0])


#Set constants for actions.
INFLATED = [2,2,2]
DEFLATED = [.2,.2,.2]
BREATH_LENGTH = 3
DEFLATE_LENGTH = .1

#Create actions to animation the inflation of a balloon (any balloon).
grow = vizact.sizeTo( INFLATED, time=BREATH_LENGTH )
play_blowing_sound = vizact.call( inflate_sound.play )
inc_transparent = vizact.fadeTo( .7, begin=1, time=BREATH_LENGTH )
#Pull together parallel actions into single actions.
inflate = vizact.parallel( grow, play_blowing_sound, inc_transparent ) 

#Create actions for floating away.
float_away = vizact.move( vizact.randfloat(-.2,.2), 1, vizact.randfloat(-.2,.2), 8 )
float_away_forever = vizact.move( vizact.randfloat(-.2,.2), 1, vizact.randfloat(-.2,.2) )


#Create actions to animate a balloon deflating.
shrink = vizact.sizeTo( DEFLATED, time=DEFLATE_LENGTH ) 
play_def = vizact.call( deflate_sound.play ) 
dec_transparent = vizact.fadeTo( 1, begin=.7, time=DEFLATE_LENGTH )
#Pull together parallel actions into a single action for deflation.
deflate = vizact.parallel( shrink, play_def, dec_transparent )

#Create a falling action.
fall = vizact.fall( 0 )

#Create an action that will wait a random amount of time.
random_wait = vizact.waittime( vizact.randfloat(.5,7) )

#Create the lifecycle of the balloon with a sequence.
life_cycle = vizact.sequence( [random_wait, inflate, float_away, deflate, fall], 1 )

#Add the actions to our balloons.
for balloon in balloons:
	balloon.setScale( DEFLATED )
	vizact.onkeydown( ' ', balloon.addAction, life_cycle ) 


#

#
#
#
#
#
#
#
#
#
#
#
#

##Add a function that signals the avatar when the balloons take flight.
#def involve_avatar():
#	avatar_signal = vizact.signal()
#	send_avatar_signal = vizact.sendsignal( avatar_signal )
#	for balloon in balloons:
#		inflate_sequence = vizact.sequence([random_wait, inflate,send_avatar_signal, float_away_forever ],1)
#		balloon.addAction( inflate_sequence )
#	avatar.addAction( vizact.waitsignal( avatar_signal ) )	
#	avatar.addAction( vizact.animation( 3 ) ) 
#vizact.onkeydown('i', involve_avatar )
#
##Add a function that clears the balloons' actions and signals the avatar.
#def pop_balloons():
#	avatar_signal = vizact.signal()
#	send_avatar_signal = vizact.sendsignal( avatar_signal )
#	for balloon in balloons:
#		balloon.clearActions()
#		pop_sequence = vizact.sequence( [deflate, fall, send_avatar_signal] )
#		balloon.addAction( pop_sequence )
#	avatar.clearActions()
#	avatar.addAction( vizact.waitsignal( avatar_signal ) )	
#	avatar.addAction( vizact.animation( 9 ) ) 
#vizact.onkeydown( 'd', pop_balloons )
#
