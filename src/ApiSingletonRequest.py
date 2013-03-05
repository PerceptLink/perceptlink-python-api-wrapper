import collections

class ApiSingletonRequest:
	
	def __init__(self):
		
		self.data = collections.OrderedDict()
	
	def builder(self, name, value):
		
		self.data[name] = value
		
	def output(self):
		
		return self.data