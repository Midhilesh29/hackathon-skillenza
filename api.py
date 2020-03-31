import streamlit as st
import json
import pandas as pd
import numpy as np
import pydeck as pdk
from vrpsolver import VrpSolver
from route_matrix import get_distance_matrix
from preprocess_input_json import get_solution
from folium_map import get_folium_map
from userexception import NoSolution
import matplotlib.pyplot as plt


def get_uncovered_delivery(out,address,del_len):
    node = []
    for v_id in out['vehicle']:
    	node.extend(out['vehicle'][v_id]['route_path'][1:-1])
    node = set(node)
    all_del = list(range(del_len-1, len(address)))
    return list(set(all_del) - set(node))
    

st.title('Vehicle Route Optimization')
st.markdown('Welcome to mathguys Vehicle Route Optimization website. Github link: <a href="https://github.com/harish-ganesh/hackathon-skillenza">routeoptim</a>', unsafe_allow_html=True)
file_bytes = None
file_bytes = st.file_uploader("Upload a .json file", type=("json"))
if st.checkbox("Show input JSON structure"):
    temp_json = {
	"distribution_pts":[
		   {
		   "address": "",#Location address of distribution point (data type: string)
		   "vehicle_capacity": [],#Contains the capacity of all the vehicles present in the distribution point(data type: list of numbers) 
		   
		   "vehicle_costs": [],#Contains the cost of each vehicle (i.e cost of diesel needed for each vehicle to cover 1Km) (data type: list)
		  
		   "vehicle_speed": [],#Contains the speed of each vehicles in (Km/hr) (data type:list)
		   "max_time": [],#Contains the maxiumum time a vehicle can travel,(data type:list)
		   "max_path_length": []#Contains maximum distance a vehicle can travel (data type:list)
		   }
	   ],
	   "delivery_pts":[
		   {
		   "address": "",#Location address of distribution point (data type: string)
		   "demand": 2#Demand needed at each location (data type:float or int)
		   }
	   ]
}
    st.json(temp_json)
if(file_bytes is not None):
     file_str = file_bytes.read()
     Inputdata = json.loads(file_str)

     demand, vehicle_capacity, vehicle_speed, vehicle_max_running_time, vehicle_max_path_length, depot, lat_long, vehicle_cost, unknown_address, address, del_len = get_solution(Inputdata)

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
               #st.title('Result:')
               #st.write(output)
               uncov_del = get_uncovered_delivery(output,address,del_len)
               get_folium_map(address,output,lat_long,st,uncov_del)
               #st.write(address[uncov_del[0]])

               labels = ['Covered Delivery Points', 'Uncovered Delivery Points']
               sizes = [len(address)-len(uncov_del), len(uncov_del)]
               explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
               fig1, ax1 = plt.subplots()
               ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
	        shadow=False, startangle=90)
               ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

               st.pyplot()
               #st.success("Total delivery points:"+str(len(demand))+"Covered delivery points:"+str(len(address)-len(uncov_del)))
               
               
          except NoSolution as error:
               st.write("Solution not found")
          #st.balloons()
          
          
          
