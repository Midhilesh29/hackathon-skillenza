import streamlit as st
import json
import pandas as pd
import numpy as np
import pydeck as pdk
from vrpsolver import VrpSolver
from route_matrix import get_distance_matrix
from preprocess_input_json import get_solution
from folium_map import get_folium_map

st.title('Route Optimization')
file_bytes = None
file_bytes = st.file_uploader("Upload a .json file", type=("json"))
if file_bytes is not None:
    file_str = file_bytes.read()
    data = json.loads(file_str)

    location_data,demand,vehicle_capacity,depot,df,lat_long,vehicle_cost = get_solution(data)

     #getting distance matrix
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
    #st.balloons()
    st.title('Result:')
    st.write(output)
    get_folium_map(df,output,lat_long,st)
