from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock
import socket
import time
import math

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 30003))
aircraft_data={}

class MyApp(App):
    def build(self):
        self.update_counter = 0  # Add a counter variable
        self.radar = Radar()
        Clock.schedule_interval(self.update_label, 1.0)  # Update every second
        #self.update_label()
        return self.radar
    
    def cleanup_flights(self, timeout=20):
        current_time = time.time()
        expired_keys = []  # a list to store the keys to delete after iteration
        for icao, flight in aircraft_data.items():
            if current_time - flight['last_seen'] >= timeout:
                expired_keys.append(icao)  # append the keys to the list, but do not delete them yet
        for icao in expired_keys:
            del aircraft_data[icao]  # now delete the keys


    def update_label(self, *args):
        #self.update_counter += 1
        data = s.recv(1024)
        # Decode the binary data into a string
        data_string = data.decode('utf-8')

        # Split the string into a list of strings
        messages = data_string.split('\n')
        
        # ...
        for line in messages:
            # Split the line into fields
            fields = line.split(',')

            # Check if the line contains at least the expected number of fields
            if len(fields) >= 18:  # adjust this number according to your needs
                # Get the ICAO24 code
                icao24 = fields[4]

                # If this is a new aircraft, add it to the dictionary
                if icao24 not in aircraft_data:
                    aircraft_data[icao24] = {}

                # Update the relevant fields in the dictionary
                if fields[1] == '3':  # Airborne position message
                    aircraft_data[icao24]['altitude'] = fields[11]
                    aircraft_data[icao24]['lat'] = fields[14]
                    aircraft_data[icao24]['lon'] = fields[15]
                elif fields[1] == '4':  # Airborne velocity message
                    aircraft_data[icao24]['speed'] = fields[12]  # Speed is a simplification of the ground speed calculation
                    aircraft_data[icao24]['track'] = fields[13]  # Track (heading)
                elif fields[1] == '1':  # Identification message
                    aircraft_data[icao24]['flight'] = fields[10]
                elif fields[1] == '6':  # Surveillance altitude message
                    aircraft_data[icao24]['squawk'] = fields[17]
                aircraft_data[icao24]['last_seen']=time.time()
        self.cleanup_flights()
        print(aircraft_data)
        
class Radar(Widget):
    def __init__(self, **kwargs):
        super(Radar, self).__init__(**kwargs)
        self.angle = 0

        with self.canvas:
            self.color = Color(0, 158, 0)  # white color
            self.circle = Line(circle=(self.center_x, self.center_y, min(self.width, self.height) / 2), width=2)

            PushMatrix()
            self.rot = Rotate()
            self.line = Line(points=[self.center_x, self.center_y, self.center_x, self.center_y - self.height / 2],
                             width=2)
            PopMatrix()

        Clock.schedule_interval(self.update, 1 / 60.)  # update at 60fps

    def update(self, dt):
        self.angle += 1
        if self.angle >= 360:
            self.angle = 0

        self.rot.angle = self.angle
        self.rot.origin = self.center

    def on_size(self, *args):
        self.circle.circle = self.center_x, self.center_y, min(self.width, self.height) / 2
        self.line.points = [self.center_x, self.center_y, self.center_x, self.center_y - self.height / 2]


if __name__ == '__main__':
    MyApp().run()
