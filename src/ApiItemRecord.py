import collections
import ApiBuilder

class ApiItemRecord:
	
	def __init__( self, item_id ):
		
		self.itemId = item_id
		self.itemFeatures = ApiBuilder.ApiBuilder()
		
	def builder( self, name, value):
		
		self.itemFeatures.builder(name, value)
		
	def getItemId( self ):
		
		return self.itemId
	
	def output( self ):
		
		return self.itemFeatures.output()
		
	