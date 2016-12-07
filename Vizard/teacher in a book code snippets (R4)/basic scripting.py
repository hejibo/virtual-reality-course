######################################
##1
##Define a constant and a variable.
#MY_CONSTANT = 'whatever'
#my_variable = 1
#
##Print their values.
#print MY_CONSTANT
#print my_variable
#
##Change the value of the variable.
#my_variable = my_variable + 1
#
##Print the value of the constant and the variable.
#print MY_CONSTANT
#print my_variable

##########################################

######################################
##2
##Define a constant and a variable.
#MY_CONSTANT = 'whatever'
#my_variable = 1
#
##Print their values.
#print MY_CONSTANT
#print my_variable
#print new_variable
#
##Change the value of the variable.
#my_variable = my_variable + 1
#
##Print the value of the constant and the variable.
#print MY_CONSTANT
#print my_variable
#
##########################################

######################################
##3
##Define a constant and a variable.
#MY_CONSTANT = 'whatever'
#my_variable = 1
#new_variable = 'another variable'
#
##Print their values.
#print MY_CONSTANT
#print my_variable
#print new_variable
#
##Change the value of the variable.
#my_variable = my_variable + 1
#
##Print the value of the constant and the variable.
#print MY_CONSTANT
#print my_variable
##
##########################################

###########################################
#4
##Define an array.
#my_array = ['a','b',1,2]
#
##Print the value of the second element (index 1).
#print my_array[1] 
#
###
##########################################
#4b
#Define a dictionary with two keys (and two values
#associated with those keys).
my_dictionary = {'Idaho':'Boise', 'Michigan': 'Lansing' }

#Call find the value for the key 'Idaho'.
print my_dictionary[ 'Idaho' ]

#
###########################################
#5
#my_variable = 0
#
#while my_variable < 5:
#	print my_variable
#	my_variable = my_variable + 1
	
#
#	
###
##########################################

###########################################
#6
#Define an array.
#my_array = ['a','b','c']
#
##Loop through every element in my_array.
#for element in my_array:
#	print 'current element is', element

##
##########################################

###########################################
#7
##Define an array.
#my_array = range( 5 )
#
##Loop through every element in my_array.
#for element in my_array:
#	print 'current element is', element

##
##########################################
#8
#for element in range(5):
#	print 'current element is', element
#	if element == 4:
#		print 'all done' 
#	else:
#		print 'wait, there is more'
################################################
##9
##Define a function named "multiply_by_twenty".
##This function requires an argument, "number".
#def multiply_by_twenty( number ):
#	answer = number*20
#	return answer
##############################################
##10
#for i in [1,5,23]:
#	#Call the function.
#	print multiply_by_twenty( i )
#############################################
#10.5
##Define a global variable.
#season = 'spring'
#
##Define a function
#def worker_bee():
#	if season == 'spring':
#		return 'honey'
#	else:
#		return 'i got nothing'
#
##Call the function and store the returned value as "bee_response".
#bee_response = worker_bee()
#print bee_response

###############################################
#11
#def fruitless():
#	apple = 'hello'
#
#fruitless()
#print apple
########################################
#12
#def fruitless():
#	global apple
#	apple = 'hello'
#
#fruitless()
#print apple
#########################################
#13
#
#value = 'hello'
#
#def change_variable():
#	value = 'goodbye'
#	print 'local ', value
#
#change_variable()
#
#print 'global ',value
#########################################
#14

#value = 'hello'
#
#def change_variable():
#	global value
#	value = 'goodbye'
#	print 'local ', value
#
#change_variable()
#
#print 'global ',value

###########################################
#15
#Define a class.
class most_basic:
	whatever = 'original value'

#Use the class to instantiate 
#two objects.
one_object = most_basic()
another_object = most_basic()

#Change the variable 
#in one of the objects.
one_object.whatever = 'changed value'

#Now print out the variable 
#from each object. Notice that
#they have different values
#(we changed "whatever" in 
#one but not the other). 
print one_object.whatever
print another_object.whatever



######################################################
#16
#Define the class.
class make_car:
	def peel_out( self ):
		#This function can 
		#be called from within
		#or outside of the 
		#class. It will print 
		#somthing and change the
		#object's moving variable.
		print 'vroom'
		print 'vroooom'
		print 'VROOOOOOOOOM'
	
#Instantiate an object using 
#the make_car class.
my_car = make_car()

#Call a function in the object.
my_car.peel_out()
#########################################################
#17
#Define the class.
class make_car:
	def __init__( self ):
		#Initialize the class. 
		#This method will be called
		#when you first instantiate 
		#an object.
		self.moving = False

	def peel_out( self ):
		#This method can be called 
		#from within or outside
		#of the class. It will print
		#somthing and change the
		#object's moving variable.
		print 'vroom'
		print 'vroooom'
		print 'VROOOOOOOOOM'
		self.moving = True
	
#Instantiate an object using 
#the make_car class.
my_car = make_car()

#Call a method in the object.
my_car.peel_out()
print my_car.moving
#####################################################
##18
#Define the class.
class make_car:
	def __init__( self ):
		#Initialize the class. 
		#This method will be called
		#when you first instantiate 
		#an object.
		self.moving = False

	def peel_out( self ):
		#This method can be called 
		#from within or outside
		#of the class. It will 
		#print somthing and change 
		#the object's moving variable.
		print 'vroom'
		print 'vroooom'
		print 'VROOOOOOOOOM'
		self.moving = True

class driver( make_car ):
	def leave_town( self ):
		print 'I am out of here'
		#Call an inherited method.
		self.peel_out()
		
#Instantiate an object using the 
#driver class.
my_driver = driver()

#Call a method in the object.
my_driver.leave_town()
#Refer to one of my_driver's 
#inherited variables.
print my_driver.moving
####################################################
##19
#Import the math module.
import math

#Define a function that uses a 
#method in the math module.
def get_square_root( number ):
	return math.sqrt( number )

#Call that function and print
#the returned value.
print get_square_root( 16 )

#####################################################
##20
import viz

#Use the viz module's go 
#function to render a 3D 
#world in a graphics 
#window.
viz.go()

#Use a for loop to . . .
for i in range( 5 ):
	#Use the viz module 
	#to add a 3D model.
	#The viz.add method 
	#will return a node3d object.
	ball = viz.add( 'white_ball.wrl' )
	#Use a node3D method 
	#to place the object 
	#in the world.
	ball.setPosition(i*.2,1.8,3)
########################################################

