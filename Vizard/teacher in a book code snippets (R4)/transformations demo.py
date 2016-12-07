import viz

viz.go()
object = viz.add('art/head coordinates.ive')
coord = viz.add('art/axes.ive')
axes = []
WAITING_ALPHA = .5
ACTIVE_ALPHA = 1
for direction in ['x','y','z']:
	axes.append( coord.getChild( direction + ' arrow' ) )
coord.alpha( WAITING_ALPHA )


#Add the camera handler.
import vizcam
n = vizcam.PivotNavigate()
viz.MainView.setEuler(180,0,0)
n.setCenter( [0,0,0] )
n.setDistance( 1 )


#Animate the transformation.
def animate_actions( kind, axis ):
	#Create a signal for the arrow to use to signal the object.
	go_signal = vizact.signal()
	
	#Set up the arrow animations.
	arrow_actions = [ vizact.fadeTo( WAITING_ALPHA, ACTIVE_ALPHA, .5 ),vizact.sendsignal( go_signal ),vizact.waittime(1), vizact.fadeTo( ACTIVE_ALPHA,WAITING_ALPHA, .5 ) ]
	axes[ axis ].addAction( vizact.sequence( arrow_actions,1) )

	#Set up the object animations.
	where = [0,0,0]	
	back = [0,0,0]
	object_actions = [vizact.waitsignal( go_signal )]
	if kind == 'POSITION':
		where[axis], back[axis] = .5,0
		object_actions +=  [ vizact.moveTo( [where[0],where[1],where[2]], speed=1 ), vizact.moveTo( [back[0],back[1],back[2]], speed=1) ]
	elif kind == 'ROTATE':
		where[axis] = 1 
		object_actions += [  vizact.spin(  where[0],where[1], where[2], 360, 1 ) ]
	elif kind == 'SCALE':
		where, back = [1,1,1], [1,1,1]
		object_actions += [ vizact.sizeTo( where, speed=1 ),  vizact.sizeTo( back, speed=1 ) ]
		where[axis] = 2
	object.addAction( vizact.sequence( object_actions, 1) )

#Create the buttons that will cue transformations.
h = .1 
dims = ['X', 'Y', 'Z']
for transformation in ['POSITION', 'ROTATE','SCALE']:
	h += .1
	for d in range( len( dims ) ):
		button = viz.addButtonLabel( transformation + ' +' + dims[d] )
		button.translate( .85, 1 - h)
		h += .05
		vizact.onbuttondown( button, animate_actions, transformation, d )