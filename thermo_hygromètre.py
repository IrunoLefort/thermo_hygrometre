"""
    Thermometer:
    x = temp
    y = distance 
    y = ax + b
    a = (y_f - y_i)/(x_f - x_i) = (6 - 1.5)/(50 - 0) = 4.5/50
    y = (4.5/50)x + 1.5
"""

"""
    Humidity:
    x = humidity
    y = theta 
    y = ax + b
    a = (y_f - y_i)/(x_f - x_i) = (π/6 - 5π/6)/(100 - 0) = -π/150
    y = (-π/150)x + 5π/6
"""

import serial
import time
from vpython import *
import numpy as np
import serial.tools.list_ports

# cadre
scene.center = vector(5, 0, 0)
scene.height = 600
scene.width = 1000

# Thermometer
offset_left = -1
# red sphere
my_sphere = sphere(radius=1,
              color=color.red, pos=vector(offset_left,-3,0))

# cylinder
[cylinder_lenght, cylinder_radius] = [0.01, 0.6]
my_cylinder = cylinder(color=color.red, radius=cylinder_radius,
                       length=cylinder_lenght, axis=vector(0,1,0), pos=vector(offset_left,-3,0))

# glass sphere
glass_sphere = sphere(radius=1.2,
              color=color.white, opacity=0.25, pos=vector(offset_left,-3,0))

# glass cylinder
[glass_cylinder_lenght, glass_cylinder_radius] = [6, 0.8]
glass_cylinder = cylinder(color=color.white, radius=glass_cylinder_radius,
                       length=glass_cylinder_lenght, axis=vector(0,1,0),
                       opacity=0.25, pos=vector(offset_left,-3,0))

for temp in range(0,51,10):
    tick_position = (4.5/50)*temp+1.5
    tick_mark = cylinder(radius=0.7, color=color.black, length=0.01,
                         pos=vector(offset_left, tick_position-3, 0), axis=vector(0, 1, 0))
    
    # Add label
    label_pos = vector(offset_left-1.25, tick_position-3,0)
    text(text=str(temp), pos=label_pos, height=0.2, color=color.white)
    
# show the value
show_value = label(text=str(0), pos=vector(offset_left, -3, 1), height=20, color=color.white, box=False)

#label
text(text="Temperature", pos=vector(offset_left,3.75,0), height=0.5, 
     color=color.white, align="center")


#Humidity 
offset_right = 7
theta_min = 5*np.pi/6
theta_max = np.pi/6

#box
[box_x, box_y, box_z] = [10, 6, 0.4]
my_box = box(color=color.white, 
             size=vector(box_x, box_y, box_z), 
             pos=vector(offset_right,0,-box_z/2))
             
# red arrow
[arrow_length, arrow_width] = [box_y-2, 0.15]
my_arrow = arrow(length=arrow_length, 
                 shaftwidth=arrow_width, 
                 color=color.red, 
                 axis=vector(arrow_length*np.cos(theta_min), arrow_length*np.sin(theta_min), 0),
                 pos=vector(offset_right,-0.9*box_y/2,0.2))

#tick
[tick_length, tick_height, tick_width] = [0.4, 0.1, 0.1]
for i, theta in enumerate(np.linspace(theta_min, theta_max, 11)): 
    tick_major = box(color=color.black,
                     pos=vector(arrow_length*np.cos(theta)+offset_right, arrow_length*np.sin(theta)-0.9*box_y/2, 0),
                     size=vector(tick_length, tick_width, tick_height),
                     axis=vector(arrow_length*np.cos(theta), arrow_length*np.sin(theta), 0))

    # Add label
    label_pos = vector(1.1*arrow_length*np.cos(theta) + offset_right, 
                       1.1*arrow_length*np.sin(theta) - 0.9*box_y/2, 0)
    text(text=str(i*10), pos=label_pos, height=0.3, color=color.black, 
         axis=vector(arrow_length*np.cos(theta-np.pi/2), arrow_length*np.sin(theta-np.pi/2), 0), align='center')

for theta in np.linspace(theta_min, theta_max, 51): 
    tick_minor = box(color=color.black,
                     pos=vector(arrow_length*np.cos(theta)+offset_right, arrow_length*np.sin(theta)-0.9*box_y/2, 0),
                     size=vector(tick_length/2, tick_width/5, tick_height/2),
                     axis=vector(arrow_length*np.cos(theta), arrow_length*np.sin(theta), 0))

#hub
[hub_length, hub_radius] = [0.02, 0.02]
hub = cylinder(color=color.red, radius=hub_radius, length=hub_length,
               axis=vector(0,0,1), pos=vector(offset_right,-0.9*box_y/2,0.2))

#label
text(text="Humidity(%)", pos=vector(offset_right,3.75,0), height=0.5, 
     color=color.white, align="center")


#communication with arduino
ports = serial.tools.list_ports.comports()
ports_list = [port.device for port in ports]

if not ports_list:
    print("Aucun port détecté.")
    exit

print("Ports disponibles :")
for port in ports:
    print(str(port))
        
try:
    choice = int(input("Select Com Port for arduino: "))
    for i in range(len(ports_list)):
        if(ports_list[i].startswith("COM" + str(choice))):
            selected_port = "COM" + str(choice)
            print(f"Selected port: {selected_port}")

except ValueError:
    print("Entrée invalide.")
    exit

try:
    arduino_data = serial.Serial(selected_port, 9600)
    time.sleep(1)
    while True:
        while(arduino_data.inWaiting()==0):
            pass
        data_packet = arduino_data.readline()
        data_packet = str(data_packet, "utf-8")
        data_packet = data_packet.strip('\r\n')
        data_packet = data_packet.split(',')
        tempC = float(data_packet[0])
        humidity = float(data_packet[1])
        y_temp = (4.5/50)*tempC + 1.5
        y_humidity = (-np.pi/150)*humidity + 5*np.pi/6
        print(f"Temp = {tempC}°C \t Humidity = {humidity}%")
        my_cylinder.length=y_temp
        my_arrow.axis=vector(arrow_length*np.cos(y_humidity), arrow_length*np.sin(y_humidity), 0)
        show_value.text=str(tempC)
        
except serial.SerialException as e:
    print(f"Erreur de connexion : {e}")