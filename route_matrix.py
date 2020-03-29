import requests
from json import loads
import copy


link = "https://atlas.microsoft.com/route/directions/batch/sync/json?api-version=1.0&subscription-key=8WNIvZx5gvryvGYpf1ZilizJCyFa4-gTfP8tXtgQ4vA"
headers = {'Content-type': 'application/json'}

def form_query(data):
    query = {"batchItems": []}
    for lat_long_pair in data:
         query["batchItems"].append({"query": "?query="+str(lat_long_pair[0][0])+','+str(lat_long_pair[0][1])+':'+str(lat_long_pair[1][0])+','+str(lat_long_pair[1][1])+"&travelMode=truck&routeType=shortest&traffic=false"})
    return query

def get_distance_matrix(data,):
    query = form_query(data)
    r = requests.post(link,json=query,headers=headers)
    response = loads(r.text)
    final_data = dict()
    final_data["distance"] = list()
    if r.status_code == 200:
        for batch_item in response["batchItems"]:
            if batch_item['statusCode'] == 200:
                try:
                    final_data["distance"].append(batch_item['response']['routes'][0]['summary']["lengthInMeters"])
                except:
                    final_data["distance"].append(None)
                    continue
            else:
                final_data["distance"].append(None)
    return final_data

test_data = [
	[[47.639987,-122.128384],[47.621252,-122.184408]],
        [[47.639987,-122.128384],[47.621252,-1000.184408]]
	]

print(get_distance_matrix(test_data))


