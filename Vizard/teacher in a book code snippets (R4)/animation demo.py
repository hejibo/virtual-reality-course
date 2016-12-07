import viz
viz.go()

#viz.clearcolor(.5,.5,1)
hat = viz.add('tophat.3DS')
hat.setEuler([0,180,0])
hat.setPosition([0,.1,0])

#Add lighting and remove the head light.
for p in [1,-1]:
	light = viz.addLight()
	light.position( p,1,p,0 ) 
viz.MainView.getHeadLight().disable()


def reset():
	for object in objects:
		object.clearActions()
		object.setPosition([0,0,0])
		object.setScale([1,1,1])
		object.color( viz.WHITE )
		object.setEuler([0,0,0])
		object.alpha(0)
	objects[0].alpha(1)

objects = []
for object in range(4):
	object = viz.add('art/balloon.ive')
	object.specular( viz.WHITE )
	object.shininess( 128 )
	objects.append( object )


actions = [['fade to red', vizact.fade(viz.WHITE, viz.RED,2 )],
['size', vizact.sizeTo([2,2,2],speed=2)],
['go to', vizact.moveTo([.6,1.8,0],time=2)],
['spin',vizact.spin(0,0,1,-15,2)] ]
sequences = [['in parallel',vizact.parallel],
['in sequence', vizact.sequence]]
triggers = [['wait for the spacebar', vizact.waitkey(' ')],
['wait for 2 seconds', vizact.waittime(2)]]
others = [['signal other objects', 1],
['just animate this object',0]]
options = [['actions',actions, viz.CHECKBOX],
['sequence style', sequences, viz.RADIO],
['triggering event', triggers, viz.RADIO],
['signal others', others, viz.RADIO]]
radio_count = 0
current = {}

def change_current( key, kind, function, which):
	global current
	if kind == viz.RADIO:
		current[ key ] = function
	elif kind == viz.CHECKBOX:
		if current[ key ].count( function ):
			current[ key ].remove( function )
		if which == 'add':
			current[ key ].append( function )

import vizmenu
menu = vizmenu.add()
menu.setAutoHide( viz.OFF )
for option in options:
	radio_count += 1
	option_menu = menu.add( option[0] )
	current[ option[0] ] = []
	for variable in option[1]:
		if option[2] == viz.CHECKBOX:
			b = option_menu.add( viz.CHECKBOX, variable[0] )
		elif option[2] == viz.RADIO:
			b = option_menu.add( viz.RADIO, radio_count, variable[0] )
			b.set( viz.UP )
		vizact.onbuttondown( b, change_current, option[0] , option[2], variable[1], 'add' )
		vizact.onbuttonup( b, change_current, option[0], option[2], variable[1], 'remove' )

def animate():
	reset()
	error_text.visible( viz.OFF )
	try:
		if current[ 'triggering event' ]:
			objects[0].addAction( current[ 'triggering event' ] )
		objects[0].addAction( current[ 'sequence style']( current[ 'actions' ] ) )
		
		if current[ 'signal others' ]:
			print 'hello'
			signal = vizact.signal()
			objects[0].addAction( vizact.sendsignal( signal ) )
			for object in objects[1:]:
				object.addAction( vizact.waitsignal( signal ) )
				object.addAction( vizact.fade(0,1,.3) )
				object.addAction( current[ 'sequence style' ]( current[ 'actions' ]) )
				signal = vizact.signal()
				object.addAction( vizact.sendsignal( signal ) )
	except:
		error_text.visible( viz.ON )
x = .25
for label in ['animate', 'reset']:
	button = viz.addButtonLabel( label.upper() )
	button.setPosition( x, .1 )
	x += .5
	vizact.onbuttondown( button, eval( label ) )
	

error_text = viz.addText( 'Pick actions and a sequence style from the menus above and then try again.', viz.SCREEN )
error_text.visible( viz.OFF )
error_text.scale( .3,.3,.3)
error_text.setPosition( .08,.03 )

viz.MainView.setPosition(0,.7,-2.5)
viz.mouse( viz.OFF )

reset()