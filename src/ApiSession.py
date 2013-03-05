import sys

import ApiDataPacketBuilder
import ApiRequestMaker
import ApiResponseReader
import json

class ApiSession:
	
	def __init__(self, apiKey, apiPostURL):
		
		self.batch_size = 1000
		self.apiKey = apiKey
		self.apiPostURL = apiPostURL
		self.mostRecentApiSessionRecord = None
		self.asrList = []
		
		self.rawHTTPRequest = None
		self.rawHTTPResponse = None
		
		if (apiKey == None) or (apiPostURL == None):
			
			self.consolePrint("Did not supply an API Key or URL", True)
				
	def addEngagementEvent( self, t_asr ):
		
		self.asrList.append( t_asr )
		
	def dispatchEngagementEvents( self ):
		
		if len(self.asrList) < 1:
			
			self.consolePrint( "No records to dispatch", True)
			
		pb = ApiDataPacketBuilder.ApiDataPacketBuilder()
		dat = pb.buildDataPacket( self.asrList )
		
		list_size = len(self.asrList)
		counter = 0
		
		while counter < list_size:
			
			end_marker = counter + self.batch_size
			
			if end_marker > list_size:
				
				end_marker = list_size
				
			batch = dat[ counter : end_marker]
			
			areq = ApiRequestMaker.ApiRequestMaker( self, self.apiPostURL, self.apiKey )
			result = areq.postData( batch )
						
			if ApiResponseReader.ApiResponseReader.getResultCode( result ) < 400:
				
				counter = end_marker
				self.mostRecentApiSessionRecord = batch[ len(batch)-1 ]
				
			else:
				
				rm = ApiResponseReader.ApiResponseReader.getResultMessage( result )
				self.consolePrint("Post failure with message: " + str(rm) +"; you can get most recent successfully sent record and try again", False)
				break;
				
	
	def fetchLastEngagementRecordSubmitted( self):
		
		areq = ApiRequestMaker.ApiRequestMaker( self, self.apiPostURL, self.apiKey);
		res = areq.fetchLastEngagementRecordSubmitted();
		self.setRawHTTPResponse(res);
		self.verifyFetchState( res )
		lRecord = json.loads( res )
		
		return lRecord;
	
	def getItemRecommendation(self, req):
		
		areq = ApiRequestMaker.ApiRequestMaker( self, self.apiPostURL, self.apiKey )
		result = areq.fetchRecommendation( req.output() )
		self.setRawHTTPResponse(result)
			
	def getItemRecommendations( self ):
		
		areq = ApiRequestMaker.ApiRequestMaker( self, self.apiPostURL, self.apiKey )
		
		return ApiResponseReader.ApiResponseReader.getDataElements( areq.fetchRecommendations() )
	
	def getContentAllocation(self, req ):
		
		areq = ApiRequestMaker.ApiRequestMaker( self, self.apiPostURL, self.apiKey )
		result = areq.fetchAllocation( req.output() )
		self.setRawHTTPResponse(result)
	
	def getContentAllocations( self ):
		
		areq = ApiRequestMaker.ApiRequestMaker( self, self.apiPostURL, self.apiKey )
		return ApiResponseReader.ApiResponseReader.getDataElements( areq.fetchAllocations() )
	
	def setRawHTTPRequest(self, value):
		
		self.rawHTTPRequest = value
		
	def getRawHTTPRequest(self):
		
		return self.rawHTTPRequest
	
	def setRawHTTPResponse(self, value):
		
		self.rawHTTPResponse = value
		
	def getRawHTTPResponse(self):
		
		return self.rawHTTPResponse
	
	def extractData(self):
		
		self.verifyFetchState( self.rawHTTPResponse )
		return ApiResponseReader.ApiResponseReader.getDataElements( self.rawHTTPResponse )
			
	def verifyFetchState(self, res):
		
		if ApiResponseReader.ApiResponseReader.getResultCode( res ) > 200:
			
			self.consolePrint( "Error on fetch: " + str( ApiResponseReader.ApiResponseReader.getResultMessage( res ) ), True )

	def consolePrint(self, message, die):
		
		print message
		
		if die == True:
			
			sys.exit()
		