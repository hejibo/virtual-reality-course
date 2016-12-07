import viz
viz.go()

#Put the viewpoint in a good place to see the texture quad.
viz.MainView.setPosition( 0, .68,-1.3 )

#Add a model and grab one of its chidren to put the textures on.
model = viz.add('art/window.ive')
window = model.getChild( 'glass' )

#Add the texture files.
clouds = viz.addTexture( 'art/tileclouds.jpg' )
moon = viz.addTexture( 'art/full moon.jpg' )

#Apply the textures to the window.
#The moon will go in the window's first unit(0) and the clouds will go in the second (1).
window.texture( clouds, '', 1 )
window.texture( moon, '', 0 )


#Set the wrapping mode for the clouds to be REPEAT
#so that as the surface's texture matrix translates,
#there will still be texture to show.
clouds.wrap( viz.WRAP_S, viz.REPEAT )
clouds.wrap( viz.WRAP_T, viz.REPEAT )

#Add a slider and put it on 
#the bottom of the screen.
slider = viz.addSlider()
slider.setPosition(.5,.1)
#This function will be called 
#every time the slider
#is moved and will swap the 
#textures according to the
#slider's position.
def swap_textures( slider_position ):
	#Use the slider's position to get 
	#the amount of cloud blend.
	cloud_amt =  slider_position
	#Blend the clouds (unit #1) in that amount.	
	window.texblend( cloud_amt, '', 1 )
#Set up the slider event to call our function.	
vizact.onslider( slider, swap_textures )
#Set the initial blend to match the slider. 
swap_textures(0)


#Create a matrix that we'll use to 
#the surface's texture matrix.
matrix = vizmat.Transform()
#This function will move the clouds incrementally.
def move_clouds():
	#Post translate the matrix (move it in the s and t dimensions).
	matrix.postTrans(.0005,.0005,0)
	#Apply it to the surface.
	window.texmat( matrix, '', 1 )
#Run the timer every hundredth of a second. 
vizact.ontimer( .01, move_clouds )






