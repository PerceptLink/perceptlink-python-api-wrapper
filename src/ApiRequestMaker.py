
import collections
import json
import ApiHttpURLFetcher

class ApiRequestMaker:
	
	def __init__(self, aso, url, apiKey):
		
		self.aso = aso
		self.url = url
		self.apiKey = apiKey
		self.default_user_agent = "Python Wrapper v1"
		self.default_timeout = 5000
		self.contentType = "application/json"
		
	def fetchRecommendation(self, req):
		
		request = self.buildSingletonRequest( "fetch_recommendation" , req)
		return self.doFetch( request )
	
	def fetchRecommendations(self):
		
		request = self.buildRequest( "fetch_recommendations" )
		return self.doFetch( request )
	
	def fetchAllocation(self, req):
		
		request = self.buildSingletonRequest( "fetch_allocation" , req)
		return self.doFetch( request )

	def fetchAllocations(self):
		
		request = self.buildRequest( "fetch_allocations" )
		return self.doFetch( request )
	
	def fetchLastEngagementRecordSubmitted( self):
		
		request = self.buildRequest( "last_engagement_record_submitted" )
		return self.doFetch( request )
	
	def postData(self, data):
		
		request = self.buildPostDataRequest( "post_event_data", data)
		return self.doFetch( request )
	
	def doFetch(self, request):
		
		self.aso.setRawHTTPRequest( request )
		uf = ApiHttpURLFetcher.ApiHttpURLFetcher( self.default_user_agent, self.default_timeout, "POST")
		uf.postData( self.url, self.contentType, request )
		res = uf.getContent()
		self.aso.setRawHTTPResponse( res )
		return res
	
	def buildRequest( self, r_type ):
		
		header = collections.OrderedDict()
		header['api_key'] = self.apiKey
		header['type'] = r_type
		
		return json.dumps( header )
	
	def buildSingletonRequest( self, r_type, criteria ):
		
		header = collections.OrderedDict()
		header['api_key'] = self.apiKey
		header['type'] = r_type
		header['criteria'] = criteria
		
		return json.dumps( header )
	
	def buildPostDataRequest(self, r_type, data):
		
		header = collections.OrderedDict()
		header['api_key'] = self.apiKey
		header['type'] = r_type
		header['data'] = data
		
		return json.dumps( header )
	

		