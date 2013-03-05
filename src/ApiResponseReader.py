
import json


class ApiResponseReader:
	
	def __init__(self):
		
		pass
	
	@staticmethod
	def getResultCode( json_string ):
		
		rs = ApiResponseReader.parseResultMessage( json_string, "result", "code")
		
		if rs == None:
			
			return 600
		
		return int( rs )
	
	@staticmethod
	def getResultMessage( json_string ):
		
		return ApiResponseReader.parseResultMessage( json_string, "result", "message")
	
	@staticmethod	
	def getDataElements( json_string ):
		
		dat = ApiResponseReader.parseResultMessage( json_string, "data", "list" )
		
		if dat == None:
			
			return []
		
		return dat
	
	@staticmethod
	def parseResultMessage( json_string, top, name):
		
		vals = json.loads( json_string)
		
		if vals.has_key(top) == True:
			
			if vals[top].has_key(name) == True:
				
				return vals[top][name]
			
		return None