from vrpsolver import VrpSolver
from route_matrix import get_distance_matrix

location_data = {
  "origins": {
    "type": "MultiPoint",
    "coordinates": [[72.849998,19.155001],
                    [73.055,24.7945],
                    [80.949997,26.85],
                    [72.877426,19.07609],
                    [75.040298,14.16704],
                    [88.719391,26.540457],
                    [87.849251,24.633568],
                    [74.493011,28.440554],
                    [72.858894,24.882618],
                    [74.556374,16.779877],
                    [77.281296,12.715035],
                    [77.727478,13.432515],
                    [77.208946,12.651805],
                    [71.637077,22.728392],
                    [76.574059,9.383452],
                    [75.621788,14.623801],
                    [79.838005,10.92544]]
  },
  "destinations": {
    "type": "MultiPoint",
    "coordinates": [[72.849998,19.155001],
                    [73.055,24.7945],
                    [80.949997,26.85],
                    [72.877426,19.07609],
                    [75.040298,14.16704],
                    [88.719391,26.540457],
                    [87.849251,24.633568],
                    [74.493011,28.440554],
                    [72.858894,24.882618],
                    [74.556374,16.779877],
                    [77.281296,12.715035],
                    [77.727478,13.432515],
                    [77.208946,12.651805],
                    [71.637077,22.728392],
                    [76.574059,9.383452],
                    [75.621788,14.623801],
                    [79.838005,10.92544]]
  }
}

if __name__ == '__main__':
    distance_matrix = get_distance_matrix(location_data)
    if(len(distance_matrix)>0):
        print("Got Distance matrix")
    else:
        print("error is fetching data from azure maps")
    demand = [0, 1, 1, 2, 4, 2, 4, 8, 8, 1, 2, 1, 2, 4, 4, 8, 8]
    vehicle_capacity = [20, 5, 15,15,15]
    num_vehicles = len(vehicle_capacity)
    depot = [1,1,2,15,16]
    
    data={}
    data['distance_matrix'] = distance_matrix
    data['demands'] = demand
    data['vehicle_capacities'] = vehicle_capacity
    data['num_vehicles'] = num_vehicles
    data['depot'] = depot

    solver = VrpSolver(5000,120)
    solver.solve(data)
