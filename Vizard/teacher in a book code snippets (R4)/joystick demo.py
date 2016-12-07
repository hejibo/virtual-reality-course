import viz

viz.go()

viz.MainView.setPosition(5,4.5,-10.8)
viz.MainView.setEuler(0,0,0)

import vizjoy
joy = vizjoy.add()

def round_string( n ):
	#Function to round arrays or numbers to a more presentable size.
	string = ''
	try:
		string += '[ '
		for i in n:
			string += str( round(i,2) ) + ', '
		string = string[0:-2] + ']'
	except:
		string = str( round( n, 2 ) )
	return string

def add_text( message, scale, position ):
	text = viz.addText( message )
	text.alignment( viz.TEXT_CENTER_CENTER )
	text.scale( scale )
	text.setPosition( position )	
	return text
	

#Create dictionary for event text and models.
event_flags = [ 'SLIDER', 'HAT', 'MOVE', 'TWIST', 'BUTTONDOWN', 'BUTTONUP' ]
event_pos = [[2.5, 5],[2.5, 8],[7.5, 5],[7.5, 8], [2.5,2], [7.5,2]]
#event_val =  
eventer = {}
MODEL_Y = 3.5
for i in range(len(event_flags)):
	text = add_text( event_flags[ i ] + ' event', [.5,.5,1], [event_pos[i][0], event_pos[i][1], 1] )
	sample_text = add_text( '', [.2,.2,1], [ event_pos[i][0], event_pos[i][1]-.5, 1 ])
	if i < 4:
		model = text.add( 'art/arrows.IVE')#lantern.ive' )
		model.setScale(.75,.75,.75)
		model.setPosition([0,-MODEL_Y,0], viz.REL_PARENT )
	else: 
		model = 0
	dic = {}
	for key in ['text', 'model', 'sample_text']:
		dic[ key ] = eval( key )
	eventer [ event_flags[ i ] ]= dic




#Create dictionary for sampling text and models.
sample_commands = [ 'Hat','Angle', 'Position', 'Rotation', 'Slider', 'Twist' ]
sample_pos = [[1.5,5], [8.5, 5],[5.5,5],[1.5, 8],[8.5, 8],[5.5, 8], [4.5, 3]]
sampler = {}
for i in range( len( sample_commands ) ):
	text = add_text( 'get' + sample_commands[i], [.5,.5,1], [sample_pos[i][0], sample_pos[i][1], 1 ])
	sample_text = add_text( '', [.2,.2,1], [sample_pos[i][0], sample_pos[i][1]-.5, 1] )
	model = text.add( 'art/arrows.IVE')#'art/lantern.ive' )
	model.setScale(.75,.75,.75)
	model.setPosition([0,-MODEL_Y,0], viz.REL_PARENT )	
	function =  'joy.get' + sample_commands[i] + '()' 
	dic = {}
	for j in ['text', 'model', 'function', 'sample_text']:
		dic[ j ] = eval( j )
	sampler[ sample_commands[ i ] ] = dic

#Create texts for buttons.
buttonTexts = {}
for kind in ['events', 'sampler']:
	buttonTexts[ kind ] = {}
	interval = joy.getButtonCount()/11
	for i in range(1, joy.getButtonCount()+1 ):
		text = viz.addText( str(i))#, viz.SCREEN )
		if kind == 'events':
			text.setScale( .2, .2 )
		else:
			text.setScale(.5,.5 )
		text.alignment( viz.TEXT_CENTER_CENTER )
		text.setPosition(i-1, 1,1 )
		buttonTexts[ kind ][ i ] = text 
getButtonText = add_text( 'isButtonDown', [.5,.5,0], [5.5,2,1] )


#Function to switch between events and sampling.
def switch(which):
	options = [sampler, eventer] 
	options.remove( which )
	next, prev = which, options[0]
	print next
	for thing in ['model', 'text', 'sample_text' ]:
		for key in next.keys():
			if next[key][ thing ]:
				next[key][ thing ].visible( viz.ON )
		for key in prev.keys():
			if prev[key][thing]:
				prev[key][thing].visible( viz.OFF )
	
	if next == sampler:
		getButtonText.visible( viz.ON )
		for key in buttonTexts['events'].keys():
			buttonTexts['events'][ key ].visible( viz.OFF )
	else:
		getButtonText.visible( viz.OFF )
		for key in buttonTexts['events'].keys():
			buttonTexts['events'][ key ].visible( viz.ON )


#Sample data.
def updateGets():
	sampler['Hat']['model'].setAxisAngle( 0,0,-1,joy.getHat() )
	sampler['Angle']['model'].setEuler( 0,0,joy.getAngle() )
	pos = joy.getPosition()
	sampler['Position']['model'].setPosition(pos[0], -(pos[1]+MODEL_Y), pos[2] )
	sampler['Rotation']['model'].setEuler( joy.getRotation() )
	sampler['Slider']['model'].setPosition([joy.getSlider(),-MODEL_Y,0],viz.ABS_PARENT )
	sampler['Twist']['model'].setAxisAngle( -1,0,0,joy.getTwist()*180 )

	for key in sampler.keys():#gets.keys():
		dic = sampler[ key ]
		string = round_string( eval(dic[ 'function' ] ))
		dic[ 'sample_text' ].message( string )

	for i in range(1, joy.getButtonCount() + 1):
		if joy.isButtonDown( i ) and getButtonText.getVisible() :
			buttonTexts['sampler'][ i ].visible( viz.ON )
		else:
			buttonTexts['sampler'][ i ].visible( viz.OFF )
			
vizact.ontimer(.1, updateGets )

#Create action to animate event texts.
grow = vizact.parallel( vizact.sizeTo( [1,1,1], time=.1 ), vizact.fadeTo(viz.RED, begin=viz.WHITE, time=.1 ) ) 
shrink = vizact.parallel( vizact.sizeTo( [.2,.2,.2], time=.1 ), vizact.fadeTo(viz.WHITE, begin=viz.RED, time=.1 ) ) 
growAndShrink = vizact.sequence( [ grow, shrink ] )
highlight = vizact.sequence( [vizact.fadeTo(viz.RED, begin=viz.WHITE, time=.5), vizact.fadeTo(viz.WHITE, begin=viz.RED, time=.01)])


def all_event_changer( kind, value ):
	string = round_string( value )
	eventer[ kind ][ 'text' ].color( viz.RED )
	eventer[ kind ][ 'sample_text' ].message( round_string( value ) )

def buttondown( e ):
	#print e.button
	buttonTexts[ 'events' ][ e.button ].addAction( grow )
	eventer[ 'BUTTONDOWN' ]['text'].color( viz.RED )

def buttonup( e ):
	#print e.button
	buttonTexts[ 'events' ][ e.button ].addAction( shrink )
	eventer[ 'BUTTONUP' ]['text'].color( viz.RED )

def slider( e ):
	eventer[ 'SLIDER' ]['model'].setPosition([e.slider,-MODEL_Y,0],viz.ABS_PARENT )
	all_event_changer( 'SLIDER', e.slider )

def twist( e ):
	eventer[ 'TWIST' ]['model'].setAxisAngle([0,0,-1,e.twist*180] )
	all_event_changer( 'TWIST', e.twist )

def joymove( e ):
	eventer[ 'MOVE' ]['model'].setPosition( [e.pos[0], -(e.pos[1]+MODEL_Y), e.pos[2]], viz.ABS_PARENT )
	all_event_changer( 'MOVE', (e.pos[0],-(e.pos[1]),e.pos[2]) )
	
def hat( e ):
	eventer[ 'HAT' ]['model'].setAxisAngle([0,0,-1,e.hat])
	all_event_changer( 'HAT', e.hat )

def clearColor():
	for key in eventer.keys():
		eventer[ key ]['text'].color( viz.WHITE )
vizact.ontimer(.5, clearColor )
viz.callback(vizjoy.BUTTONDOWN_EVENT,buttondown)
viz.callback(vizjoy.BUTTONUP_EVENT,buttonup)
viz.callback(vizjoy.SLIDER_EVENT,slider)
viz.callback(vizjoy.HAT_EVENT,hat)
viz.callback(vizjoy.MOVE_EVENT,joymove)
viz.callback(vizjoy.TWIST_EVENT,twist) 

#Create a drop-down menu for all the "has" functions.
import vizmenu
menu = vizmenu.add()
a = {0:'no', 1:'yes'}
b = [['Force feedback','FFB']]
for dim in ['X','Y','Z']:
	b.append( ['Rotation about the ' + dim + ' axis', 'R' + dim ] )
	b.append( ['Movement about the ' + dim + ' axis', dim ] )
b.sort()
capabilities = menu.add('Joystick capabilities')
for thing in b:
	capabilities.add(viz.TEXT3D, thing[0] + ': ' + a[eval( 'joy.has' + thing[1] + '()' )]  )
capabilities.add( viz.TEXT3D, 'Number of buttons: '+ str( joy.getButtonCount() ) )

#Add menu to switch back and forth between sampling and events.
events_samples = menu.add('Events vs sampling')
events_button = events_samples.add( viz.RADIO, 0, 'Events' )
vizact.onbuttondown( events_button, switch, eventer )
samples_button = events_samples.add( viz.RADIO, 0, 'Samples' )
vizact.onbuttondown( samples_button, switch, sampler )
events_button.set( viz.DOWN )

#Add menu to play with the rumble feature.
ffb_menu = menu.add('Force feedback')
ffb_on_button = ffb_menu.add( viz.RADIO, 1, 'Apply force' )
vizact.onbuttondown( ffb_on_button, joy.addForce, 1, 1)
ffb_off_button = ffb_menu.add( viz.RADIO, 1, 'No force' )
vizact.onbuttondown( ffb_off_button, joy.setForce,0,0 )
ffb_off_button.set( viz.DOWN )


switch(eventer)
