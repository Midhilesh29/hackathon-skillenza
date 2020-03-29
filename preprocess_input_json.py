import pandas as pd
from geocoding import get_lat_long


def get_solution(Input):
    distribution_address = []
    delivery_address = []
    demand = []
    vehicle_capacity = []
    depot = []
    vehicle_cost = []
    for index, values in enumerate(Input['distribution_pts']):
        distribution_address.append(values['address'])
        vehicle_capacity.extend(values['vehicle_capacity'])
        vehicle_cost.extend(values['vehicle_cost'])
        for i in range(len(values['vehicle_capacity'])):
            depot.append(index)
        demand.append(0)
    for index, values in enumerate(Input['delivery_pts']):
        delivery_address.append(values['address'])
        demand.append(values['demand'])
    # geocoding
    distribution_address_data = get_lat_long(distribution_address)
    delivery_address_data = get_lat_long(delivery_address)

    unknown_address = list
    unknown_address.append(distribution_address_data['unknown_address'])
    unknown_address.append(delivery_address_data['unknown_address']) 
   
    lat_long = list()
    lat_long.extend(distribution_address_data['lat_long'])
    lat_long.extend(delivery_address_data['lat_long'])
	
    return(demand,vehicle_capacity,depot,lat_long,vehicle_cost,unknown_address)
