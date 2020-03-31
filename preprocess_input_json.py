import pandas as pd
from geocoding import get_lat_long


def get_solution(Input):
    print("Input:")
    print(Input)
    print("\n")
    distribution_address = []
    delivery_address = []
    demand = []
    vehicle_capacity = []
    depot = []
    vehicle_speed = []
    vehicle_cost = []
    vehicle_max_time = []
    vehicle_max_path_length = []

    for index, values in enumerate(Input['distribution_pts']):
        distribution_address.append(values['address'])
        vehicle_capacity.extend(values['vehicle_capacity'])
        vehicle_cost.extend(values['vehicle_cost'])
        vehicle_speed.extend(values['vehicle_speed'])
        vehicle_max_time.extend(values['max_time'])
        vehicle_max_path_length.extend(values['max_path_length'])
        for i in range(len(values['vehicle_capacity'])):
            depot.append(index)
        demand.append(0)
    for index, values in enumerate(Input['delivery_pts']):
        delivery_address.append(values['address'])
        demand.append(values['demand'])
    # geocoding
    distribution_address_data = get_lat_long(distribution_address)
    #delivery_address_data = get_lat_long(delivery_address)

    #'''
    #cache data

    
    distribution_address_data = {'lat_long': [[77.01372,11.02543], [77.87545,29.85297]], 
    'known_address': ['psg college of tech address avinashi rd peelamedu coimbatore tamil nadu 641004', 'iit roorkee roorkee haridwar highway roorkee uttarakhand 247667'], 
    'unknown_address': []}
    delivery_address_data = {'lat_long': [[72.91116,19.13393], [78.56615,17.57336], [77.18362,28.54057]], 
    'known_address': ['iit bombay search results main gate rd iit area powai mumbai maharashtra 400076', 'bits pilani shamirpet keesara road jawahar nagar shameerpet hyderabad telangana 500078', 'iit delhi iit campus hauz khas new delhi delhi 110016'], 
    'unknown_address': []}
    

    
    unknown_address = list()
    print("\n")
    print("distribution address:", distribution_address_data)
    print("delivery address:", delivery_address_data)
    unknown_address.extend(distribution_address_data['unknown_address'])
    unknown_address.extend(delivery_address_data['unknown_address']) 
   
    lat_long = list()
    lat_long.extend(distribution_address_data['lat_long'])
    lat_long.extend(delivery_address_data['lat_long'])
    address = []
    address.extend(distribution_address)
    address.extend(delivery_address)
    return(demand,vehicle_capacity,vehicle_speed, vehicle_max_time,vehicle_max_path_length,depot, lat_long,vehicle_cost,unknown_address,address)
