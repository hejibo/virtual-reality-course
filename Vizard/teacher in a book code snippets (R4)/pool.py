#Import the viz, math, and vizact modules.
import viz
import math
import vizact

class pool_game:
	#Initialize the class.
	def __init__( self ):
		#Call functions outside the class. 
		pool_table()
		pool_lights()

		#Call a methods within the class.
		#This function will return objects that will belong
		#to each instantiation of the class. Because we use
		#the 'self.' prefix, we'll be able to refer to 
		#the table and balls variables throughout the class.
		self.balls = self.add_balls()		
		
		#Call classes outside of the function.
		self.cueball = pool_ball( 0 )
		self.cue = cue()
		
		#Reset the models with one 
		#of the class's methods.
		self.rack_balls()
		
	def add_balls( self ):
		#Create an empty array.
		balls = []
		#Loop through 15 times.
		for i in range(15):
			#Use create a ball object with the pool_ball 
			#class.
			ball = pool_ball( i + 1 ) 
			#Add the object to our array.
			balls.append( ball )
		#Return the array.
		return balls

	def rack_balls( self ):
		#Call one of the methods in this class.
		self.set_cueball()
		#Use looping, along with some constants and variables
		#to take balls from self.balls and place them in the world
		#in the standard pool ball triangle.
		zs = range(-2,3)
		x = 0
		cycle = viz.cycle( self.balls )
		XFACTOR = .058
		ZFACTOR = .068
		HEIGHT = 1
		while zs:
			new_zs = []
			for i in range(len(zs)):
				ball = cycle.next()
				ball.reset()
				ball.setPosition( (XFACTOR*x)-1.0, HEIGHT, ZFACTOR*zs[i])
				if i < (len(zs)-1):
					new_zs.append((zs[i] + zs[ i + 1] )/2.0)
			zs = new_zs
			x += 1		
	
	def set_cueball( self ):
		#Use methods available to reset the cueball's physis,
		#and to place the cueball and cue
		#objects.
		self.cueball.reset()
		self.cueball.setPosition(.5,1.03,0)
		self.cue.setPosition(.5,1.03,0)
		self.cue.setEuler(-180,0,0)

	def shoot( self ):
		#Use methods available to the cueball and cue
		#objects to shoot the cueball.		
		self.cueball.prepare_to_be_shot()
		self.cue.shoot()
		
	def set_up_shot( self ):
		#Put the cue in the sample place as the cueball.				
		self.cue.setPosition( self.cueball.getPosition() )

def pool_table():
	#Add a 3D model using the viz module.
	#This object is an instantiation of the vizNode class.
	table = viz.add('art/pool table.ive')
	table.setEuler(180,0,0)
	#Call one of the methods available to this object 
	table.collideMesh()
	#Return the object.
	return table	

def pool_lights():
	#Add light to the virtual world using
	#more methods from the viz module.
	viz.MainView.getHeadLight().remove()
	light = viz.addLight()
	light.position( 1,3,1,1 )
	light.spread( 70 )
	light.direction( 0,-1,0)


class pool_ball( viz.VizNode ):
	#This class will inherit from the VizNode class.
	#It also needs a "number" value when it's called.
	def __init__( self, number ):
		#Call a method in this class, passing it the 
		#argument "number". 
		ball = self.add_ball( number )
		#Identify the ball object as the heir to the 
		#VizNode class.
		viz.VizNode.__init__( self, ball.id )
		
	def add_ball( self, number ):
		#This method adds a pool_ball and its physics.
		#Use the viz module to add a 3D model.
		ball = viz.add('art/pool ball.ive')
		
		#Add a texture file.
		tex = viz.addTexture( 'art/poolb' + str( number ) + '.jpg' )
		#Apply that texture to the ball model.
		ball.texture( tex )
			
		#Add a mesh for physics using methods available to 
		#VizNode objects.
		mesh = ball.collideSphere()
		mesh.setHardness(1)
		mesh.setFriction(1)
				
		#Use collisions with this shape in collision events.
		ball.enable( viz.COLLIDE_NOTIFY )
		
		#Return the object. 
		return ball
	
	def prepare_to_be_shot( self ):
		#Use the VizNode method applyForce to apply a tiny force.
		#This command is a workaround to deal with the fact that 
		#collide meshes (the cue in this case) will not act on
		#static objects.
		self.applyForce([.001,.001,.001],.001)
	
		
class cue( viz.VizNode ):
	def __init__( self ):
		#Call the add_cue method within this class.
		cue = self.add_cue()
		#Define the parameters of shooting.
		self.shot = self.define_shot()
		#Identify the cue as an heir to the VizNode class.
		viz.VizNode.__init__( self, cue.id )
		
	def add_cue( self ):
		#Add a model using the viz module. 
		cue = viz.add( 'art/pool cue.ive' )
		#Set this model's physics.
		c = cue.collideMesh()
		c.setHardness(1)
		cue.disable( viz.PHYSICS )
		#Return the model.
		return cue
	
	def define_shot( self ):
		#Define the action that is a shot.
		#Move the cue back and forth.
		meters, time = 1.0, .2
		shoot = vizact.move(meters,0,0,time)
		withdraw = vizact.move(-meters,0,0,time)
		#Turn off physics.
		turn_off_physics = vizact.call( self.disable, viz.PHYSICS ) 
		#Put these actions together in a sequence.
		seq = vizact.sequence( [shoot, withdraw, turn_off_physics] )
		#Return the sequence.
		return seq
		
	def shoot( self ):
		#Enable physics on the cue.
		self.enable( viz.PHYSICS )
		#Call the action.
		self.addAction( self.shot )
		









