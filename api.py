import streamlit as st
import json
import pandas as pd
import numpy as np
import pydeck as pdk
from vrpsolver import VrpSolver
from route_matrix import get_distance_matrix
from preprocess_input_json import get_solution
from folium_map import get_folium_map
from math import radians, cos, sin, asin, sqrt
from userexception import NoSolution

def haversine(lon1, lat1 , lon2, lat2):
     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
     dlon = lon2 - lon1 
     dlat = lat2 - lat1 
     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
     c = 2 * asin(sqrt(a)) 
     r = 6371 # Radius of earth in kilometers. Use 3956 for miles
     return c * r

st.title('Route Optimization')

file_bytes = None
file_bytes = st.file_uploader("Upload a .json file", type=("json"))

if(file_bytes is not None):
     file_str = file_bytes.read()
     Inputdata = json.loads(file_str)

     demand, vehicle_capacity, vehicle_speed, vehicle_max_running_time, vehicle_max_path_length, depot, lat_long, vehicle_cost, unknown_address = get_solution(Inputdata)

     if(len(unknown_address)>0):
          st.info('Address shown below are not found!')
          st.write(unknown_address)
     else:
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
          distance_matrix = get_distance_matrix(location_data, len(lat_long))

          '''
          cache Data:

          
          distance_matrix = [[1.655,2426.973,1188.234,871.528,2276.26],
          [2426.685,0.0,1493.191,1604.636,180.83700000000002],
          [1190.011,1486.967,0.0,701.855,1332.884],
          [872.38,1579.133,702.914,0.126,1448.003],
          [2267.602,180.776,1327.406,1465.724,0.0]] 
          '''



          for i in range(len(lat_long)):
               for j in range(len(lat_long)):
                    print(distance_matrix[i][j],end=" ")
               print("\n")
          data = {}
          data['distance_matrix'] = distance_matrix
          data['demands'] = demand
          data['vehicle_capacities'] = vehicle_capacity
          data['vehicle_speed'] = vehicle_speed
          data['num_vehicles'] = len(vehicle_capacity)
          data['depot'] = depot
          data['vehicle_costs'] = vehicle_cost
          data['vehicle_max_running_time'] = vehicle_max_running_time
          data['vehicle_max_path_length'] = vehicle_max_path_length

          #define solver with penality as 5000 and 120seconds as maximum running time
          solver = VrpSolver(5000,120)
          try:
               output = solver.solve(data)
               st.title('Result:')
               st.write(output)
          except NoSolution as error:
               st.write("Solution not found")
          #st.balloons()
          get_folium_map(df,output,lat_long,st)
          
          
