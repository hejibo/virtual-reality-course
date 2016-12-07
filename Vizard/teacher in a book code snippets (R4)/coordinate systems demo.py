import viz
import random
viz.go()


#Create a reset function.
def reset():
	for key in d_dict.keys():
		p_dict[ key ] = d_dict[key][ 'argument' ]
		l_dict[ key ] = d_dict[key][ 'label' ]
		d_dict[key][ 'button' ].set( viz.DOWN )
			
#Function for getting the current mode.
def get_mode():
	return  eval( 'viz.' + p_dict[ 'relative or absolute' ] + '_' + p_dict[ 'coordinate system' ] )

#Write out a numeric array as a string.
def write_array( array ):
	string = '[ ' 
	for num in array:
		string += str( round( num, 2 ) ) + ', '
	string = string[0:-2]
	string += ']'
	return string
	
#Change the texts at the bottom of the screen.
def change_texts():
	get_functions = [child.getEuler, child.getPosition]
	kinds = ['orientation', 'position' ]
	for i in range( 2 ):
		string = 'child ' + kinds[ i ] + ': '
		for cs in ['GLOBAL', 'PARENT', 'LOCAL']:
			string += cs + ' '
			string += write_array( get_functions[i]( eval( 'viz.ABS_' + cs ) ) )
			string += '   '
		texts[ i ].message( string )
	status_string = 'Transforming the ' + l_dict[ 'object'] +' '+  l_dict['relative or absolute'] + 'ly along or about the ' + l_dict[ 'axis' ] + '-axis in the ' + l_dict['coordinate system'] + ' coordinate system.'
	texts[ 2 ].message( status_string )

#Change the current
def change_dicts( property, parameter, label ):
	global p_dict, l_dict
	p_dict[ property ] = parameter
	l_dict[ property ] = label
	if property == 'show schematic':
		change_visibility()
	
def change_visibility():
	alphas.reverse()
	for arrow in arrows:
		arrow.alpha( alphas[0] )
	for object in [parent, child, ground, dome]:
		object.alpha( alphas[1] )

#Animate the transformation.
def animate_actions( kind ):
	object = p_dict[ 'object' ]
	axis = p_dict[ 'axis' ]
	coord = p_dict[ 'coordinate system' ]
	object_name = l_dict[ 'object' ]
	direction = eval(p_dict[ 'direction' ] + '1' )
		
	#Create a signal for the arrow to use to signal the object.
	go_signal = vizact.signal()
	
	#Set up the arrow animations.
	arrow_actions = [ vizact.fadeTo( ACTIVE_ALPHA, begin=alphas[0], time=.1 ),vizact.sendsignal( go_signal ), vizact.fadeTo( alphas[0], begin=ACTIVE_ALPHA, time=.1 ) ]
	#arrows
	arrow_dict[object_name][coord].sub_arrows[axis].addAction( vizact.sequence( arrow_actions,1) )

	#Set up the object animations.
	where = [0,0,0]	
	object_actions = [vizact.waitsignal( go_signal )]
	if kind == 'TRANSLATE':
		where[axis] = POSITION_FACTOR * direction
		object_actions +=  [ vizact.call( object.setPosition( where[0], where[1], where[2],get_mode()))]
	elif kind == 'ROTATE':
		where[axis] = EULER_FACTOR * direction
		object_actions += [ vizact.call( object.setEuler( where[1],where[0], where[2],get_mode()))]
	elif kind == 'SCALE':
		where = [1,1,1]
		where[axis] = 1 + direction*SCALE_FACTOR
		object_actions += [ vizact.call( object.setScale( where[0],where[1], where[2],get_mode()))]
	elif kind == 'RESET':
		for item in [parent, child]:
			item.setScale([1,1,1])
			item.setEuler([0,0,0])
			item.setPosition([0,0,0])
		child.setPosition(  [ 0.0 , 7.75 , 0.0 ] )
	elif kind == 'SCRAMBLE':
		for item in [parent, child]:
			for transform in ['Scale','Euler', 'Position']:
				random_factors = []
				standard_factor = eval(transform.upper()+ '_FACTOR')
				for i in range(3):
					random_factor = random.randint(2,4)*standard_factor*random.choice([-1,1]) 
					if transform == 'Scale':
						random_factor = random_factor + 1
					#random_factors.append( random.randint(4,8)*standard_factor*random.choice([-1,1]) )
					random_factors.append( random_factor )
				function = eval('item.set' + transform)
				function( random_factors )
		
	object.addAction( vizact.sequence( object_actions, 1) )
	change_texts()	



#Add a sky.
env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
dome = viz.add('skydome.dlc')
dome.texture(env)


#Add the camera handler.
import vizcam
n = vizcam.PivotNavigate()
n.setCenter( [0,7,0] )
n.setDistance(22)
viz.MainView.setEuler(180,5,0)
viz.MainView.setPosition(0,6,19)

#Add the lighting. 
viz.MainView.getHeadLight().disable()
l = viz.addLight()
l.position(1,1,1,0)
l2 = viz.addLight()
l2.position(0,0,1,0)


#Add the models and set their properties..
POSITION_FACTOR = .2
EULER_FACTOR = 5
SCALE_FACTOR = .1
VISIBLE_ALPHA = 1
HIDDEN_ALPHA = 0
#waiting_alpha = .1
alphas = [ HIDDEN_ALPHA, VISIBLE_ALPHA ]
ACTIVE_ALPHA = 1
parent = viz.add('art/tower.ive')
child = parent.add( 'art/turbine.ive')
child.setPosition(  [ 0.0 , 7.75 , 0.0 ] )
ground = viz.add('art/sphere_ground.ive')
arrows = []
for item in [ground, parent, child]:
	arrow = viz.add('art/arrows.ive')
	arrow.alpha( alphas[0] )
	arrow.sub_arrows = []
	for direction in ['x','y','z']:
		arrow.sub_arrows.append( arrow.getChild( direction + ' arrow' ) )
	arrow.parent( item )
	#viz.link( item, arrow )
	arrows.append( arrow )
arrow_dict = {'child':{'LOCAL':arrows[2],'PARENT':arrows[1], 'GLOBAL':arrows[0]},
'parent':{'LOCAL':arrows[1],'PARENT':arrows[0], 'GLOBAL':arrows[0]}}


#Add a menu and the contents therein to use to switch properties.
import vizmenu
menu = vizmenu.add()
menu.setAlignment( vizmenu.LEFT)
objects = [['child',child], ['parent',parent]]
coord = [ 'GLOBAL', 'PARENT', 'LOCAL']
rel = [  ['relative', 'REL'],['absolute', 'ABS'] ]
axes = [ ['x',0],['y',1],['z',2]]
directions = ['-','+']

see_arrows = [ 'show','hide' ]
properties =  [['object', objects],
['coordinate system',coord],
['relative or absolute', rel],
['axis', axes],
['direction',directions],
['show schematic', see_arrows]]

#Add dictionaries for the current settings.
p_dict = {}
l_dict = {}
d_dict = {}
button_set = -1

#Set up the menus.
for j in range(len(properties)):
	new_menu = menu.add( properties[ j ][0] )
	button_set += 1
	p_dict[ properties[ j ][ 0 ]] =  properties[ j ][ 1 ][ 0 ]
	for variable in properties[j][1]:
		if type( variable ) == type([]):
			label = variable[0]
			argument = variable[1]
		else:
			label = str(variable)
			argument = variable
		b = new_menu.add( viz.RADIO,  button_set , label ,0 )
		b.set( viz.DOWN )
		vizact.onbuttondown( b, change_dicts, properties[j][0], argument, label ) 
		vizact.onbuttondown( b, change_texts ) 
		#Create the initial settings.
		d_dict[ properties[j][0] ] = {}
		d_dict[ properties[j][0] ][ 'argument' ] = argument
		d_dict[ properties[j][0] ][ 'label' ] = label
		d_dict[ properties[j][0] ][ 'button' ] = b
		p_dict[ properties[j][0] ] = argument
		l_dict[ properties[j][0] ] = label


#Add a couple sentences at the bottom of the screen that tell the user what's current.
texts = []
for i in range(3):
	text = viz.addText( 't ', viz.SCREEN )
	text.scale(.30,.30,.30)
	text.translate(.01,i*.03+ .015)
	texts.append( text )
#Add a sentence at the top of the screen to describe current transformations.
texts[2].translate(.01,.965)
texts[2].color( viz.BLACK )

change_texts()	


#Create the buttons that will cue transformations.
d = .1
for transformation in ['ROTATE', 'TRANSLATE','SCALE', 'SCRAMBLE', 'RESET']:
	button = viz.addButtonLabel( transformation )
	button.translate( .0+ d, .1)
	d += .2
	vizact.onbuttondown( button, animate_actions, transformation )
	
	


