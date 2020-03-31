# Hackathon-skillenza
Project designes by team MathGuys
Harish
Midhilesh
# Route Optimization and visualizating sales vehicles
Route Optimization is a NP hard integer programming problem. Finding a near optimial solution for route optimization technique is very useful for delivery and transportation companies to save more money and time with goods delivered to all the places.

The project we developed tries to minimize the total route distance + cost of picking each vehicle + time taken to complete the route by chosing optimal vehicles with constrains that each vehicle has it's own maximum travel distance, maximum time taken to complete a ride and multiple delivery points. We used branch and bound optimization technique to solve this problem. Hence we used CBC tool with Google OR-tool python wraper to find the optimal solution.

We developed this as an API which gets input in the form of JSON and receives an Output in the form of JSON. The input and output JSON structure were discussed below:

## Input JSON structure
```
{
"distribution_pts":[
   {
   "address": #Location address of distribution point (data type: string),
   "vehicle_capacity": #Contains the capacity of all the vehicles present in the distribution point (data type: list),
   "vehicle_costs": #Contains the cost of each vehicle (i.e cost of diesel needed for each vehicle to cover 1Km) (data type: list),
   "vehicle_speed": #Contains the speed of each vehicles in (Km/hr) (data type:list),
   "max_time": #Contains the maxiumum time a vehicle can travel,(data type:list)
   "max_path_length": #Contains maximum distance a vehicle can travel (data type:list)
   }
   ]
   "delivery_pts":[
   {
   "address": #Location address of distribution point (data type: string),
   "demand": #Demand needed at each location (data type:float or int)
   }
   ]
}
```

## Output JSON structure
```
{'vehicle': 
 {'v0': 
  {'route_path': #Contains the delivery points and distribution points present in this vehicle route, 
  'distance': #Contains the pair wise distance between each point present in this vehicle route, 
  'capacity': #Contains the capacity of this vehicle, 
  'cost': #Contains the cost of each vehicle (i.e cost of diesel needed for each vehicle to cover 1Km), 
  'demand': #Contains demand for each points present in the route, 
  'route_load': #Total load carried by this vehicle on this route, 
  'route_distance': #Total distance Covered by thix vehicle,
  'travel_time': #Time taken by this vehicle to complete this route (route path)}, 
  'Total_distance': #Total distance travelled by all the vehicles present in the distribution points, 
  'Total_load': #Total load carried by all the vehiles present in the distribution points}
  }
 }
}
```
There will a option for downloading the output map. The downloaded map contains the detailed visualization of generated optimzal path.

# Azure Technologies
1) Azure maps
  a) Azure geocoding API
  b) Azure distancematrix API
2) WebApps

# Language and libraries
1) Streamlit - UI
2) Folium - Map generation using OpenStreetMap
3) Google OR-tools - Tool for optimization
4) CBC tool - Tool for branch and bound tool

# How to use this code
