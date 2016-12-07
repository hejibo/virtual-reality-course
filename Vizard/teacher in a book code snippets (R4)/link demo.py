import viz

viz.go()


source = viz.add('wheelbarrow.ive')
destination = viz.add('soccerball.ive')


link = viz.link( source, destination )

import vizmenu
menu = vizmenu.add()

def change_pos( pos, node_name, dim ):
	node = eval( node_name )
	current = node.getPosition()
	current[dim] = -.5 + pos
	node.setPosition(current, viz.ABS_GLOBAL )

def change_ori(  pos, node_name, dim):
	node = eval( node_name )
	current = node.getEuler()
	current[dim] = pos*180
	node.setEuler(current, viz.ABS_GLOBAL )

def change_scale( pos, node_name, dim ):
	node = eval( node_name )
	current = node.getScale()
	current[dim] = .5 + pos
	node.setScale(current)

pos_words = ['x','y','z']
ori_words = ['yaw', 'pitch', 'roll']

for thing in ['source', 'destination' ]:
	thing_menu = menu.add(thing + ' transform')
	thing_ori_menu = thing_menu.add(vizmenu.MENU, 'orientation')
	thing_pos_menu = thing_menu.add(vizmenu.MENU,'position')
	thing_scale_menu = thing_menu.add(vizmenu.MENU,'scale')
	for i in range(3):
		ori_slider = thing_ori_menu.add( viz.PROGRESS_BAR, ori_words[ i ] )
		ori_slider.set( .5 )
		vizact.onslider( ori_slider, change_ori, thing, i )
		
		pos_slider = thing_pos_menu.add( viz.PROGRESS_BAR, pos_words[ i ])
		pos_slider.set( .5 )
		vizact.onslider( pos_slider, change_pos, thing, i )
		
		scale_slider = thing_scale_menu.add( viz.PROGRESS_BAR, pos_words[ i ])
		scale_slider.set( .5 )
		vizact.onslider( scale_slider, change_scale, thing, i )

mask_flags = [ 'viz.LINK_POS | viz.LINK_ORI', 'viz.LINK_POS', 'viz.LINK_ORI', 'viz.LINK_SCALE', 'viz.LINK_ALL' ]
def change_mask( e ):
	print e.newSel
	print mask_options.getItem(  e.newSel )
	link.setMask( eval( mask_options.getItem(  e.newSel ) ) )

link_menu = menu.add( 'link' )
mask_menu = link_menu.add( vizmenu.MENU, 'mask' )
mask_options = mask_menu.add( viz.DROPLIST )
mask_options.addItems( mask_flags )
vizact.onlist( mask_options, change_mask )


def link_transform( info, transform ):
	if info.key == viz.KEY_RETURN:
		content = info.newText
		print  'link.' + transform + '(' + content + ')'
		try:
			eval( 'link.' + transform + '(' + content + ')' )
		except:
			info.object.message( 'Enter an array' )

transform_textboxes = []
for thing in ['setOffset', 'preTrans', 'preEuler', 'postTrans', 'postEuler' ]:
	text_box = link_menu.add( viz.TEXTBOX, thing )
	vizact.ontextbox( text_box, link_transform, thing )
	transform_textboxes.append( text_box )

def reset_all():
	link.reset( viz.RESET_OPERATORS )
	for text_box in transform_textboxes[1:]:
		text_box.message('')

reset_button = link_menu.add( viz.BUTTON, 'reset' )
vizact.onbuttondown( reset_button, reset_all )


viz.MainView.setPosition( [0,.6,-3.75] )
viz.mouse( viz.OFF )


	
