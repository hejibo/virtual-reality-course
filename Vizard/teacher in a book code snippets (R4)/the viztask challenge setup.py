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
grow = vizact.size( 3,3,3,5, viz.TIME)
jump = vizact.animation(2)

#Add a woman who can walk away.
run = vizact.walkTo([10,0,10], walkSpeed=1.7, turnSpeed=90, walkAnim=11)

#1. Wait for the spacebar.

#2. Make the text fade away.
#This is the function you'll need to make the text visible.
#text.addAction( disappear )

#3. Change the text to 'something is happening'.

#4. Show the text and then hide the text.
#These are the functions you'll need to make the text visible.
#text.addAction( appear )
#text.addAction( disappear )

#5. Make the duck grow.
#This is the function you'll need to make the duck grow.
#duck.addAction( grow )

#6. Make the duck jump.
#This is the function you'll need to make the duck hop.
#duck.execute( 2 )

#7. Make the woman run.
#This is the function you'll need to make the woman run away.
#woman.addAction( run )

