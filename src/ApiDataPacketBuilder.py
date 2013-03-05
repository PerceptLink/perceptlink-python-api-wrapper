
import collections

class ApiDataPacketBuilder:
	
	def __init__(self):
		
		pass
	
	def buildDataPacket( self, recs ):
		
		dataMap = []
		
		for r in recs:
			
			new_rec = collections.OrderedDict()
			chrono = collections.OrderedDict()
			engagement = collections.OrderedDict()
			
			chrono['occurred'] = r.getDate()
			engagement['type'] = r.getEngagementType()
			engagement['weight'] = r.getEngagementWeight()
			
			new_rec['chrono'] = chrono
			new_rec['engagement'] = engagement
			new_rec['identity'] = r.getIdentity()
			new_rec['context'] = r.getContext()
			new_rec['features'] = r.getFeatures()
			new_rec['itemset'] = []
			
			itemset = []
			
			for i in r.getItemset():
				
				itemInfo = collections.OrderedDict()
				itemInfo['item_id'] = i.getItemId()
				itemInfo['features'] = i.output()
				
				itemset.append(itemInfo)
			
			new_rec['itemset'] = itemset
			
			dataMap.append( new_rec )
			
		return dataMap
			
		
		