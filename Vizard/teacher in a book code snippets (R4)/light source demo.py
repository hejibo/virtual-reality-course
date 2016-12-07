import viz
viz.go()

viz.clearcolor( [.2,.2,.2] )

#Disable the default headlight.
viz.MainView.getHeadLight().disable()

#Add a light.
light = viz.addLight()


#Create a grid of objects so that we
#can see the effect of lights on objects
#at different positions.
r = range(-1,4)
objects = []
for thisX in r:
	for thisY in r:
		for thisZ in r:
			object = viz.add('white_ball.wrl')
			object.scale(3,3,3)
			object.setPosition( thisX, thisY, thisZ )
			objects.append( object )
		



def change_light( kind ):
	if kind == 'spot':
		light.position( 1,1,1,1 )
		light.spread( 70 )
		light.direction( -1,0,0)
	elif kind == 'point':
		light.position( 1,1,1,1 )
		light.spread( 180 )
	elif kind == 'directional':
		light.position( 1,1,1,0 )
		light.spread( 180 )
	elif kind == 'positional':
		light.position( 1,1,1,1 )


#Add a menu to use to switch properties.
import vizmenu
menu = vizmenu.add()
menu.setAutoHide(viz.OFF)
menu.setAlignment( vizmenu.LEFT)
colors = [ ['black',viz.BLACK ],['white',viz.WHITE],['orange',viz.ORANGE],['blue',viz.BLUE],['green',viz.GREEN ]]
intensities = [0,.1,.5,1,2]
attenuations = [['no attenuation',0],['attenuate light',1]]
exponents = [1,2,5,10]

kind = ['directional','positional']
kind_pos = ['point','spot']
properties =  [['positional or directional', kind, change_light],
['spot or point',kind_pos, change_light],
['color',colors, light.color],
['intensity', intensities, light.intensity],
['attenuation', attenuations, light.quadraticattenuation],
['spot exponent', exponents, light.spotexponent ]]
button_set = -1

for j in range(len(properties)):
	new_menu = menu.add( properties[ j ][0] )
	button_set += 1
	for variable in properties[j][1]:
		if type( variable ) == type([]):
			title = variable[0]
			argument = variable[1]
		else:
			title = str(variable)
			argument = variable
		b = new_menu.add( viz.RADIO,  button_set , title,0 )
		vizact.onbuttondown( b,properties[j][2], argument ) 

#Set the pivot point to the center of the logo
#viz.MainView.pivot(1,1,1)
#Set the animation mode
#viz.MainView.gotomode( viz.PIVOT_ROTATE )
seq = []
coordinates = [[7,5,-5],[8,1,1],[7,5,7],[-5,5,7],[-7,1,1], [1,1,-7]]
for c in coordinates:
	#seq.append( vizact.call( viz.MainView.goto, c[0],c[1],c[2], 2, viz.TIME ) )
	seq.append( vizact.goto([c[0],c[1],c[2]], 2, viz.TIME,rotate_mode=viz.PIVOT_ROTATE,pivot=[1,1,1],ori_mask=viz.BODY_ORI) )
	seq.append( vizact.waittime( 3) )
#viz.MainView.addAction( vizact.sequence( seq, viz.FOREVER ) )	
viz.MainView.setPosition(0,0,-5)

change_light( 'directional' )

import vizcam
n = vizcam.PivotNavigate()
n.setCenter( [1,1,1] )
n.setDistance( 10 )
