import viz
viz.go()

#Add a model.
court = viz.add('court.ive')
#Make it invisible.
court.visible( viz.OFF )

##Write the function that will be called.
#def onKeyDown(key):
#	#If the key that was pressed is the
#	#a key, then make the court visible.
#	if key == 'a':
#		court.visible( viz.ON )
##Issue a callback for keyboard events.
##When those events occur, call the
##onKeyDown function.
#viz.callback(viz.KEYDOWN_EVENT,onKeyDown)

##This command comes from the vizact library.
##We give the key to wait for, the function to
##call, and the argument to pass that function.
#vizact.onkeydown( 'a', court.visible, viz.ON )

#This command will wait for 1 second  
#to pass and then it will call the 
#court.visible function with the viz.ON
#argument. The 0 here means that the 
#timer will only go off once.
vizact.ontimer2( 1, 0, court.visible, viz.ON )