from vrpsolver import VrpSolver
from route_matrix import get_distance_matrix

def get_solution(Input):
  lat_long=[]
  demand = []
  vehicle_capacity = []
  depot = []
  for index, values in enumerate(Input['distribution_pts']):
    lat_long.append(values['coordinates'])
    depot.append(index)
    vehicle_capacity.extend(values['vehicle_capacity'])
  for index, values in enumerate(Input['delivery_pts']):
    lat_long.append(values['coordinates'])
    demand.append(values['demand'])
  
  #Structure for getting distance data using azure map
  location_data={
    "origins":{
      "type":"MultiPoint",
      "coordinates":lat_long
    },
    "destinations":{
      "type":"MultiPoint",
      "coordinates":lat_long
    }
  }

  #Getting distance matrix
  distance_matrix = get_distance_matrix(location_data)


  data={}
  data['distance_matrix'] = distance_matrix
  data['demands'] = demand
  data['vehicle_capacities'] = vehicle_capacity
  data['num_vehicles'] = len(vehicle_capacity)
  data['depot'] = depot

  #define solver with penality as 5000 and 120seconds as maximum running time
  solver = VrpSolver(5000,120)
  output = solver.solve(data)
  return output
      

