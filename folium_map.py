import folium
import numpy as np
import pandas as pd
from IPython.display import display
from collections import namedtuple# using omaha coordinates
import base64
import codecs
import json
import random
from uuid import uuid4
f = open('colors.json',)
color_list = list(json.load(f))

def get_arrows(locations, color='red', size=4, n_arrows=3):
    
    '''
    Get a list of correctly placed and rotated 
    arrows/markers to be plotted
    
    Parameters
    locations : list of lists of lat lons that represent the 
                start and end of the line. 
                eg [[41.1132, -96.1993],[41.3810, -95.8021]]
    arrow_color : default is 'blue'
    size : default is 6
    n_arrows : number of arrows to create.  default is 3    Return
    list of arrows/markers
    '''
    
    Point = namedtuple('Point', field_names=['lat', 'lon'])
    
    # creating point from our Point named tuple
    p1 = Point(locations[0][0], locations[0][1])
    p2 = Point(locations[1][0], locations[1][1])
    
    # getting the rotation needed for our marker.  
    # Subtracting 90 to account for the marker's orientation
    # of due East(get_bearing returns North)
    rotation = get_bearing(p1, p2) - 90
    
    # get an evenly space list of lats and lons for our arrows
    # note that I'm discarding the first and last for aesthetics
    # as I'm using markers to denote the start and end
    arrow_lats = np.linspace(p1.lat, p2.lat, n_arrows + 2)[1:n_arrows+1]
    arrow_lons = np.linspace(p1.lon, p2.lon, n_arrows + 2)[1:n_arrows+1]
    
    arrows = []
    
    #creating each "arrow" and appending them to our arrows list
    for points in zip(arrow_lats, arrow_lons):
        arrows.append(folium.RegularPolygonMarker(location=points, 
                      fill_color=color, number_of_sides=3, 
                      radius=size, rotation=rotation))
    return arrows


def get_bearing(p1, p2):
    
    '''
    Returns compass bearing from p1 to p2
    
    Parameters
    p1 : namedtuple with lat lon
    p2 : namedtuple with lat lon
    
    Return
    compass bearing of type float
    
    Notes
    Based on https://gist.github.com/jeromer/2005586
    '''
    
    long_diff = np.radians(p2.lon - p1.lon)
    
    lat1 = np.radians(p1.lat)
    lat2 = np.radians(p2.lat)
    
    x = np.sin(long_diff) * np.cos(lat2)
    y = (np.cos(lat1) * np.sin(lat2) 
        - (np.sin(lat1) * np.cos(lat2) 
        * np.cos(long_diff)))    
    bearing = np.degrees(np.arctan2(x, y))
    
    # adjusting for compass bearing
    if bearing < 0:
        return bearing + 360
    return bearing


def get_folium_map(df,output,lat_long,st):
    midpoint = (np.average(df['lat']), np.average(df['lon']))
    center_lat = midpoint[0]
    center_lon = midpoint[1]
    some_map = folium.Map(location=[center_lat, center_lon], zoom_start=7)
    
    arrows = []
    for vehicle_id in output['vehicle'].keys():
        route_len = len(output['vehicle'][vehicle_id]['route_path'])
        count = random.randint(0,17)
        if route_len <= 2:
            loc = lat_long[output['vehicle'][vehicle_id]['route_path'][0]]
            loc = [loc[1],loc[0]]
            folium.CircleMarker(location=loc,radius=7,icon=folium.Icon(color=color_list[count]), popup="Distribution_point").add_to(some_map)
            continue
        loc = lat_long[output['vehicle'][vehicle_id]['route_path'][0]]
        folium.CircleMarker(location=loc,radius=7,icon=folium.Icon(color=color_list[count]), popup ="Distribution_point").add_to(some_map)
        loc2 = lat_long[output['vehicle'][vehicle_id]['route_path'][1]]
        loc_p = [loc,loc2]
        folium.PolyLine(locations=loc_p, color=color_list[count]).add_to(some_map)
        arrows.extend(get_arrows(locations=loc_p, n_arrows=2))
        for route_path_index in range(1,len(output['vehicle'][vehicle_id]['route_path'])-1):
            loc = lat_long[output['vehicle'][vehicle_id]['route_path'][route_path_index]]
            folium.Marker(location=loc,icon=folium.Icon(color=color_list[count]),popup="Delivery point").add_to(some_map)
            loc2 = lat_long[output['vehicle'][vehicle_id]['route_path'][route_path_index+1]]
            loc_p = [loc,loc2]
            folium.PolyLine(locations=loc_p, color=color_list[count]).add_to(some_map)	
            arrows.extend(get_arrows(locations=loc_p, n_arrows=2))
    for arrow in arrows:
        arrow.add_to(some_map)
    fname = str(uuid4())+".html"
    some_map.save(fname)
    f=codecs.open(fname, 'r')
    b64 = base64.b64encode(f.read().encode()).decode()
    st.info('Download and open the Map (HTML file) in a browser')
    st.markdown('<a href="data:@file/html;base64,{}" download="map.html">Download the Map</a>'.format(b64), unsafe_allow_html=True)
    

