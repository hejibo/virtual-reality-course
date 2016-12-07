import viz
import random
import viztask
viz.go()

viz.MainView.setPosition(0,1.2,5.9 )
viz.MainView.setEuler(180,0,0)
#Add a sky.
env = viz.add(viz.ENVIRONMENT_MAP,'sky.jpg')
dome = viz.add('skydome.dlc')
dome.texture(env)

ground = viz.add( 'art/sphere_ground3.ive')
ground.collidePlane( 0,1,0,0 )

import vizmenu
menu = vizmenu.add()
menu.setAutoHide( viz.OFF )
targets = {}
def change_target():
	current_target = targets[ target_list.getItem( target_list.getSelection() ) ]
	
	#Make the target visible.
	if current_target.getVisible() == False:
		for target in targets.keys():
			targets[target].visible( viz.OFF )
		current_target.visible( viz.ON )
		current_target.setPosition([0,0,0])
		current_target.setEuler( [0,0,0] )
	
	#Get the right shape.
	current_shape = shape_list.getItem( shape_list.getSelection() )
	current_target.collideNone()
	eval( 'current_target.collide' + current_shape + '()' )
	
	
	#Set the parameters.
	if current_target.getCollideShapes():
		current_shape = current_target.getCollideShapes()[0]
		for parameter in parameter_options.keys():
			value = parameter_options[ parameter ].get()
			if value.isdigit():
				eval( 'current_shape.set' + parameter + '(' + value + ')' )
	


target_menu = menu.add('target model options')
target_list = target_menu.add( viz.DROPLIST, 'target' )
for filename in ['barrel.ive', 'vcc_male.cfg', 'tube.ive']:
	targets[ filename] = viz.add('art/' + filename  )
	targets[ filename].visible( viz.OFF )
	target_list.addItem( filename )
vizact.onbuttonup( target_list, change_target )

shape_list = target_menu.add( viz.DROPLIST, 'collision shape' )
collide_shapes = ['Box', 'Sphere', 'Mesh', 'Capsule', 'None']
for shape in collide_shapes:
	shape_list.addItem( shape )
vizact.onbuttonup( shape_list, change_target )

#Set up parameter menus for the 
parameter_menu = target_menu.add( vizmenu.MENU, 'parameters' ) 
parameters = ['Bounce', 'Density', 'Friction', 'Hardness']
parameter_options = {}
for parameter in parameters :
	parameter_options[ parameter ] = parameter_menu.add( viz.TEXTBOX,  parameter )
	vizact.onbuttonup( parameter_options[ parameter ], change_target )




def change_droppers():
	current_dropper = dropper_list.getItem( dropper_list.getSelection() ) 
	print current_dropper
	#Set the parameters.
	current_parameters = []
	for parameter in drop_parameter_options.keys():
		value = drop_parameter_options[ parameter ].get()
		if value.isdigit():
			current_parameters.append(  '.set' + parameter + '(' + value + ')' )

	#Make the dropper visible.
	#reset( current_dropper, current_parameters )
	for key in droppers.keys():
		objects = droppers[ key ]
		for i in range(GRID_WIDTH):
			for j in range(GRID_WIDTH):
				#print key, shape
				if key == current_dropper:
					objects[i][j].visible( viz.ON )
				else:
					objects[i][j].visible( viz.OFF )
				if current_parameters:
					for function in current_parameters:
						eval( str(objects[i][j])+'.getCollideShapes()[0]' + function )


def reset():
	#print 'one', shape
	for key in droppers.keys():
		objects = droppers[ key ]
		for i in range(GRID_WIDTH):
			for j in range(GRID_WIDTH):
				objects[i][j].reset()
				objects[i][j].setPosition((i*SPACING)-(GRID_WIDTH*SPACING/2) + SPACING/2,3,(j*SPACING)-(GRID_WIDTH*SPACING/2) + SPACING/2)
				
		

SPACING = .2
GRID_WIDTH = 7
dropper_menu = menu.add('dropping objects options')
dropper_list = dropper_menu.add( viz.DROPLIST, 'shape' )
dropper_kinds = [['box.wrl',.1,'Box'], ['white_ball.wrl',1,'Sphere']]
droppers = {}
for kind in dropper_kinds:
	droppers[ kind[2] ] = []
	dropper_list.addItem( kind[2] )
	for i in range(GRID_WIDTH):
		droppers[ kind[2] ].append( [] )
		for j in range(GRID_WIDTH):
			object = viz.add(kind[0])
			object.color( random.random(), random.random(), random.random() )
			if kind[2] == 'Sphere':
				object.specular( viz.WHITE )
				object.shininess(128 )
			object.scale(kind[1],kind[1],kind[1])
			eval('object.collide' + kind[2] + '()' )
			droppers[ kind[2] ][i].append( object )
vizact.onbuttonup( dropper_list, change_droppers )

#Set up parameter menus for the dropppers
parameter_menu = dropper_menu.add( vizmenu.MENU, 'parameters' ) 
parameters = ['Bounce', 'Density', 'Friction', 'Hardness']
drop_parameter_options = {}
for parameter in parameters :
	drop_parameter_options[ parameter ] = parameter_menu.add( viz.TEXTBOX,  parameter )
	vizact.onbuttonup( drop_parameter_options[ parameter ], change_droppers )



enable_menu = menu.add('reset')
reset_button = enable_menu.add( viz.BUTTON, 'reset dropping objects' )
vizact.onbuttondown( reset_button, reset )

reset()
change_droppers()
change_target()
viz.phys.enable()



