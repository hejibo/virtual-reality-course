import viz


#Read in a text file and make into a nested dictionary.
def text_to_dict( file ):
	open_file = open( file, 'r' )
	lines = open_file.readlines()
	keys = lines[0].split('\t')
	keys[-1] = keys[-1][0:-1]
	#print 'keys',keys
	dict = {}
	for line in lines[1:]:
		if len( line[0:line.find('\n')] )<=5:
			continue
		
		split_line = line.split( '\t' )
		split_line[-1] = split_line[-1][0:-1]
		dict[ split_line[0] ] = {}
		
		for i in range(1, len(keys) ):

			try: 
				dict[ split_line[0] ][ keys[i] ] = eval( split_line[ i ] )
			except:
				dict[ split_line[0] ][ keys[i] ] = split_line[ i ] 	
	open_file.close()
	return dict

		
#Make a dictionary from one tab-delimited file 
#Where the first column is the key and the other
#columns are in an array for that key.
def text_to_one_dict( filename ):
	file = open( filename, 'r' )
	lines = file.readlines()
	dict = {}
	for line in lines[1:]:
		line = line.rstrip('\n')
		split = line.split('\t')
		array = []
		for column in split[1:]:
			try:
				value = eval( column )
			except:	
				value = column
			array.append( value )	
		dict[ split[ 0 ] ] = array
	file.close()
	return dict
	

#Read in a nested dictionary (2 levels) and record it on a text file.
def dict_to_text( dict, filename ):
	file = open( filename, 'w' )
	
	keys = dict.keys()
	keys.sort()
	subkeys = dict[keys[0]].keys()
	subkeys.sort()
	
	#create the first line.
	string = 'key'
	for subkey in subkeys:
		string += '\t' + str( subkey )
	string += '\n' 
	
	#Add each following line.
	for key in keys:
		string += str( key ) 
		for subkey in subkeys:
			string +=  '\t' + str( dict[ key ][ subkey ] )
		string += '\n'
	
	file.write( string )
	file.close()
	print 'done' 


#Set up a dictionary of a node's pos, ori, and scale
#with the keys x,x_scale, yaw, etc.
def coord_to_dict( node ):
	pos = node.getPosition( viz.ABS_GLOBAL )
	ori = node.getEuler( viz.ABS_GLOBAL )
	scale = node.getScale( viz.ABS_GLOBAL )
	coords = ['x','y','z']
	dims = ['yaw', 'pitch', 'roll' ]
	dict = {}
	for i in range(3):
		dict[ coords[i] ] = pos[ i ]
		dict[ coords[i] + '_scale' ] = scale[i]
		dict[ dims[i] ] = ori[i]
	return dict
	
#Return arrays for pos, ori and scale given a dictionary
#with the keys x,x_scale, yaw, etc.
def dict_to_coord( dict ):
	pos = []
	ori = []
	scale = []
	coords = ['x','y','z']
	dims = ['yaw', 'pitch', 'roll' ]
	for i in range(3) :
		pos.append( dict[ coords[ i ] ] )
		scale.append( dict[ coords[ i ] + '_scale' ]) 
		ori.append( dict[ dims[ i ]] ) 
	return pos, ori, scale

#Flip a dictionary's values to the keys and vice versa.
def flip_dict( dict ):
	new_dict = {}
	values = dict.values()
	for key in dict.keys():
		if values.count( dict[ key ]  )>1:
			return False
		else:
			new_dict[ dict[ key ] ] = key
	return new_dict


#Pose an avatar's body with a dictionary of its bones'
#eulers.
def pose_avatar( avatar, text_file ):
	dict = text_to_dict( text_file ) 
	for bone in dict.keys():
		this = avatar.getBone( bone )
		if abs( sum( dict[ bone ][ 'ori' ] )) <= .1:
			continue
		this.lock()
		this.setEuler( dict[ bone ][ 'ori' ], viz.AVATAR_LOCAL )

	

		