import viz
viz.go()

#Set the clear color to grey.
viz.clearcolor([.2,.2,.2])



#Add a menu to use to switch properties.cc8
import vizmenu
menu = vizmenu.add()
menu.setAutoHide( viz.OFF )
menu.setAlignment( vizmenu.LEFT)
colors = [ 'viz.BLACK','viz.WHITE','viz.RED','viz.BLUE', 'viz.YELLOW']
shines = ['10','50','128']
properties =  [['color',colors ],['specular',colors],['shininess',shines],['emissive',colors],['ambient',colors] ]
button_set = -1
def evaluate_string( string ):
	eval( string )
for j in range(len(properties)):
	new_menu = menu.add( properties[ j ][0] )
	button_set += 1
	for variable in properties[j][1]:
		b = new_menu.add( viz.RADIO,  button_set , variable,0 )
		vizact.onbuttondown( b,evaluate_string,  'object.' + properties[j][0] + '(' + variable + ')' ) 




#Add an object.
object = viz.add('art/big_leaf.ive')
#object = viz.add('art/white_ball.wrl')
#object = viz.add('box.wrl')
object_animation = vizact.sequence( [vizact.spinto(0,0,1,30,10),vizact.spinto(0,1,0,20,10), vizact.spinto(0,0,1,-60,10) ], viz.PERPETUAL )
#object.addAction( object_animation )	

#Add a texture and add buttons to add and remove the texture.
tex = viz.addTexture( 'art/ld.bmp' )
texture_menu = menu.add( 'texture' )
button_set += 1
t_off = texture_menu.add( viz.RADIO, button_set, 'without texture', 1 )
vizact.onbuttondown( t_off, object.texture, viz.OFF )
t_on = texture_menu.add( viz.RADIO, button_set, 'with texture', 1 )
t_on.set( viz.DOWN )
vizact.onbuttondown( t_on, object.texture, tex )


#Add a light and turn off the default head light.
l = viz.addLight()
l.position(1,1,0,0)
l.intensity(1)
viz.MainView.getHeadLight().disable()


#Add a light switch and a light color changer to the menu.
light_switch = menu.add( 'light switch')
button_set += 1
l_on = light_switch.add( viz.RADIO, button_set, 'on', 1 )
vizact.onbuttondown( l_on, l.enable )
l_off = light_switch.add( viz.RADIO, button_set, 'off', 0 )
vizact.onbuttondown( l_off, l.disable )
light_color = menu.add('light color')
button_set +=1
for color in colors :
	color_button = light_color.add( viz.RADIO, button_set, color, 0 )
	vizact.onbuttondown( color_button, l.color, eval(color) )





#Set the view position and turn off mouse navigation.
#viz.MainView.setPosition([-0.7, 0.22, 1.0])
#viz.MainView.setEuler( [130, 13, -15])
#viz.mouse( viz.OFF )

import vizcam
n = vizcam.PivotNavigate()


def onKeyDown(key):
	if key == ' ':
		object.pauseActions()
	if key == 'r':
		object.resumeActions()
	else:
		viz.window.screenCapture('leaf' + str(key) + '.bmp' )
viz.callback(viz.KEYDOWN_EVENT,onKeyDown)
