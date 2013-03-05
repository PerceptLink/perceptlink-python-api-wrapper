import collections
import ApiBuilder


class ApiEngagementRecord:
	
	def __init__( self, transactionDate ):
		
		self.transactionDate = transactionDate
		
		self.context = ApiBuilder.ApiBuilder()
		self.identity = ApiBuilder.ApiBuilder()
		self.features = ApiBuilder.ApiBuilder()
		
		self.itemset = []
		
		self.engagementType = None
		self.engagementWeight = None
		
		self.charLimit = 128
		

	def identityBuilder( self, name, value ):
		
		self.identity.builder(name,value)
		
	def contextBuilder( self, name, value ):
		
		self.context.builder(name, value)
		
	def featureBuilder( self, name, value ):
		
		self.features.builder(name, value)
		
	def itemsetBuilder(self, item ):
		
		self.itemset.append( item )
		
	def setEngagement(self, engagementType, engagementWeight ):
		
		engagementWeight = engagementWeight * 1.0
		
		if engagementWeight < 0:
		
			engagementWeight = 0.0
			
		if len(engagementType) > self.charLimit:
			
			engagementType = engagmentType[0: self.charLimit + 1]
					
		self.engagementType = engagementType
		self.engagementWeight = engagementWeight
		
	def getContext( self ):
		
		return self.context.output()
	
	def getIdentity( self ):
		
		return self.identity.output()
	
	def getFeatures( self ):
		
		return self.features.output()
	
	def getItemset( self ):
		
		return self.itemset

	def getDate( self ):
		
		return self.transactionDate
	
	def getEngagementType( self ):
		
		return self.engagementType
	
	def getEngagementWeight( self ):
		
		return self.engagementWeight
	
	
	

	