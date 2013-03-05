
import collections

class ApiBuilder:
	
	def __init__(self):
		
		self.elements =  collections.OrderedDict()
		self.charLimit = 128
		
	def builder(self, name, value):
		
		self.elements[ name ] = self.__preprocessObject(value)
		
	def output(self):
		
		return self.elements
	
	def __preprocessObject( self, obj ):
		
		if isinstance( obj, str):
			
			obj = obj[0: self.charLimit]
			
		return obj