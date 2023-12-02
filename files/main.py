import paho.mqtt.client as mqtt
import random as rd
import time
import math

#Random Number generator below
'''
mqtt_publish_topic = "group4/test/py"
mqtt_broker_address = "wi-vm162-01.rz.fh-ingolstadt.de"
mqtt_broker_port = 1870

def PrintRandomNumbers():
    while True:
        mqtt_client.publish(mqtt_publish_topic, payload= rd.randint(0,100), qos=2, retain=False)
        time.sleep(5)

mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker_address, 1870)
PrintRandomNumbers()
'''

def draw_fence(start_coords1, end_coords1, start_coords2, end_coords2, num_steps):
    # Convert coordinates to radians
    start_lat1, start_lon1 = math.radians(start_coords1[0]), math.radians(start_coords1[1])
    end_lat1, end_lon1 = math.radians(end_coords1[0]), math.radians(end_coords1[1])

    start_lat2, start_lon2 = math.radians(start_coords2[0]), math.radians(start_coords2[1])
    end_lat2, end_lon2 = math.radians(end_coords2[0]), math.radians(end_coords2[1])

    # Calculate bearing towards destination coordinates
    delta_lon1 = end_lon1 - start_lon1
    y1 = math.sin(delta_lon1) * math.cos(end_lat1)
    x1 = math.cos(start_lat1) * math.sin(end_lat1) - math.sin(start_lat1) * math.cos(end_lat1) * math.cos(delta_lon1)
    theta1 = math.atan2(y1, x1)

    delta_lon2 = end_lon2 - start_lon2
    y2 = math.sin(delta_lon2) * math.cos(end_lat2)
    x2 = math.cos(start_lat2) * math.sin(end_lat2) - math.sin(start_lat2) * math.cos(end_lat2) * math.cos(delta_lon2)
    theta2 = math.atan2(y2, x2)

    # Calculate step distance
    earth_radius = 6371000  # Radius of the Earth in meters
    total_distance1 = math.acos(math.sin(start_lat1) * math.sin(end_lat1) +
                                math.cos(start_lat1) * math.cos(end_lat1) * math.cos(delta_lon1)) * earth_radius
    step_distance1 = total_distance1 / num_steps

    total_distance2 = math.acos(math.sin(start_lat2) * math.sin(end_lat2) +
                                math.cos(start_lat2) * math.cos(end_lat2) * math.cos(delta_lon2)) * earth_radius
    step_distance2 = total_distance2 / num_steps

    # Calculate intermediate coordinates
    intermediate_coordinates = []
    
    # Add the starting coordinates to the list
    intermediate_coordinates.append([(start_coords2[0], start_coords2[1]), (start_coords1[0], start_coords1[1])])

    for step in range(1, num_steps + 1):
        current_distance1 = step * step_distance1
        intermediate_lat1 = math.asin(math.sin(start_lat1) * math.cos(current_distance1 / earth_radius) +
                                       math.cos(start_lat1) * math.sin(current_distance1 / earth_radius) * math.cos(theta1))
        intermediate_lon1 = start_lon1 + math.atan2(math.sin(theta1) * math.sin(current_distance1 / earth_radius) * math.cos(start_lat1),
                                                    math.cos(current_distance1 / earth_radius) - math.sin(start_lat1) * math.sin(intermediate_lat1))
        
        current_distance2 = step * step_distance2
        intermediate_lat2 = math.asin(math.sin(start_lat2) * math.cos(current_distance2 / earth_radius) +
                                       math.cos(start_lat2) * math.sin(current_distance2 / earth_radius) * math.cos(theta2))
        intermediate_lon2 = start_lon2 + math.atan2(math.sin(theta2) * math.sin(current_distance2 / earth_radius) * math.cos(start_lat2),
                                                    math.cos(current_distance2 / earth_radius) - math.sin(start_lat2) * math.sin(intermediate_lat2))
        
        # Convert intermediate coordinates back to degrees
        intermediate_lat1 = math.degrees(intermediate_lat1)
        intermediate_lon1 = math.degrees(intermediate_lon1)

        intermediate_lat2 = math.degrees(intermediate_lat2)
        intermediate_lon2 = math.degrees(intermediate_lon2)

        # Append the coordinates in reverse order for every second of the new inner list
        if step % 2 == 0:
            intermediate_coordinates.append([(intermediate_lat2, intermediate_lon2), (intermediate_lat1, intermediate_lon1)])
        else:
            intermediate_coordinates.append([(intermediate_lat1, intermediate_lon1), (intermediate_lat2, intermediate_lon2)])

    return intermediate_coordinates


def move_coordinates(start_coords, end_coords, num_steps):
    # Convert coordinates to radians
    start_lat, start_lon = math.radians(start_coords[0]), math.radians(start_coords[1])
    end_lat, end_lon = math.radians(end_coords[0]), math.radians(end_coords[1])

    # Calculate bearing towards destination coordinate
    delta_lon = end_lon - start_lon
    y = math.sin(delta_lon) * math.cos(end_lat)
    x = math.cos(start_lat) * math.sin(end_lat) - math.sin(start_lat) * math.cos(end_lat) * math.cos(delta_lon)
    theta = math.atan2(y, x)
    # Calculate step distance
    earth_radius = 6371000  # Radius of the Earth in meters
    total_distance = math.acos(math.sin(start_lat) * math.sin(end_lat) +
                               math.cos(start_lat) * math.cos(end_lat) * math.cos(delta_lon)) * earth_radius
    step_distance = total_distance / num_steps

    # Calculate intermediate coordinates
    intermediate_coordinates = [start_coords]  # Include the start coordinate in the list
    for step in range(1, num_steps + 1):
        current_distance = step * step_distance
        intermediate_lat = math.asin(math.sin(start_lat) * math.cos(current_distance / earth_radius) +
                                     math.cos(start_lat) * math.sin(current_distance / earth_radius) * math.cos(theta))
        intermediate_lon = start_lon + math.atan2(math.sin(theta) * math.sin(current_distance / earth_radius) * math.cos(start_lat),
                                                  math.cos(current_distance / earth_radius) - math.sin(start_lat) * math.sin(intermediate_lat))
        
        # Convert intermediate coordinates back to degrees
        intermediate_lat = math.degrees(intermediate_lat)
        intermediate_lon = math.degrees(intermediate_lon)

        intermediate_coordinates.append((intermediate_lat, intermediate_lon))

    return intermediate_coordinates

def PublishVehicle1():
    for loc in final_coords:
        mqtt_client.publish(mqtt_publish_topic, 
                            payload = str(loc),
                            qos = 2,
                            retain = False)
        time.sleep(5)
        
# Draw the fences
start_coordinates1 = (48.82003, 11.54096)
end_coordinates1 = (48.81839, 11.54184)
start_coordinates2 = (48.82147, 11.54974)
end_coordinates2 = (48.81981, 11.55062)
num_steps = 30
fence_coordinates = draw_fence(start_coordinates1, end_coordinates1, start_coordinates2, end_coordinates2, num_steps)

# Create path coordinates between two corresponding fence coordinates
num_steps_path = 600
final_coords = []
for path in fence_coordinates: # Structure: [[(), ()], [(), ()], ...]
    path_coords = move_coordinates(path[0], path[1], num_steps_path)
    final_coords = final_coords + path_coords

mqtt_publish_topic = "group4/autonomesfahren/gps_fahrzeuge"
mqtt_broker_address = "wi-vm162-01.rz.fh-ingolstadt.de"
mqtt_broker_port = 1870

mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)

PublishVehicle1()