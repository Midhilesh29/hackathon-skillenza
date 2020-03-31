import requests
from json import loads
import copy
from math import radians, cos, sin, asin, sqrt

link = "https://atlas.microsoft.com/route/matrix/json?subscription-key=8WNIvZx5gvryvGYpf1ZilizJCyFa4-gTfP8tXtgQ4vA&api-version=1.0&routeType=shortest"

def haversine(lon1, lat1 , lon2, lat2):
     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
     dlon = lon2 - lon1 
     dlat = lat2 - lat1 
     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
     c = 2 * asin(sqrt(a)) 
     r = 6371 # Radius of earth in kilometers. Use 3956 for miles
     return c * r

def get_distance_matrix(location_data,len):
  r = requests.post(link,json=location_data)
  if r.status_code == 202:
    result = requests.get(r.headers['Location'])
    matrix = loads(result.text)
    print(matrix)
    DistanceMatrix= []
    
    for i in range(len):
      temp = []
      for j in range(len):
        if matrix['matrix'][i][j]['statusCode'] == 200:
            temp.append(matrix['matrix'][i][j]['response']['routeSummary']['lengthInMeters']*0.001)
        else:
            distance = haversine(location_data["origins"]["coordinates"][i][0],location_data["origins"]["coordinates"][i][1],location_data["destinations"]["coordinates"][j][0],location_data["destinations"]["coordinates"][j][1])
            temp.append(distance)
      DistanceMatrix.append(copy.copy(temp))
    return DistanceMatrix
  else:
    raise ValueError(r.content)

#print(get_distance_matrix(test_data))


