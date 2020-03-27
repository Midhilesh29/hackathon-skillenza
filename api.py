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
    df = pd.DataFrame(lat_long, columns = ['lon', 'lat'])
    return(location_data,demand,vehicle_capacity,depot,df,lat_long)

file_bytes = st.file_uploader("#Upload a JSON file", type=("json"))
file_str = file_bytes.read()
data = json.loads(file_str)
location_data,demand,vehicle_capacity,depot,df,lat_long = get_solution(data)
#Getting distance matrix
df
midpoint = (np.average(df['lat']), np.average(df['lon']))
st.deck_gl_chart(
            viewport={
                'latitude': midpoint[0],
                'longitude':  midpoint[1],
                'zoom': 4
            },
            layers=[{
                'type': 'ScatterplotLayer',
                'data': df,
                'radiusScale': 250,
   'radiusMinPixels': 5,
                'getFillColor': [248, 24, 148],
            }]
        )
distance_matrix = get_distance_matrix(location_data, len(lat_long))
data = {}
data['distance_matrix'] = distance_matrix
data['demands'] = demand
data['vehicle_capacities'] = vehicle_capacity
data['num_vehicles'] = len(vehicle_capacity)
data['depot'] = depot
#define solver with penality as 5000 and 120seconds as maximum running time
#solver = VrpSolver(5000,120)
#output = solver.solve(data)
#st.write('Result `%s`' % json.dumps(output))
