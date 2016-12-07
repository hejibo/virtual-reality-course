import viz
viz.go()


#Place the viewpoint where you want it.
viz.MainView.setPosition(0,1.8,-5)


#Add models.
tent = viz.add('art/tent.ive')
barrel = viz.add('art/barrel.ive' )
ball = viz.add('soccerball.ive')

#Shift the barrel to a different position.
barrel.setEuler( [0, 0, 90] )
barrel.setPosition( [ -1,.5,0 ] )

#Use actions to make some of the models
#spin
ball.addAction( vizact.spin(0,1,0,360 ) )
barrel.addAction( vizact.spin( 0,1,0,-90 ) )

#Add a female avatar.
female = viz.add('vcc_female.cfg')
female.setEuler( 180,0,0 )
female.state(2)

#Add a male avatar and pose him.
male = viz.add('vcc_male.cfg')
#Use the debaser module to pose the avatar
#using a text file created with the avatar
#demo.
import debaser
debaser.pose_avatar( male, 'links_pose.txt' )
male.setPosition([1,0,0])
male.setEuler( -45,0,0 )
male.state(5)

#Get the bone of one of the avatar's fingers,
#and link the ball to it.
finger_bone = male.getBone( 'Bip01 R Finger1Nub' )
finger_link = viz.link( finger_bone, ball )
#Now add an offset so that the ball appears to
#rest on the avatar's finger.
finger_link.setOffset( [0,.1,0 ] )
#Set the link's mask so that it only uses
#position data.
finger_link.setMask( viz.LINK_POS )


#Link the female to the barrel.
barrel_link = viz.link( barrel, female )
#Set the mask of that link.
barrel_link.setMask( viz.LINK_POS )
#Offset the link.
barrel_link.setOffset( [-.5,.4,0] )


#Link the barrel to the mouse.
mouse_link = viz.link(viz.Mouse, barrel )
#Use the position data from the x and y of
#the mouse for the x and z of the barrel.
mouse_link.swapPos( [1,3,2] )
#Use .5 instead of the mouse data for the barrel.
mouse_link.setPos( [None,.5,None] )


#Link the view to the male's head.
head_bone = male.getBone( 'Bip01 Head' )
#view_link = viz.link( head_bone, viz.MainView )
#Set the eyeheight at 0 (so the default
#eyeheight is not added to the data).
#viz.eyeheight( 0 )
