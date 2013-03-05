import sys
sys.path.append('src')
import unittest

class TestSuite( unittest.TestCase ):
	
	def setUp( self):
		
		pass
	
	def tearDown( self):
		
		pass
	

	def testBuilderCharLimitation(self):
		
		import ApiBuilder
		
		limit = 128
		testString = ""
		
		for i in xrange(0,300):
			
			testString += "a"
			
		aBuilder = ApiBuilder.ApiBuilder()	
		aBuilder.builder("name", testString)
		length = len ( aBuilder.output()['name'] )
		
		self.assertEqual(limit,length)
		
	def testApiDataPacketBuilderAccuracy(self):
		
		import ApiDataPacketBuilder
		
		adp = ApiDataPacketBuilder.ApiDataPacketBuilder()
		self.assertEqual([], adp.buildDataPacket( [] ))
		
		import ApiEngagementRecord
		
		aer_list = []
		
		aer = ApiEngagementRecord.ApiEngagementRecord( "12-31-2012 12:59:59" )
		aer.contextBuilder("group", "test1")
		aer.featureBuilder("feat1", "tfeat1")
		aer.identityBuilder("ident1", "tident1")
		
		aer_list.append(aer)
		
		aer = ApiEngagementRecord.ApiEngagementRecord( "12-31-20123 12:59:59" )
		aer.contextBuilder("group", "test2")
		aer.featureBuilder("feat1", "tfeat2")
		aer.identityBuilder("ident1", "tident2")

		import ApiItemRecord
		
		item = ApiItemRecord.ApiItemRecord( "item100")
		item.builder("if1","if1_value")
		
		aer.itemsetBuilder( item )
		
		aer_list.append( aer )
		
		recs = adp.buildDataPacket( aer_list )
		
		self.assertEqual( len(aer_list), len(recs))
		self.assertEqual("test1", recs[0]['context']['group'])
		self.assertEqual("test2", recs[1]['context']['group'])
		
		self.assertEqual("tfeat2", recs[1]['features']['feat1'])
		self.assertEqual("tident1", recs[0]['identity']['ident1'])
		
		self.assertEqual(0, len( recs[0]['itemset']))
		self.assertEqual(1, len( recs[1]['itemset']))
				
		self.assertEqual("if1_value",recs[1]['itemset'][0]['features']['if1'])
		self.assertEqual("item100",recs[1]['itemset'][0]['item_id'])
		
	def testApiEngagementRecordAccuracy(self):
		
		import ApiEngagementRecord
		
		aer = ApiEngagementRecord.ApiEngagementRecord( "12-31-2012 12:59:59" )
		aer.contextBuilder("group", "test1")
		aer.featureBuilder("feat1", "tfeat1")
		aer.identityBuilder("ident1", "tident1")
		
		aer.setEngagement( "buy", 5.0)
		
		self.assertEqual( 5.0, aer.getEngagementWeight())
		self.assertEqual( "buy", aer.getEngagementType())
		
		self.assertEqual("test1", aer.getContext()['group'])
		self.assertEqual("tfeat1", aer.getFeatures()['feat1'])
		self.assertEqual("tident1", aer.getIdentity()['ident1'])
		
		import ApiItemRecord
		
		item = ApiItemRecord.ApiItemRecord( "item100")
		item.builder("if1","if1_value")
		
		aer.itemsetBuilder( item)
		
		item = ApiItemRecord.ApiItemRecord( "item200")
		item.builder("if2","if2_value")
		
		aer.itemsetBuilder( item)
		
		self.assertEqual(2, len(aer.getItemset() ) )
		
		items = aer.getItemset()
		
		self.assertEqual("item100", items[0].getItemId() )
		self.assertEqual("item200", items[1].getItemId() )
		
	def testApiItemRecordAccuracy(self):
		
		import ApiItemRecord
		
		item = ApiItemRecord.ApiItemRecord( "item100")
		item.builder("if1","if1_value")
		item.builder("if2","if2_value")
				
		self.assertEqual("item100", item.getItemId() )
		self.assertEqual("if1_value", item.output()['if1'] )
		self.assertEqual("if2_value", item.output()['if2'] )
		
	def testJSONAccuracy( self ):
		
		json_dict = {}
		json_dict['result'] = {'code':200, 'message':'test_message'}
		
		import json
		import ApiResponseReader
		
		json_string = json.dumps( json_dict )
		
		rc = ApiResponseReader.ApiResponseReader.getResultCode( json_string )
		self.assertEqual( 200, rc)
		
		rm = ApiResponseReader.ApiResponseReader.getResultMessage( json_string )
		self.assertEqual( "test_message", rm)
		
		import collections
		
		data = collections.OrderedDict()
		data = {}
		data['data'] = {}
		lst = []
		
		element1 = collections.OrderedDict()
		element2 = collections.OrderedDict()
		
		element1['item_id'] = 'item100'
		element1['n1'] = "1"
		element1['n2'] = "2"
		element1['n3'] = "3"
		
		element2['item_id'] = 'item200'
		element2['n1'] = "4"
		element2['n2'] = "5"
		element2['n3'] = "6"
		
		lst.append( element1 )
		lst.append( element2 )
		
		data['data']['list'] = lst
		
		json_data = json.dumps( data )
				
		recs = ApiResponseReader.ApiResponseReader.getDataElements( json_data )
		
		self.assertEquals('1', recs[0]['n1'])
		
	def testFetchRecommendations(self):
		
		import ApiSession

		apiKey = "aaaaa"
		url = "https://api.perceptlink.com/api/1/test/ok_fetch_recommendations";

		aso = ApiSession.ApiSession( apiKey, url)
		aso.getItemRecommendations()

		recs =  aso.extractData()
		
		self.assertEquals(3, len(recs) )
		self.assertEquals(200, recs[1]['item_id'])
		self.assertEquals("Z", recs[2]['recommendations'][1])
		self.assertEquals("A", recs[0]['recommendations'][0])
		
	def testFetchRecommendation(self):
		
		import ApiSession
		import ApiSingletonRequest
		
		apiKey = "apiKey";
		url = "https://api.perceptlink.com/api/1/test/ok_fetch_recommendation";
		
		singleton = ApiSingletonRequest.ApiSingletonRequest()
		singleton.builder("item_id", 150)
		
		aso = ApiSession.ApiSession("apikey", url);
		aso.getItemRecommendation( singleton );
		
		data = aso.extractData()
				
		self.assertEquals( 150, data[0]['item_id'])
		
	def testFetchAllocations(self):
		
		import ApiSession
				
		apiKey = "apiKey";
		url = "https://api.perceptlink.com/api/1/test/ok_fetch_allocations";
				
		aso = ApiSession.ApiSession("apikey", url);
		aso.getContentAllocations( );
		
		data = aso.extractData()
				
		self.assertEquals( "sg", data[0]['group'])
		self.assertEquals( 0.46, data[2]['allocation'])
		
	def testFetchAllocation(self):
		
		import ApiSession
		import ApiSingletonRequest
		
		apiKey = "apiKey";
		url = "https://api.perceptlink.com/api/1/test/ok_fetch_allocation";
		
		singleton = ApiSingletonRequest.ApiSingletonRequest()
		singleton.builder("group", "sg")
		
		aso = ApiSession.ApiSession("apikey", url);
		aso.getContentAllocation( singleton );
		
		data = aso.extractData()
				
		self.assertEquals( "sg", data[0]['group'])
		
	def testFetchLastRecordSubmitted(self):
		
		import ApiSession
		
		url = "https://api.perceptlink.com/api/1/test/ok_last_record_submitted";
				
		aso = ApiSession.ApiSession( "api", url);
		
		lRecord = aso.fetchLastEngagementRecordSubmitted()
		data = aso.extractData()
		context = data[0]['context']
				
		self.assertEquals( context['group'], "sg");
		self.assertEquals( 1, len(data))
		
if __name__ == '__main__':
	
	unittest.main()
		
