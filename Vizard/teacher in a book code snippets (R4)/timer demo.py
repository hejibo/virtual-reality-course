import viz

viz.go()

viz.MainView.setPosition([.16,0,-.7])


object = viz.add('soccerball.ive')
running_timers = []
def reset():
	for timer in running_timers:
		timer.setEnabled( viz.OFF )
	object.setPosition( [0,0,0] )
	object.setEuler( [0,0,0] )
	error_text.message( WAIT_MESSAGE )

def get_data_and_go():
	global running_timers
	values = []
	for box in boxes:
		value = box.get()
		try:
			values.append( float( value ) )
		except:
			error_text.message( ERROR_MESSAGE )
			return
	error_text.message( GOING_MESSAGE )
	running_timers.append ( vizact.ontimer2( values[2],values[1], go, values[0]  ) )
	running_timers.append ( vizact.ontimer2( values[2]*(values[1]+ 1),1, done ) )
	
def go(distance):
	object.setEuler([distance,0,0],viz.REL_LOCAL )

def done():
	error_text.message( RESET_MESSAGE )

import vizinfo
info = vizinfo.add('Timer parameters')
boxes = []
boxes.append( info.add( viz.TEXTBOX, 'increment of change' ))
boxes.append( info.add(viz.TEXTBOX, 'repeats' ) )
boxes.append( info.add( viz.TEXTBOX, 'timer expiration time' ))
go_button = info.add( viz.BUTTON_LABEL, 'START TIMER' )
reset_button = info.add( viz.BUTTON_LABEL, 'RESET' )
WAIT_MESSAGE = 'Enter numbers in each field' 
GOING_MESSAGE = 'Animation running'
ERROR_MESSAGE = 'Those are not numbers'
RESET_MESSAGE = 'Hit reset to try again'
error_text = info.add( viz.TEXT3D, WAIT_MESSAGE )
vizact.onbuttondown( go_button, get_data_and_go )
vizact.onbuttondown( reset_button, reset )

reset()