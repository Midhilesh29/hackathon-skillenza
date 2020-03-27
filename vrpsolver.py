

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class VrpSolver():
    def __init__(self, penality=1000, maxRunningTime=30):

        '''
        penality (type:int, default:1000)
        --------------------------------
        If solution doesn't exist, then some of the distination should be left.
        While leaving those destination penality will be added to the objective function.
        If penality is high, lesser distinations will be left, else more distinations will be left off.

        maxRunningTime (type:int, default:30seconds)
        -------------------------------------
        If optimization takes very long amount of time, then it will be killed after exceeding maxRunningTime (in seconds) 
        '''
        self.penality = penality
        self.maxRunningTime = maxRunningTime

    def print_solution(self,data, manager, routing, solution):
        """Prints solution on console."""
        total_distance = 0
        total_load = 0
        json_data={"vehicle":{}}
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            route_load = 0
            vehicle_number = 'v'+str(vehicle_id)
            json_data['vehicle'][vehicle_number] = {}
            json_data['vehicle'][vehicle_number]['route_path'] = []
            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                json_data['vehicle'][vehicle_number]['route_path'].append(node_index)
                route_load += data['demands'][node_index]
                plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
            json_data['vehicle'][vehicle_number]['route_distance'] = route_distance
            json_data['vehicle'][vehicle_number]['route_load'] = route_load
            plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                    route_load)
            json_data['vehicle'][vehicle_number]['route_path'].append(manager.IndexToNode(index))
            plan_output += 'Distance of the route: {}km\n'.format(route_distance)
            plan_output += 'Load of the route: {}\n'.format(route_load)
            print(plan_output)
            total_distance += route_distance
            total_load += route_load
        json_data['Total_distance'] = total_distance
        json_data['Total_load'] = total_load
        print('Total distance of all routes: {}m'.format(total_distance))
        print('Total load of all routes: {}'.format(total_load))
        return json_data
    

    '''
    def solve(self, distanceMatrix, demandVector, depot, vehicleCapacityAtEachDepot)
    '''

    def solve(self,data):
        """Solve the CVRP problem."""
        # Instantiate the data problem.

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                            data['num_vehicles'], data['depot'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)


        # Create and register a transit callback.
        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


        # Add Capacity constraint.
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = manager.IndexToNode(from_index)
            return data['demands'][from_node]

        demand_callback_index = routing.RegisterUnaryTransitCallback(
            demand_callback)
        routing.AddDimensionWithVehicleCapacity(
            demand_callback_index,
            0,  # null capacity slack
            data['vehicle_capacities'],  # vehicle maximum capacities
            True,  # start cumul to zero
            'Capacity')

        for node in range(1, len(data['distance_matrix'])):
            routing.AddDisjunction([manager.NodeToIndex(node)], self.penality)

        # Setting first solution heuristic.


        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.time_limit.seconds = self.maxRunningTime
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        '''
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        '''


        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            json_data = self.print_solution(data, manager, routing, solution)
            print("\nJSON Data:")
            print(json_data)
            return(json_data)
        else:
            print("Solution doesn't exist")
