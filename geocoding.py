import requests
from json import loads
link = "https://atlas.microsoft.com/search/address/batch/sync/json?api-version=1.0&subscription-key=8WNIvZx5gvryvGYpf1ZilizJCyFa4-gTfP8tXtgQ4vA"
headers = {'Content-type': 'application/json'}


def form_query(data):
    query = {"batchItems": []}
    for address in data:
         query["batchItems"].append({"query": "?query="+address+"&limit=1"})
    return query


def get_lat_long(data):
    """
       data : list of address
    """
    query = form_query(data)
    r = requests.post(link,json=query,headers=headers)
    response = loads(r.text)
    print("geoencoding value:")
    print(response)
    print("\n")
    final_data = dict()
    final_data["lat_long"] = list()
    final_data["known_address"] = list()
    final_data["unknown_address"] = list()
    if r.status_code == 200:
        count = -1
        for batch_item in response["batchItems"]:
            count = count + 1
            if batch_item['statusCode'] == 200:
                try:
                    result = batch_item['response']['results'][0]
                except:
                    final_data["unknown_address"].append(batch_item['response']['summary']['query'])
                    continue
                final_data["lat_long"].append([result['position']["lon"],result['position']["lat"]])
                final_data["known_address"].append(batch_item['response']['summary']['query'])
            else:
                final_data["unknown_address"].append(data[count])
    return final_data
