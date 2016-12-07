import viz
import viztask

viz.go()

#Position the viewpoint.
viz.MainView.setPosition(0,1.8,6)
viz.MainView.setEuler(180,0,0)

woman = viz.addAvatar('vcc_female.cfg')
woman.state(1)

#Add a text message.
text = viz.addText('hit the spacebar to begin')
text.alignment( viz.TEXT_CENTER_BASE )
text.setEuler(180,0,0)
text.setScale(.3,.3,.3)
text.setPosition(0,2,0)
appear = vizact.fadeTo(1, begin=0, time=1)
disappear = vizact.fadeTo(0, begin=1, time=1)

#Add a balloon and an action for that balloon.
duck = viz.add('duck.cfg')
duck.scale( .01,.01,.01)
duck.setPosition(0,0,-5)
duck.state(1)
grow = vizact.sizeTo( [3,3,3], time=5)
jump = vizact.animation(2)

#Add a woman who can walk away.
run = vizact.walkTo([10,0,10], walkSpeed=1.7, turnSpeed=90, walkAnim=11)

#1. Wait for the spacebar.
def mytask():
	yield viztask.waitKeyDown( ' ' )

#2. Make the text fade away.
#This is the function you'll need to make the text visible.
#text.addAction( disappear )
	yield viztask.addAction( text, disappear )

#3. Change the text to 'something is happening'.
	text.message( 'something is happening' )
	
#4. Show the text and then hide the text.
#These are the functions you'll need to make the text visible.
#text.addAction( appear )
#text.addAction( disappear )
	yield viztask.addAction( text, appear )
	yield viztask.addAction( text, disappear )
	
#5. Make the duck grow (and wait for it to grow ).
#This is the function you'll need to make the duck grow.
#duck.addAction( grow )
	yield viztask.addAction( duck, grow )

#6. Wait for a second and then make the duck jump
#This is the function you'll need to make the duck hop.
#duck.execute( 2 )
	yield viztask.waitTime( 1 )
	duck.execute( 2 )
	

#7. Wait a fraction of a second and then make the woman run jump.
#This is the function you'll need to make the woman run away.
#woman.addAction( walk )
	yield viztask.waitTime( .5) 
	woman.addAction( run )


#Schedule the task.	
viztask.schedule( mytask() )

vizact.onkeydown( 's', viz.window.startRecording, 'test.avi' )
vizact.onkeydown( 't', viz.window.stopRecording )


