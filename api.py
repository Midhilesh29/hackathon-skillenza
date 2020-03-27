from vrpsolver import VrpSolver
from route_matrix import get_distance_matrix
import streamlit as st
import json
import pandas as pd
import numpy as np

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

file_bytes = st.file_uploader("#Upload a JSON file", type=("json"))
file_str = file_bytes.read()
data = json.loads(file_str)
location_data,demand,vehicle_capacity,depot,df,lat_long,vehicle_cost = get_solution(data)
#Getting distance matrix
midpoint = (np.average(df['lat']), np.average(df['lon']))
st.deck_gl_chart(
            viewport={
                'latitude': midpoint[0],
                'longitude':  midpoint[1],
                'zoom': 4
            },
            layers=[{
                'type': 'ScatterplotLayer',
                'data': df.iloc[:len(data['distribution_pts']),:],
                'radiusScale': 250,
   'radiusMinPixels': 5,
                'getFillColor': [248, 24, 148],
            },
	    {
                'type': 'ScatterplotLayer',
                'data': df.iloc[len(data['distribution_pts']):,:],
                'radiusScale': 250,
   'radiusMinPixels': 5,
                'getFillColor': [0, 24, 113],
            }]
        )
distance_matrix = get_distance_matrix(location_data, len(lat_long))
data = {}
data['distance_matrix'] = distance_matrix
data['demands'] = demand
data['vehicle_capacities'] = vehicle_capacity
data['num_vehicles'] = len(vehicle_capacity)
data['depot'] = depot
data['vehicle_costs'] = vehicle_cost
#define solver with penality as 5000 and 120seconds as maximum running time
solver = VrpSolver(5000,120)
output = solver.solve(data)
st.title('Result:')
st.write(output)
