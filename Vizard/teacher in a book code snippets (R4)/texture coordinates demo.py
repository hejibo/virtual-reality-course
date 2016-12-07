import viz
viz.go()
viz.clearcolor([.3,.3,.3])
viz.mouse( viz.OFF )
viz.MainView.setPosition(0,0,-1.5)

#Add the texture quad and the texture to put on it.
quad = viz.addTexQuad()
textures = []
files = ['foliage.jpg','pine needles.jpg' ]
for i in range(len(files)):
	texture =  viz.addTexture( 'art/' + files[i] )
	texture.wrap( viz.WRAP_S, viz.CLAMP_TO_EDGE )
	texture.wrap( viz.WRAP_T, viz.CLAMP_TO_EDGE )
	quad.texture( texture, '', i )
	textures.append( texture )

def change_wrap_mode( event,  dimension ):
	mode = event.object.getItem( event.newSel )
	for texture in textures:
		texture.wrap( eval( 'viz.WRAP_' + dimension ), eval( 'viz.' + mode ) )

matrix = vizmat.Transform()
def change_texture_matrix( textbox, dimension, kind ):
	value = eval( textbox.get() )
	if dimension == 'S':
		index = 0
	elif dimension == 'T':
		index = 1
	if kind == 'scale':
		current = matrix.getScale()
		current[ index ] = value
		matrix.setScale( current )
	elif kind == 'translation':
		current = matrix.getTrans()
		current[ index ] = value
		matrix.setTrans( current )
	quad.texmat( matrix, '', 0 )
	quad.texmat( matrix, '', 1 )

	
	
import vizmenu
menu = vizmenu.add()
menu.setAutoHide(viz.OFF)



transforms = [['scale','1'],['translation','0']]
default = [1,0]
matrix_menu = menu.add( 'texture coordinates' )
dims = ['S','T']
for transform in transforms:
	this_menu = matrix_menu.add( vizmenu.MENU, transform[0] )
	for dim in dims:
		dim_box = this_menu.add( viz.TEXTBOX, dim )
		dim_box.message( transform[1] )
		vizact.onbuttonup( dim_box, change_texture_matrix, dim_box, dim, transform[0] )

wrap_menu = menu.add( 'wrap modes' )
wrap_dims = [ 'S', 'T' ]
wrap_options = ['CLAMP_TO_EDGE', 'CLAMP_TO_BORDER', 'REPEAT', 'MIRROR']
for dim in wrap_dims:
	this_list = wrap_menu.add( viz.DROPLIST, dim + ' axis')
	this_list.addItems( wrap_options )
	vizact.onlist( this_list,change_wrap_mode, dim )

def change_border_color( event ):
	color = event.object.getItem( event.newSel )
	for texture in textures:
		texture.setBorderColor( eval('viz.' + color ) )
border_menu = menu.add( 'border color' )
colors = ['BLACK', 'GREEN', 'RED']
color_list = border_menu.add( viz.DROPLIST, 'choose' )
color_list.addItems( colors )
vizact.onlist( color_list,change_border_color )

blend_menu =  menu.add( 'blend' )


def blender( pos ):
	quad.texblend(pos ,'',1)
slider = blend_menu.add( viz.PROGRESS_BAR, 'blend to other' )
vizact.onslider( slider,blender )
quad.texblend(0,'',1 )

