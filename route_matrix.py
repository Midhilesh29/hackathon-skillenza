import requests
from json import loads
import copy


import requests
from json import loads
import copy

link = "https://atlas.microsoft.com/route/matrix/json?subscription-key=8WNIvZx5gvryvGYpf1ZilizJCyFa4-gTfP8tXtgQ4vA&api-version=1.0&routeType=shortest"

def get_distance_matrix(location_data,len):
  r = requests.post(link,json=location_data)
  if r.status_code == 202:
    result = requests.get(r.headers['Location'])
    matrix = loads(result.text)
    #print(matrix)
    DistanceMatrix= []
    for i in range(len):
      temp = []
      for j in range(len):
        temp.append(matrix['matrix'][i][j]['response']['routeSummary']['lengthInMeters']*0.001)
      DistanceMatrix.append(copy.copy(temp))
    return DistanceMatrix
  else:
    raise ValueError(r.content)

#print(get_distance_matrix(test_data))


