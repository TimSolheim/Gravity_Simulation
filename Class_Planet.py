from copy import deepcopy
from numpy import pi, cos, sin, arctan


class DelayedStart:
    def __init__(self, inp_dict):
        self.time = float(inp_dict['Time'])
        self.follow = inp_dict['Follows']
        self.distance = float(inp_dict['Distance'])
        self.angle = float(inp_dict['Angle'])
        # When object is launched, this is the object it's angle should be calculated relative to
        self.oriented = inp_dict['Oriented']
        self.velocity = float(inp_dict['Velocity'])
        self.velocity_angle = float(inp_dict['Velocity_angle'])
        self.velocity_oriented = inp_dict['Velocity_oriented']


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Impulse:
    def __init__(self, inp_dict):
        self.start_time = float(inp_dict['Start_time'])
        self.end_time = self.start_time + float(inp_dict['Length'])
        self.impulse = float(inp_dict['Magnitude'])
        self.orientation_angle = float(inp_dict['Orientation_angle'])
        self.orientated_relative_to = inp_dict['Orientated_relative_to']


class HistoricalCoordinates:
    def __init__(self, x_cur, y_cur, x_prev, y_prev):
        self.current = Coordinates(x_cur, y_cur)
        self.start = Coordinates(x_cur, y_cur)
        self.previous = Coordinates(x_prev, y_prev)
        self.history = [deepcopy(self.current)]


class Planet:
    def __init__(self, inp_dict, dsd, impulse_set, crash_checking=True):
        self.position = HistoricalCoordinates(float(inp_dict['Pos_x']), float(inp_dict['Pos_y']),
                                              float(inp_dict['Pos_x']), float(inp_dict['Pos_y']))
        self.velocity = HistoricalCoordinates(float(inp_dict['V_x']), float(inp_dict['V_y']),
                                              float(inp_dict['V_x']), float(inp_dict['V_y']))
        self.radius = int(inp_dict['Radius'])
        self.mass = float(inp_dict['Mass'])
        self.name = inp_dict['Name']
        self.colour = inp_dict['Colour']
        self.impulse_set = []
        if impulse_set is not None:
            for x in impulse_set:
                self.impulse_set += [Impulse(x)]
        self.crash_checking = crash_checking
        self.crashed = False
        if dsd is None:
            self.delayed = False
            self.started = True
        else:
            self.delayed = True
            self.started = False
            self.delayed_details = DelayedStart(dsd)
    
    def set_velocity(self, new_velocity):
        self.velocity.current.x = new_velocity.x
        self.velocity.current.y = new_velocity.y

    def set_radius(self, radius):
        self.radius = radius
    
    def set_mass(self, mass):
        self.mass = mass

    def print_start_position(self):
        print(f'Start position:\n\tX: {self.position.start.x}\n\tY: {self.position.start.y}\n')

    def print_current_position(self):
        print(f'Current position:\n\tX: {self.position.current.x}\n\tY: {self.position.current.y}\n')

    def print_start_velocity(self):
        print(f'Start velocity:\n\tX: {self.velocity.start.x}\n\tY: {self.velocity.start.y}\n')

    def print_current_velocity(self):
        print(f'Current velocity:\n\tX: {self.velocity.current.x}\n\tY: {self.velocity.current.y}\n')
    
    def print_information(self):
        print(f'Name: {self.name}\nMass: {self.mass}\nRadius: {self.radius}\n')
        self.print_start_position()
        self.print_current_position()
        self.print_start_velocity()
        self.print_current_velocity()
        print('\n')

    def print_information_at_time(self, time):
        if time < len(self.position.history):
            print(f'Name: {self.name}\nMass: {self.mass}\nRadius: {self.radius}\n')
            print(f'Position:\n\tX: {self.position.history[time].x}\n\tY: {self.position.history[time].y}\n')
            print(f'Velocity:\n\tX: {self.velocity.history[time].x}\n\tY: {self.velocity.history[time].y}\n')

    def update_velocity(self, velocity_change, input_mass):
        self.velocity.current.x += (velocity_change[0]*input_mass)
        self.velocity.current.y += (velocity_change[1]*input_mass)

    def set_starting_velocity(self, new_velocity):
        self.velocity.current.x = new_velocity[0]
        self.velocity.current.y = new_velocity[1]
        self.velocity.start.x = new_velocity[0]
        self.velocity.start.y = new_velocity[1]
        self.velocity.history[0].x = new_velocity[0]
        self.velocity.history[0].y = new_velocity[1]

    def set_starting_position(self, new_position):
        self.position.current.x = new_position[0]
        self.position.current.y = new_position[1]
        self.position.start.x = new_position[0]
        self.position.start.y = new_position[1]
        self.position.history[0].x = new_position[0]
        self.position.history[0].y = new_position[1]

    def add_impulse(self, impulse_set):
        self.impulse_set += [Impulse(impulse_set)]
    
    def change_impulse(self, impulse_set, impulse_num):
        self.impulse_set[impulse_num] = Impulse(impulse_set)

    def increment_time_point(self, precision, record_history=True):
        self.position.previous = deepcopy(self.position.current)
        self.position.current.x += (self.velocity.current.x*precision)
        self.position.current.y += (self.velocity.current.y*precision)
        if record_history:
            self.position.history += [deepcopy(self.position.current)]
            self.velocity.history += [deepcopy(self.velocity.current)]

    def activate_impulse(self, planet_list, current_time, precision):
        for this_impulse in self.impulse_set:
            if this_impulse.start_time <= current_time + precision and current_time < this_impulse.end_time:
                for this_planet in planet_list:
                    if this_planet.name == this_impulse.orientated_relative_to:
                        if this_planet.name == self.name:
                            angle = arctan(self.velocity.current.y/self.velocity.current.x)*180/pi
                        else:
                            angle = arctan((this_planet.position.current.y - self.position.current.y) /
                                           (this_planet.position.current.x - self.position.current.x))*180/pi
                        if this_planet.position.current.x < self.position.current.x:
                            angle += 180
                        angle += this_impulse.orientation_angle
                        while angle > 360:
                            angle -= 360
                        while angle < 0:
                            angle += 360
                        # Correcting needs to be done
                        precision_2 = min(this_impulse.end_time, current_time + precision) -\
                            max(this_impulse.start_time, current_time)
                        x_impulse = this_impulse.impulse*abs(cos(angle*pi/180))*precision_2
                        y_impulse = this_impulse.impulse*abs(sin(angle*pi/180))*precision_2
                        if angle < 90 or angle > 270:
                            self.velocity.current.x += x_impulse
                        elif 90 < angle < 270:
                            self.velocity.current.x -= x_impulse
                        if angle < 180:
                            self.velocity.current.y += y_impulse
                        elif angle > 180:
                            self.velocity.current.y -= y_impulse
                        break

    def start_planet(self, following_planet, oriented_planet, velocity_planet):
        self.started = True
        # Changing the position
        if oriented_planet.position.current.x == following_planet.position.current.x:
            if oriented_planet.position.current.y > following_planet.position.current.y:
                position_angle = 0
            else:
                position_angle = 180
        else:
            position_angle = 180/pi*arctan((oriented_planet.position.current.y - following_planet.position.current.y) /
                                           (oriented_planet.position.current.x - following_planet.position.current.x))
            if oriented_planet.position.current.x < following_planet.position.current.x:
                position_angle += 180
        if velocity_planet.position.current.x == following_planet.position.current.x:
            if velocity_planet.position.current.y > following_planet.position.current.y:
                velocity_angle = 0
            else:
                velocity_angle = 180
        else:
            velocity_angle = 180/pi*arctan((velocity_planet.position.current.y - following_planet.position.current.y) /
                                           (velocity_planet.position.current.x - following_planet.position.current.x))
            if velocity_planet.position.current.x < following_planet.position.current.x:
                velocity_angle += 180
        position_angle += self.delayed_details.angle
        velocity_angle += self.delayed_details.velocity_angle
        self.position.current.x += self.delayed_details.distance*cos(position_angle*pi/180)
        self.position.current.y += self.delayed_details.distance*sin(position_angle*pi/180)
        self.velocity.current.x += self.delayed_details.velocity*cos(velocity_angle*pi/180)
        self.velocity.current.y += self.delayed_details.velocity*sin(velocity_angle*pi/180)
