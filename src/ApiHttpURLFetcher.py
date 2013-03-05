
import urllib2

class ApiHttpURLFetcher:
	
	def __init__(self, user_agent, timeout, method):
		
		self.userAgent = user_agent
		self.timeout = timeout
		self.method = method
		self.responseCode = 600
		self.content = None
		
	def getContent(self):
		
		return self.content
	
	def getResponseCode(self):
		
		return self.responseCode
	
	def getSuccessState( self ):
		
		if (self.responseCode < 400):
			
			return True
		
		return False
	
	def initialize(self):
		
		self.content = None
		self.responseCode = 600
	
	def fetchContent(self, url, content_type):
		
		self.fetchURL( url, content_type)
			
	def postData( self, url, contentType, request ):
		
		self.initialize()
		
		try:
						
			headers = {'User-Agent' : self.userAgent, 'Content-Type' : contentType}
			req = urllib2.Request( url, request, headers )
			resp = urllib2.urlopen( req )
			self.content = resp.read()
			
		except urllib2.HTTPError as e:
			
			print "Request Failed"
			print "Code: " + str(e)
			
		except urllib2.URLError as e:
			
			print "Server unavailable"
			print "More: " + str(e)
			
		except Exception as e:
			
			print "Other error"
			print "More: " + str(e)
			
	def fetchURL( self, url, contentType):
		
		pass
		
		
		
		
	
