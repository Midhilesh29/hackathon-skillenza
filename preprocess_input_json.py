import pandas as pd

def get_solution(Input):
    lat_long=[]
    demand = []
    vehicle_capacity = []
    depot = []
    vehicle_cost = []
    for index, values in enumerate(Input['distribution_pts']):
        lat_long.append(values['coordinates'])
        vehicle_capacity.extend(values['vehicle_capacity'])
        vehicle_cost.extend(values['vehicle_cost'])
        for i in range(len(values['vehicle_capacity'])):
            depot.append(index)
        demand.append(0)
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
    df = pd.DataFrame(lat_long, columns = ['lon', 'lat'])
    return(location_data,demand,vehicle_capacity,depot,df,lat_long,vehicle_cost)
