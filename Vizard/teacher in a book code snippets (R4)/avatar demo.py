import viz
viz.go()



def transform_bone(amt,which):
	if which in ['x','y','z']:
		range = POS_RANGE
	elif which in ['yaw','pitch','roll']:
		range = ORI_RANGE
	new_amt = (amt-.5)*range
	bp = bone_parameters[ current_bone ]
	bp[ which ] = new_amt
	#bones[ current_bone ].setPosition( bp['x'], bp['y'], bp['z'] )
	bones[ current_bone ].setEuler( bp['yaw'], bp['pitch'], bp['roll'], viz.AVATAR_LOCAL )
	reset_euler_text()
	
def reset():
	for bone in bones.keys():
		#bone.setPosition(0,0,0, viz.AVATAR_LOCAL)
		bones[ bone ].setEuler(0,0,0, viz.AVATAR_LOCAL)
		for parameter in parameters:
			bone_parameters[ bone ][ parameter ] = 0
	reset_sliders()

def set_current_bone(e):
	global current_bone
	selection = e.newSel
	current_bone = 'Bip01' + e.object.getItem( selection )
	current_bone_text.message( current_bone )
	for list in lists:
		list.select(0)
	e.object.select( selection )
	reset_sliders()

def reset_sliders():
	for parameter in parameters:
		parameter_value = bone_parameters[ current_bone ][ parameter ]
		amt = float(parameter_value)/ORI_RANGE + .5
		sliders[ parameter ].set( amt )
	reset_euler_text()

def reset_euler_text():
	text_string = '['
	for parameter in parameters:
		text_string += str( round( bone_parameters[ current_bone ][ parameter ] ) ) + ', '
	text_string = text_string.rstrip(', ') + ']'
	euler_text.message( text_string )

#Variables.
avatar = viz.add('vcc_male.cfg')
bone_list = avatar.getBoneList()
bones = {}
parts = {' L':[], ' R':[], '':[]}
parameters = ['yaw','pitch','roll']
bone_parameters = {}
current_bone = 0
ORI_RANGE = 360
POS_RANGE = 1
for bone in bone_list:
	bone_name = bone.getName()
	bones[ bone_name ] = bone
	bone.lock()
	new_name = bone_name.lstrip( 'Bip01' )
	side = new_name[0:new_name.rfind(' ')]
	parts[ side ].append( new_name )
	bone_parameters[ bone_name ] = {}
	for parameter in parameters:
		bone_parameters[ bone_name ][ parameter ] = 0 

for value in parts.values():
	value.sort()



import vizmenu
menu = vizmenu.add()
menu.setAutoHide( viz.OFF )
bone_menu = menu.add( 'Pick a bone' )
lists = []
for item in [[' L','left'],[' R','right'],['','center']]:
	sub_menu = bone_menu.add( vizmenu.MENU, item[1] )
	list = sub_menu.add( viz.DROPLIST )
	list.addItems( ['--'] + parts[item[0]] )
	vizact.onlist( list, set_current_bone )
	lists.append( list )


import vizinfo
panel = vizinfo.add('')
current_bone_text = panel.add( viz.TEXT3D, '')
current_bone_text.alignment( viz.TEXT_RIGHT_BASE )
sliders = {}
for parameter in parameters:
	slider = panel.add( viz.SLIDER, parameter )
	slider.set(.5)
	sliders[ parameter ] = slider
	vizact.onslider( slider, transform_bone, parameter  )
euler_text = panel.add( viz.TEXT3D, '[0,0,0]' )
euler_text.alignment( viz.TEXT_RIGHT_BASE )
reset_butt = panel.add( viz.BUTTON_LABEL, 'RESET')
vizact.onbuttondown( reset_butt, reset )


#Initial settings.
current_bone = 'Bip01 Head'
current_bone_text.message( current_bone )

import debaser
def write_record():
	coordinates = {}
	for key in bones.keys():
		coordinates[ key ] = {}
		coordinates[ key ][ 'ori' ] = bones[ key ].getEuler( viz.AVATAR_LOCAL )
	debaser.dict_to_text( coordinates, 'avatar_bones.txt'  )

vizact.onexit( write_record )
import vizcam
vizcam.PivotNavigate()
n = vizcam.PivotNavigate()
n.setCenter( [0,1,0] )
n.setDistance(3)
avatar.setEuler(180,0,0)
#viz.MainView.setPosition(0,1,3)


	
	
