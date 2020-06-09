from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices


landmark_string = ""
for landmark in landmark_choices:
    landmark_string+= f" '{landmark}' for {landmark_choices[landmark]}\n"

stations_under_construction = ['Gilmore',]



# print(landmark_string)

def greet():
    print("Hi there and welcome to SkyRoute!")
    print("We'll help you find the shortest route between the following Vancouver landmarks:\n" + landmark_string)

def skyroute():
    greet()
    new_route()
    goodbye()


def get_active_stations():
    updated_metro = vc_metro
    for station_under_construction in stations_under_construction:
        for current_station,neighboring_stations in vc_metro.items():
            if current_station != station_under_construction:
                 updated_metro[current_station] -= set(stations_under_construction)
            else:
                updated_metro[current_station] = set([])
    return updated_metro


def set_start_and_end(start_point,end_point):
    if start_point is not None:
        change_point = input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both': ")   
        if change_point == "b":
            start_point = get_start()
            end_point = get_end()
        elif change_point == "o":
            start_point = get_start()
        elif change_point == "d":
            end_point = get_end()
        else:
            print("Oops look like you have ntered an incorrect value")
            set_start_and_end(start_point,end_point)
        
    else:
        start_point = get_start()
        end_point = get_end()
    if start_point==end_point:
        print("You should just walk lol, please enter appropriate station next time")
        return set_start_and_end(start_point,end_point)

    return start_point, end_point



def get_start():
    start_point_letter = input("Where you coming from bud\n")
    if start_point_letter  in landmark_choices:
        start_point = landmark_choices[start_point_letter]
        return start_point
    else:
        print("Sorry we dont't have that landmark, please enter other\n")
        return get_start()

def get_end():
    end_point_letter = input("Where you heading to bud\n")
    if end_point_letter  in landmark_choices:
        end_point = landmark_choices[end_point_letter]
        return end_point
    else:
        print("Sorry we dont't have that landmark, please enter other\n")
        get_end()

# skyroute()
# print(set_start_and_end(None,None))

def new_route(start_point= None, end_point = None):
    start_point,end_point = set_start_and_end(start_point,end_point)
    shortest_route = get_route(start_point,end_point)
    if shortest_route:
        shortest_route_string = "\n".join(shortest_route)
        print("The shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
    
    else:
        print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
    
    again = input("\nWould you like to see another route? Enter y/n: ")
    if again =="y":
        show_landmarks()
        new_route(start_point,end_point)

def show_landmarks():
    see_landmarks = input("Would you want to see list of landmarks again. Enter y/n: \n")
    if see_landmarks == "y":
        print(landmark_string)

def get_route(start_point,end_point):
    start_stations = vc_landmarks[start_point]
    end_stations = vc_landmarks[end_point]
    routes = []
    for start_station in start_stations:
        for end_station in end_stations:
            metro_system = get_active_stations() if stations_under_construction else vc_metro
            if stations_under_construction:
                possible_route = dfs(metro_system,start_station,end_station)
                if not possible_route:
                    return None
            route = bfs(metro_system,start_station,end_station)
            if route:
                routes.append(route)
    shortest_route  = min(routes,key= len)
    return shortest_route
def goodbye():
    print("Thanks for using skyroute, hope to see you again. \nGodspeed\n")
skyroute()
