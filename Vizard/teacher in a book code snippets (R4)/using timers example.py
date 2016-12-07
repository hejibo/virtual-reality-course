import viz
viz.go()

#Set the position of the view.
viz.MainView.setPosition( 0, 2, 0)
viz.MainView.setEuler( 0,90,0 )

#Set the background color.
viz.clearcolor( [.3,.3,.3] )

#Add the spider avatar.
spider = viz.add('art/spider/spider1.cfg')
spider_bone = spider.getBone( 'bone_root' )
spider.texture(viz.addTexture( 'art/spider/euro_cross.tif' ))
spider.setScale(.04,.04,.04)
#Animate the spider's legs.
spider.state(2)

#Animate the spider travelling 
#in a spiral path.
increment = 0
C = 0.01
import math
def move_spider():
	global increment
	#Increase the increment every 
	#time the function is executed.
	increment += .02
	#Use some trig to place the 
	#spider on the spiral.
	x = C*increment*math.cos( increment )
	z = C*increment*math.sin( increment )
	spider.setPosition( [x,0,z] )
	#Find the increment the spider 
	#should be facing.
	face_angle = vizmat.AngleToPoint([0,0], [x,z])-90
	spider.setEuler( [face_angle, 0, 0] )
#Call the move_spider function every 
#hundredth of a second.
vizact.ontimer(.01,move_spider )


#Start an on-the-fly object for the web.
viz.startlayer( viz.LINE_STRIP )
viz.vertex(0,0,0)
myweb = viz.endlayer()

#Make the object dynamic, since we'll 
#be adding to it.
myweb.dynamic()

#Add the next vertex and link it to 
#the spider.
current_vertex = myweb.addVertex([0,0,0])
web_link = viz.link( spider, myweb.Vertex( 0 ) )

def lay_web():
	#This function will lay the most 
	#recent vertex of the web down.
	#We make these variables global 
	#because we'll be changing them.
	global web_link, current_vertex
	
	#Remove the current link between 
	#web and spider.
	web_link.remove()
	
	#Set the vertex at the spider's 
	#current location.
	myweb.setVertex( current_vertex, spider.getPosition() )
	
	#Add a new vertex and link it 
	#to the spider.
	current_vertex = myweb.addVertex( spider.getPosition() )
	web_link = viz.link( spider_bone, myweb.Vertex( current_vertex ) )

#Call the function on a timer.
vizact.ontimer(.5,lay_web)
