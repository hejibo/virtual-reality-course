import viz
viz.go()

#Add a model of a forest.
forest = viz.add('art/forest.ive' )

#Add an avatar to stand there idly.
a = viz.addAvatar( 'vcc_male.cfg')
a.setEuler( [20,0,0] )
a.setPosition( [-.78,0,.3] )
a.state(1)

#Set the viewpoint's position and orientation so that we'll be able to see our scene.
viz.MainView.setPosition( [-.75,1.8,4.2 ] )
viz.MainView.setEuler( [-180,4, 0] )

#Disable the default head light.
viz.MainView.getHeadLight().disable()


#Add a directional light source. 
moon_light = viz.addLight()
moon_light.position(0,1,0,0)
#Give the light a moonish color and intensity.
moon_light.color( [.6,.7,.9] )
moon_light.intensity( 1 )

#Disable the moon light for a moment.
moon_light.disable()

#Add a model of a lantern and place it so that it appears to hand on a the tree.
lantern = viz.add('art/lantern.ive')
lantern_position = [ 0.14 , 1.5 , 0.5 ]
lantern.setPosition( lantern_position )

#Add a light source to put inside the lantern.
lantern_light = viz.addLight()

#Define the light as a point, positional light.
#This is done with the last '1' in this command's arguments.
lantern_light.position( 0,0,0,1 )

#Link the light to the lantern.
viz.link( lantern, lantern_light )

#Grab the flame part of the lantern model and give an emissive quality to emulate light.
flame = lantern.getChild( 'flame' )
flame.emissive( viz.YELLOW )

#Play with the light source's parameters.
lantern_light.color( viz.YELLOW )
lantern_light.quadraticattenuation( 1 )
lantern_light.intensity( 8 )

#Give the lantern some shine.
lantern.specular(viz.YELLOW)
lantern.shininess(10)

#Disable the lantern light.
#lantern_light.disable()



#Add a model of a torch and place it in the scene.
torch = viz.add('art/flashlight.IVE')
torch.setPosition( [ -1.16 , 1.78 , 1.63 ])
#Add a light for the torch.
flash_light = viz.addLight()
#Make the light positional.
flash_light.position(0,0,0,1)
#Make this positional light a spot light by limiting its spread.
flash_light.spread(45)
flash_light.spotexponent( 40 )

#Link the light source to the torch.
viz.link( torch, flash_light )

torch.addAction( vizact.spin( 0,1,0,90, viz.FOREVER ) )

