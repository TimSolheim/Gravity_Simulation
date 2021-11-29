from numpy import pi, arctan, sqrt, round, cos, sin
from Class_Planet import Planet
from copy import deepcopy
from matplotlib.pyplot import plot
from matplotlib.pyplot import show
from matplotlib.pyplot import figure
from matplotlib.pyplot import axes
from matplotlib.animation import FuncAnimation
from Custom_analysis import analysis
from Custom_analysis import analysis_2


class PlanetSet:
    def __init__(self):
        self.max_time = 1000000
        self.max_runs = 1000000
        self.precisions = [100, 100]
        self.g = 66740*360000
        self.precision_min = self.precisions[0]
        self.precision_max = self.precisions[1]
        self.precision_cur = self.precisions[1]
        self.current_time = 0
        self.current_run = 0
        self.animation_length = 30
        self.animation_scale = 400000000
        self.planets_loaded = False
        self.min_time = 0
        self.print_percentages = True
        self.planets = []
        self.all_planets = []
        self.original_planets = []
        self.plot_planets = []
        self.plot_relative_planets = []
        self.time_list = []
        self.x_positions = []
        self.y_positions = []
        self.main_planet = None

    def set_parameters(self, extra_info=None):
        if extra_info is not None and len(extra_info) > 0:
            using_ei = True
        else:
            using_ei = False
        while True:
            if using_ei:
                inp = extra_info[0]
            else:
                inp = input('Please input a maximum time: ')
            if inp.upper() == 'E':
                print(f'The current maximum time of {self.max_time} was used.')
                break
            try:
                self.max_time = int(inp)
                break
            except ValueError:
                print('That was not a number.')
                using_ei = False
        if extra_info is not None and len(extra_info) > 1:
            using_ei = True
        while True:
            if using_ei:
                inp = extra_info[1]
            else:
                inp = input('Please input the maximum number of runs: ')
            if inp.upper() == 'E':
                print(f'The current maximum number of {self.max_runs} was used.')
                break
            try:
                self.max_runs = int(inp)
                break
            except ValueError:
                print('That was not a number.')
                using_ei = False
        if extra_info is not None and len(extra_info) > 2:
            using_ei = True
        while True:
            if using_ei:
                inp = extra_info[2]
            else:
                inp = input('Please input the minimum precision: ')
            if inp.upper() == 'E':
                print(f'The current minimum precision of {self.precision_min} was used.')
                break
            try:
                self.precision_min = float(inp)
                break
            except ValueError:
                print('That was not a number.')
                using_ei = False
        if extra_info is not None and len(extra_info) > 3:
            using_ei = True
        while True:
            if using_ei:
                inp = extra_info[3]
            else:
                inp = input('Please input the maximum precision: ')
            if inp.upper() == 'E':
                print(f'The current maximum precision of {self.precision_max} was used.')
                break
            try:
                self.precision_max = float(inp)
                self.precision_cur = float(inp)
                break
            except ValueError:
                print('That was not a number.')
                using_ei = False
        if extra_info is not None and len(extra_info) > 1:
            using_ei = True
        while True:
            if using_ei:
                inp = extra_info[4]
            else:
                inp = input('Please input whether you want to print percentages: ')
            if inp.upper() in ('0', 'NO', 'N', 'FALSE', 'F'):
                self.print_percentages = False
                break
            elif inp.upper() in ('1', 'YES', 'Y', 'TRUE', 'T'):
                self.print_percentages = True
                break
            elif inp.upper() == 'E':
                break
            else:
                using_ei = False

    def write_to_file(self, filename='Planet_load.txt'):
        file = open('C:\\Users\\jtims\\PycharmProjects\\Gravity\\' + filename, 'a+')
        for p in self.planets:
            file.write(f'\nName:{p.name}\tColour:{p.colour}\tMass:{p.mass}\tRadius:{p.radius}\t' +
                       f'Pos_x:{p.position.current.x}\tPos_y:{p.position.current.y}\tV_x:{p.velocity.current.x}\t' +
                       f'V_y:{p.velocity.current.y}')
        file.close()

    def load_planets(self, filename='Planet_load.txt'):
        print(f'Loading planets from {filename}')
        file = open('C:\\Users\\jtims\\PycharmProjects\\Gravity\\' + filename)
        input_data = file.read().split('\n')
        file.close()
        while input_data[-1] == '':
            del input_data[-1]
        for this_planet in input_data:
            dict_planet = {}
            dsd_dict = None
            impulse_list = None
            planet_details = deepcopy(this_planet).split('\t')
            for specific_detail in planet_details:
                split_details = deepcopy(specific_detail).split(':')
                if split_details[0] == 'DSD':
                    dsd_dict = {}
                    dsd_details = deepcopy(split_details[1]).split('|')
                    for this_detail in dsd_details:
                        dsd_specific_detail = deepcopy(this_detail).split('~')
                        dsd_dict[dsd_specific_detail[0]] = dsd_specific_detail[1]
                elif split_details[0] == 'Impulse':
                    impulse_list = []
                    impulse_details = deepcopy(split_details[1]).split('|')
                    for this_impulse in impulse_details:
                        impulse_dict = {}
                        this_impulse_details = deepcopy(this_impulse).split('~')
                        for x in this_impulse_details:
                            y = deepcopy(x).split('^')
                            impulse_dict[y[0]] = y[1]
                        impulse_list += [deepcopy(impulse_dict)]
                else:
                    dict_planet[split_details[0]] = split_details[1]
            self.all_planets += [Planet(dict_planet, dsd_dict, impulse_list)]
        self.planets = self.all_planets
        self.plot_planets = self.all_planets
        self.plot_relative_planets = self.all_planets[1:]
        self.main_planet = self.all_planets[0]
        self.planets_loaded = True
        self.original_planets = deepcopy(self.all_planets)

    def set_planet_value(self, num, value_to_change, value_set):
        if value_to_change in ('VELOCITY_XY', 'V_XY', 'VXY'):
            v1 = int(value_set[0])
            v2 = int(value_set[1])
            self.all_planets[num].set_starting_velocity([v1, v2])
        elif value_to_change in ('VELOCITY_A', 'V_A', 'VA'):
            v1 = int(value_set[0])*cos(pi*int(value_set[1])/180)
            v2 = int(value_set[0])*sin(pi*int(value_set[1])/180)
            self.all_planets[num].set_starting_velocity([v1, v2])
        elif value_to_change in ('POSITION_XY', 'P_XY', 'PXY', 'POS_XY', 'POSXY'):
            p1 = int(value_set[0])
            p2 = int(value_set[1])
            self.all_planets[num].set_starting_position([p1, p2])
        elif value_to_change in ('POSITION_A', 'P_A', 'PA', 'POS_A', 'POSA'):
            p1 = int(value_set[0])*cos(pi*int(value_set[1])/180)
            p2 = int(value_set[0])*sin(pi*int(value_set[1])/180)
            self.all_planets[num].set_starting_position([p1, p2])
        elif value_to_change in ('IMPULSE_ADD', 'I_ADD', 'IADD', 'IAD'):
            inp_dict = {'Start_time': value_set[0], 'Length': value_set[1], 'Magnitude': value_set[2],
                        'Orientation_angle': value_set[3], 'Orientated_relative_to': value_set[4]}
            self.all_planets[num].add_impulse(inp_dict)
        elif value_to_change in ('IMPULSE_ALT', 'I_ALT', 'IALT', 'IAL'):
            inp_dict = {'Start_time': value_set[0], 'Length': value_set[1], 'Magnitude': value_set[2],
                        'Orientation_angle': value_set[3], 'Orientated_relative_to': value_set[4]}
            self.all_planets[num].add_impulse(inp_dict, int(value_set[5]))

    def set_animation_scale(self):
        while True:
            try:
                self.animation_scale = int(input('Please input a scale: '))
                break
            except ValueError:
                print('That is not a valid scale. Please retry')

    def set_min_time(self):
        while True:
            inp = input('Please input a minimum plotting time: ')
            if inp.upper() == 'E':
                break
            try:
                self.min_time = int(inp)
                break
            except ValueError:
                print('That was not a number.')

    def print_info_for_planet_for_time(self):
        inp = input('Please input a planet number: ')
        planet_num = 0
        try:
            planet_num = int(inp)
            is_number = True
        except ValueError:
            is_number = False
            print('That was not a number!')
        if is_number:    
            if planet_num > len(self.planets):
                print('That number does not correspond to a planet!')
            else:
                inp = input('Please input a time: ')
                time = 0
                try:
                    time = float(inp)
                    is_number = True
                except ValueError:
                    is_number = False
                    print('That was not a number!')
                if is_number:
                    time_index = 0
                    searching = True
                    while searching and time_index < len(self.time_list):
                        if self.time_list[time_index] == time:
                            searching = False
                        else:
                            time_index += 1
                    if searching:
                        print('That was not a valid time!')
                    else:
                        self.planets[planet_num].print_information_at_time(time_index)

    # def write_to_file(self):
    #     filename = 'C:\\Users\\jtims\\PycharmProjects\\Gravity\\Data_'
    #     for x in range(len(self.planets)):
    #         filename += self.planets[x].name + '-'
    #     if self.precision_min == self.precision_max:
    #         filename = filename[:-1] + f'_{self.precision_min}.txt'
    #     else:
    #         filename = filename[:-1] + '_var.txt'
    #     file = open(filename, 'a+')
    #     for i in range(len(self.time_list)):
    #         if self.time_list[i] % 10 == 0:
    #             writing = f'{i}\t{self.time_list[i]}\t'
    #             for n in range(len(self.planets)):
    #                 writing += f'{self.planets[n].position.history[i].x}\t{self.planets[n].position.history[i].y}\t' +
    #                 f'{self.planets[n].velocity.history[i].x}\t{self.planets[n].velocity.history[i].y}\t'
    #             file.write(writing[:-1] + '\n')
    #     file.close()

    def get_planets_for_running(self, do_deepcopy=False, inp_0=None):
        if not self.planets_loaded:
            self.load_planets()
        output_subset_numbers = []
        adding_planets = True
        for planet_number in range(len(self.all_planets)):
            print(f'#{planet_number}\t{self.all_planets[planet_number].name}')
        while adding_planets:
            if inp_0 is None:
                inp_0 = input('Please enter a planet number to add to the list. Enter "E" to finish: ')
            inp_1 = inp_0.split(' ')
            for inp in inp_1:
                if inp.upper() == 'E':
                    if len(self.planets) == 0:
                        new_input = input('You have not yet added a planet! Enter "E" to confirm: ')
                        if new_input.upper() == 'E':
                            adding_planets = False
                            break
                    else:
                        adding_planets = False
                        break
                else:
                    planet_num = 0
                    try:
                        planet_num = int(inp)
                        is_number = True
                    except ValueError:
                        print('That is not a number.')
                        is_number = False
                    if is_number:
                        if planet_num in output_subset_numbers:
                            print('That number planet is already in the plotting list.')
                        elif planet_num >= len(self.all_planets):
                            print('That is not a valid planet number.')
                        else:
                            output_subset_numbers += [planet_num]
                            if do_deepcopy:
                                self.planets += [deepcopy(self.all_planets[planet_num])]
                            else:
                                self.planets += [self.all_planets[planet_num]]
            inp_0 = None
        self.main_planet = self.planets[0]
        self.plot_planets = self.planets
        self.plot_relative_planets = self.planets[1:]

    def reset_all_planets(self):
        self.all_planets = deepcopy(self.original_planets)
        self.planets = self.all_planets
        self.plot_planets = self.planets
        self.main_planet = self.planets[0]
        self.plot_relative_planets = self.planets[1:]
        self.current_time = 0
        self.current_run = 0

    def get_subset_planets(self, subset_for, do_deepcopy=False):
        if subset_for not in ('Plotting', 'Relative plotting'):
            print('That is an invalid subset intention')
        else:
            if subset_for == 'Plotting':
                self.plot_planets = []
            elif subset_for == 'Relative plotting':
                self.plot_relative_planets = []
            output_subset_numbers = []
            adding_planets = True
            if subset_for == 'Plotting':
                for planet_number in range(len(self.planets)):
                    print(f'#{planet_number}\t{self.planets[planet_number].name}')
            while adding_planets:
                inp = input('Please enter a planet number to add to the list. Enter "E" to finish: ')
                if inp.upper() == 'E':
                    if (subset_for == 'Running' and len(self.planets) == 0) or\
                       (subset_for == 'Plotting' and len(self.plot_planets) == 0) or \
                       (subset_for == 'Relative plotting' and len(self.plot_relative_planets) == 0):
                        new_input = input('You have not yet added a planet! Enter "E" to confirm: ')
                        if new_input.upper() == 'E':
                            adding_planets = False
                    else:
                        adding_planets = False
                else:
                    planet_num = 0
                    try:
                        planet_num = int(inp)
                        is_number = True
                    except ValueError:
                        print('That is not a number.')
                        is_number = False
                    if is_number:
                        if planet_num in output_subset_numbers:
                            print('That number planet is already in the plotting list.')
                        elif planet_num >= len(self.planets):
                            print('That is not a valid planet number.')
                        else:
                            output_subset_numbers += [planet_num]
                            if subset_for == 'Plotting':
                                if do_deepcopy:
                                    self.plot_planets += [deepcopy(self.planets[planet_num])]
                                else:
                                    self.plot_planets += [self.planets[planet_num]]
                            elif subset_for == 'Relative plotting':
                                if do_deepcopy:
                                    self.plot_relative_planets += [deepcopy(self.planets[planet_num])]
                                else:
                                    self.plot_relative_planets += [self.planets[planet_num]]

    def get_relative_planets(self):
        for planet_number in range(len(self.planets)):
            print(f'#{planet_number}\t{self.planets[planet_number].name}')
        getting_main_planet = True
        while getting_main_planet:
            inp = input('Please input a main planet number: ')
            planet_number = 0
            try:
                planet_number = int(inp)
                is_number = True
            except ValueError:
                print('That is not a number.')
                is_number = False
            if is_number:
                if planet_number >= len(self.planets):
                    print('That number is not a valid planet number.')
                else:
                    self.main_planet = self.planets[planet_number]
                    getting_main_planet = False
        self.get_subset_planets('Relative plotting')

    def plot_position(self):
        print('POSITION')
        pos_x, pos_y = [], []
        for p in range(len(self.plot_planets)):
            pos_x += [[]]
            pos_y += [[]]
            for t in range(len(self.plot_planets[0].position.history)):
                pos_x[p] += [self.plot_planets[p].position.history[t].x]
                pos_y[p] += [self.plot_planets[p].position.history[t].y]
        for p in range(len(self.plot_planets)):
            plot(pos_x[p], pos_y[p], color=self.plot_planets[p].colour)
        show()

    def plot_position_x(self):
        print('X POSITION')
        pos_x = []
        for p in range(len(self.plot_planets)):
            pos_x += [[]]
            for t in range(len(self.plot_planets[p].position.history)):
                pos_x[p] += [self.plot_planets[p].position.history[t].x]
        for p in range(len(self.plot_planets)):
            plot(self.time_list, pos_x[p], color=self.plot_planets[p].colour)
        show()

    def plot_position_y(self):
        print('Y POSITION')
        pos_y = []
        for p in range(len(self.plot_planets)):
            pos_y += [[]]
            for t in range(len(self.plot_planets[p].position.history)):
                pos_y[p] += [self.plot_planets[p].position.history[t].y]
        for p in range(len(self.plot_planets)):
            plot(self.time_list, pos_y[p], color=self.plot_planets[p].colour)
        show()

    def plot_distance(self):
        print('DISTANCE')
        dist = [[]]
        for p in range(len(self.plot_planets)):
            dist += [[]]
            for t in range(len(self.plot_planets[p].position.history)):
                dist[p] += [sqrt(self.plot_planets[p].position.history[t].x**2 +
                                 self.plot_planets[p].position.history[t].y**2)]
        for p in range(len(self.plot_planets)):
            plot(self.time_list, dist[p], color=self.plot_planets[p].colour)
            if min(dist[p]) == 0:
                print(f'{self.plot_planets[p].name}\tMaximum distance: {max(dist[p])}\t' +
                      f'Minimum distance: {min(dist[p])}\t%Diff: N/A')
            else:
                print(f'{self.plot_planets[p].name}\tMaximum distance: {max(dist[p])}\t' +
                      f'Minimum distance: {min(dist[p])}\t%Diff: {max(dist[p])/min(dist[p])*100-100}')
        show()

    def plot_velocity(self):
        print('VELOCITY')
        v = []
        for p in range(len(self.plot_planets)):
            v += [[]]
            for t in range(len(self.plot_planets[p].velocity.history)):
                v[p] += [sqrt(self.plot_planets[p].velocity.history[t].x**2 +
                              self.plot_planets[p].velocity.history[t].y**2)]
        for p in range(len(self.plot_planets)):
            plot(self.time_list, v[p], color=self.plot_planets[p].colour)
            if min(v[p]) == 0:
                print(f'{self.plot_planets[p].name}\tMaximum velocity: {max(v[p])}\tMinimum velocity: {min(v[p])}' +
                      f'\t%Diff: N/A')
            else:
                print(f'{self.plot_planets[p].name}\tMaximum velocity: {max(v[p])}\tMinimum velocity: {min(v[p])}' +
                      f'\t%Diff: {max(v[p])/min(v[p])*100-100}')
        show()

    def plot_velocity_x(self):
        print('X VELOCITY')
        v_x = []
        for p in range(len(self.plot_planets)):
            v_x += [[]]
            for t in range(len(self.plot_planets[p].velocity.history)):
                v_x[p] += [self.plot_planets[p].velocity.history[t].x]
        for p in range(len(self.plot_planets)):
            plot(self.time_list, v_x[p], color=self.plot_planets[p].colour)
        show()

    def plot_velocity_y(self):
        print('Y VELOCITY')
        v_y = []
        for p in range(len(self.plot_planets)):
            v_y += [[]]
            for t in range(len(self.plot_planets[p].velocity.history)):
                v_y[p] += [self.plot_planets[p].velocity.history[t].y]
        for p in range(len(self.plot_planets)):
            plot(self.time_list, v_y[p], color=self.plot_planets[p].colour)
        show()

    def plot_angles(self):
        print('ANGLE')
        a = []
        for p in range(len(self.plot_planets)):
            a += [[]]
            for t in range(len(self.plot_planets[p].position.history)):
                if self.plot_planets[p].position.history[t].y == 0:
                    ang = 90 if self.plot_planets[p].position.history[t].x > 0 else 270
                else:
                    ang = arctan(self.plot_planets[p].position.history[t].x/self.plot_planets[p].position.history[t].y)\
                          / pi * 180
                    if self.plot_planets[p].position.history[t].y < 0:
                        ang += 180
                    elif self.plot_planets[p].position.history[t].x < 0 and \
                            self.plot_planets[p].position.history[t].y > 0:
                        ang += 360
                a[p] += [ang]
            plot(self.time_list, a[p], color=self.plot_planets[p].colour)
        show()

    def plot_relative_position(self):
        time_list_min = 0
        for i in range(len(self.time_list)):
            if self.time_list[i] >= self.min_time:
                time_list_min = i
                break
        for p in range(len(self.plot_relative_planets)):
            print('RELATIVE POSITIONS', self.main_planet.name, self.plot_relative_planets[p].name)
            pos_x = []
            pos_y = []
            for t in range(time_list_min, len(self.main_planet.position.history)):
                pos_x += [self.plot_relative_planets[p].position.history[t].x - self.main_planet.position.history[t].x]
                pos_y += [self.plot_relative_planets[p].position.history[t].y - self.main_planet.position.history[t].y]
            plot(pos_x, pos_y, color=self.plot_relative_planets[p].colour)
        show()

    def plot_relative_position_x(self):
        for p in range(len(self.plot_relative_planets)):
            print('RELATIVE POSITION X', self.main_planet.name, self.plot_relative_planets[p].name)
            dist = []
            for t in range(len(self.plot_relative_planets[p].position.history)):
                dist += [self.plot_relative_planets[p].position.history[t].x - self.main_planet.position.history[t].x]
            plot(self.time_list, dist, color=self.plot_relative_planets[p].colour)
        show()

    def plot_relative_position_y(self):
        for p in range(len(self.plot_relative_planets)):
            print('RELATIVE DISTANCE', self.main_planet.name, self.plot_relative_planets[p].name)
            dist = []
            for t in range(len(self.plot_relative_planets[p].position.history)):
                dist += [self.plot_relative_planets[p].position.history[t].y - self.main_planet.position.history[t].y]
            plot(self.time_list, dist, color=self.plot_relative_planets[p].colour)
        show()

    def plot_relative_distance(self):
        time_list_min = 0
        for i in range(len(self.time_list)):
            if self.time_list[i] >= self.min_time:
                time_list_min = i
                break
        for p in range(len(self.plot_relative_planets)):
            print('RELATIVE DISTANCE', self.main_planet.name, self.plot_relative_planets[p].name)
            dist = []
            min_dist = sqrt((self.main_planet.position.history[time_list_min].x -
                             self.plot_relative_planets[p].position.history[time_list_min].x)**2 +
                            (self.main_planet.position.history[time_list_min].y -
                             self.plot_relative_planets[p].position.history[time_list_min].y)**2)
            max_dist = min_dist
            min_t = time_list_min
            max_t = time_list_min
            for t in range(time_list_min, len(self.main_planet.position.history)):
                dist_new = sqrt((self.main_planet.position.history[t].x -
                                 self.plot_relative_planets[p].position.history[t].x)**2 +
                                (self.main_planet.position.history[t].y -
                                 self.plot_relative_planets[p].position.history[t].y)**2)
                dist += [dist_new]
                if dist_new < min_dist:
                    min_dist = dist_new
                    min_t = t
                elif dist_new > max_dist:
                    max_dist = dist_new
                    max_t = t
            print(f'The minimum distance between {self.main_planet.name} and {self.plot_relative_planets[p].name} was' +
                  f' {min_dist} and was at time {self.time_list[min_t]}')
            print(f'The maximum distance between {self.main_planet.name} and {self.plot_relative_planets[p].name} was' +
                  f' {max_dist} and was at time {self.time_list[max_t]}')
            plot(self.time_list[time_list_min:], dist, color=self.plot_relative_planets[p].colour)
        show()

    def plot_relative_to_two_fixed_stars(self):
        fixed_distances = []
        fixed_angles = []
        y_axis = []
        for i in range(len(self.planets[1].position.history)):
            fixed_distances += [sqrt((self.planets[1].position.history[i].x -
                                      self.planets[0].position.history[i].x)**2 +
                                     (self.planets[1].position.history[i].y -
                                      self.planets[0].position.history[i].y)**2)]
            angle = 180/pi*arctan((self.planets[1].position.history[i].y - self.planets[0].position.history[i].y) /
                                  (self.planets[1].position.history[i].x - self.planets[0].position.history[i].x))
            if self.planets[1].position.history[i].x < self.planets[0].position.history[i].x:
                angle += 180
            if angle < 0:
                angle += 360
            fixed_angles += [angle]
            y_axis += [0]
        plot(fixed_distances, y_axis, color=self.planets[1].colour)
        for p in range(2, len(self.planets)):
            x_axis = []
            y_axis = []
            for i in range(len(self.planets[1].position.history)):
                distance = sqrt((self.planets[0].position.history[i].x - self.planets[p].position.history[i].x)**2 +
                                (self.planets[0].position.history[i].y - self.planets[p].position.history[i].y)**2)
                angle = 180/pi*arctan((self.planets[p].position.history[i].y - self.planets[0].position.history[i].y) /
                                      (self.planets[p].position.history[i].x - self.planets[0].position.history[i].x))
                if self.planets[p].position.history[i].x < self.planets[0].position.history[i].x:
                    angle += 180
                angle -= fixed_angles[i]
                if angle > 360:
                    angle -= 360
                elif angle < 0:
                    angle += 360
                x_axis += [distance*cos(pi/180*angle)]
                y_axis += [distance*sin(pi/180*angle)]
            plot(x_axis, y_axis, color=self.planets[p].colour)
        show()

    def plot_relative_velocity(self):
        print('VELOCITY')
        v = []
        time_list_min = 0
        for i in range(len(self.time_list)):
            if self.time_list[i] >= self.min_time:
                time_list_min = i
                break
        for p in range(len(self.plot_relative_planets)):
            v += [[]]
            for t in range(time_list_min, len(self.plot_relative_planets[p].velocity.history)):
                v[p] += [sqrt((self.main_planet.velocity.history[t].x -
                               self.plot_relative_planets[p].velocity.history[t].x)**2 +
                              (self.main_planet.velocity.history[t].y -
                               self.plot_relative_planets[p].velocity.history[t].y)**2)]
        for p in range(len(self.plot_relative_planets)):
            plot(self.time_list[time_list_min:], v[p], color=self.plot_relative_planets[p].colour)
            if min(v[p]) == 0:
                print(f'{self.plot_relative_planets[p].name} Maximum relative velocity: {max(v[p])}\t' +
                      f'Minimum relative velocity: {min(v[p])}\t%Diff: N/A')
            else:
                print(f'{self.plot_relative_planets[p].name} Maximum relative velocity: {max(v[p])}\t' +
                      f'Minimum relative velocity: {min(v[p])}\t%Diff: {max(v[p])/min(v[p])*100-100}')
        show()

    def plot_relative_angles(self):
        print('ANGLE')
        a = []
        for p in range(len(self.plot_relative_planets)):
            a += [[]]
            for t in range(len(self.plot_relative_planets[p].position.history)):
                if (self.plot_relative_planets[p].position.history[t].y - self.main_planet.position.history[t].y) == 0:
                    ang = 90 if (self.plot_relative_planets[p].position.history[t].x -
                                 self.main_planet.position.history[t].x) > 0 else 270
                else:
                    ang = arctan((self.plot_relative_planets[p].position.history[t].x -
                                  self.main_planet.position.history[t].x) /
                                 (self.plot_relative_planets[p].position.history[t].y -
                                  self.main_planet.position.history[t].y))/pi*180
                    if (self.plot_relative_planets[p].position.history[t].y -
                            self.main_planet.position.history[t].y) < 0:
                        ang += 180
                    elif (self.plot_relative_planets[p].position.history[t].x -
                          self.main_planet.position.history[t].x) < 0 and\
                            (self.plot_relative_planets[p].position.history[t].y -
                             self.main_planet.position.history[t].y) > 0:
                        ang += 360
                a[p] += [ang]
            plot(self.time_list, a[p], color=self.plot_relative_planets[p].colour)
        show()

    def plot_distance_relative_to_angle(self):
        for p in range(len(self.plot_planets)):
            dist = []
            angles = []
            for t in range(len(self.plot_planets[p].position.history)):
                if self.plot_planets[p].position.history[t].y == self.main_planet.position.history[t].y:
                    if self.plot_planets[p].position.history[t].x > self.main_planet.position.history[t].x:
                        angles += [90]
                    else:
                        angles += [270]
                else:
                    angle = 180/pi*arctan((self.plot_planets[p].position.history[t].x -
                                           self.main_planet.position.history[t].x) /
                                          (self.plot_planets[p].position.history[t].y -
                                           self.main_planet.position.history[t].y))
                    # if self.plot_planets[p].position.history[t].y < self.main_planet.position.history[t].y:
                    # UNTESTED CORRECTION
                    if self.plot_planets[p].position.history[t].x < self.main_planet.position.history[t].x:
                        angle += 180
                    if angle > 360:
                        angle -= 360
                    elif angle < 0:
                        angle += 360
                    angles += [angle]
                dist += [self.plot_planets[p].position.history[t].y - self.main_planet.position.history[t].y]
            plot(angles, dist, color=self.plot_planets[p].colour)
        show()

    def animation_init(self):
        for line in self.lines:
            line.set_data([], [])
        return self.lines

    def plot_animate_single(self, i, animation_list, c_size, sq_size):
        for j, line in enumerate(self.lines):
            if j < len(animation_list):
                line.set_data(self.x_positions[j][:i+1], self.y_positions[j][:i+1])
            elif j < 2*len(animation_list):
                x_pos = self.x_positions[j-len(animation_list)][i]
                y_pos = self.y_positions[j-len(animation_list)][i]
                t_size = sq_size[j-len(animation_list)]
                x_square_pos = [x_pos-t_size, x_pos-t_size*0.7, x_pos, x_pos+t_size*0.7, x_pos+t_size,
                                x_pos+t_size*0.7, x_pos, x_pos-t_size*0.7, x_pos-t_size]
                y_square_pos = [y_pos, y_pos+t_size*0.7, y_pos+t_size, y_pos+t_size*0.7, y_pos,
                                y_pos-t_size*0.7, y_pos-t_size, y_pos-t_size*0.7, y_pos]
                line.set_data(x_square_pos, y_square_pos)
            else:
                x_square_pos = [-c_size, -c_size*0.7,      0, c_size*0.7, c_size,  c_size*0.7, 0, -c_size*0.7, - c_size]
                y_square_pos = [0,  c_size*0.7, c_size, c_size*0.7,      0, -c_size*0.7, -c_size, -c_size*0.7, 0]
                line.set_data(x_square_pos, y_square_pos)
        return self.lines

    def plot_animate_full(self):
        c_size = self.planets[0].radius
        sq_size = []
        for i in range(len(self.planets)):
            sq_size += [max(self.planets[i].radius, 0.02*self.animation_scale)]
        self.x_positions = []
        self.y_positions = []
        for _ in range(len(self.planets)):
            self.x_positions += [[]]
            self.y_positions += [[]]
        animation_list = deepcopy(self.planets)
        interval = round(50*self.current_time/self.precision_max/self.animation_length/1000)
        for j in range(len(animation_list)):
            for i in range(0, len(animation_list[j].position.history)):
                if self.time_list[i] % (self.precision_max*interval) == 0:
                    self.x_positions[j] += [animation_list[j].position.history[i].x]
                    self.y_positions[j] += [animation_list[j].position.history[i].y]
        fig = figure()
        ax = axes(xlim=(-self.animation_scale, self.animation_scale),
                  ylim=(-self.animation_scale, self.animation_scale))
        self.lines = [plot([], [])[0] for _ in range(2*len(animation_list)+1)]
        for i in range(len(animation_list)):
            self.lines[i].set_color(self.planets[i].colour)
            self.lines[i + len(animation_list)].set_color(self.planets[i].colour)
        self.lines[-1].set_color("black")
        time_interval = self.animation_length*1000/len(self.x_positions[0])
        if time_interval > 500:
            time_interval = 500
        print(time_interval, time_interval * len(self.x_positions[0]))
        an = FuncAnimation(fig, self.plot_animate_single, fargs=[animation_list, c_size, sq_size],
                           init_func=self.animation_init, frames=len(self.x_positions[0]), interval=time_interval,
                           blit=True, repeat=False)
        show()

    def plot_animate_relative_position(self):
        c_size = self.main_planet.radius
        sq_size = []
        for i in range(len(self.plot_planets)):
            sq_size += [max(self.plot_planets[i].radius, 0.02*self.animation_scale)]
        self.x_positions = []
        self.y_positions = []
        for _ in range(len(self.plot_planets)):
            self.x_positions += [[]]
            self.y_positions += [[]]
        animation_list = deepcopy(self.plot_planets)
        a = 0
        b = self.time_list[-1]
        start_time = int(input('Please input a start time: '))
        interval = round(50*self.current_time/self.precision_max/self.animation_length/1000)
        for j in range(len(animation_list)):
            for i in range(start_time, len(animation_list[j].position.history)):
                if i < len(self.time_list) and self.time_list[i] % (self.precision_max*interval) == 0 and \
                   a <= self.time_list[i] <= b:
                    self.x_positions[j] += [animation_list[j].position.history[i].x -
                                            self.main_planet.position.history[i].x]
                    self.y_positions[j] += [animation_list[j].position.history[i].y -
                                            self.main_planet.position.history[i].y]
        fig = figure()
        ax = axes(xlim=(-self.animation_scale, self.animation_scale), ylim=(-self.animation_scale,
                                                                            self.animation_scale))
        self.lines = [plot([], [])[0] for _ in range(2*len(animation_list)+1)]
        print("Number of frames: " + str(len(self.x_positions[0])))
        time_interval = self.animation_length*1000/len(self.x_positions[0])
        if time_interval > 500:
            time_interval = 500
        print("Time interval: " + str(time_interval))
        an = FuncAnimation(fig, self.plot_animate_single, fargs=[animation_list, c_size, sq_size],
                           init_func=self.animation_init, frames=len(self.x_positions[0])-1, interval=time_interval,
                           blit=True, repeat=False)
        show()

    def _calculate_velocity_change(self, p1, p2):
        # Note, this is not the actual velocity change (acceleration), this is acceleration/mass_of_other_object
        a = self.planets[p1].position.current.x - self.planets[p2].position.current.x
        b = self.planets[p1].position.current.y - self.planets[p2].position.current.y
        c = a**2 + b**2
        acceleration = self.g/c/sqrt(c)*self.precision_cur
        return [a*acceleration, b*acceleration]

    def _calculate_new_velocities(self):
        for p1 in range(len(self.planets)):
            for p2 in range(p1+1, len(self.planets)):
                if self.planets[p1].started and self.planets[p2].started and (self.planets[p1].mass != 0 or
                                                                              self.planets[p2].mass != 0):
                    acceleration = self._calculate_velocity_change(p1, p2)
                    # The negative here is because acceleration is calculated as the same for 1->2 as 2->1 for
                    # efficiency reasons, but they should be in opposite directions
                    self.planets[p1].update_velocity(acceleration, -self.planets[p2].mass)
                    self.planets[p2].update_velocity(acceleration,  self.planets[p1].mass)
            self.planets[p1].activate_impulse(self.planets, self.current_time, self.precision_cur)
        for p3 in range(len(self.planets)):
            if not self.planets[p3].started:
                for p4 in range(len(self.planets)):
                    if self.planets[p3].delayed_details.follow == self.planets[p4].name:
                        self.planets[p3].set_velocity(self.planets[p4].velocity.current)

    def _check_if_planets_close(self, p1, p2, radius):
        if min(self.planets[p1].position.current.x, self.planets[p1].position.previous.x) -\
                max(self.planets[p2].position.current.x, self.planets[p2].position.previous.x) > radius:
            return False
        elif min(self.planets[p2].position.current.x, self.planets[p2].position.previous.x) -\
                max(self.planets[p1].position.current.x, self.planets[p1].position.previous.x) > radius:
            return False
        elif min(self.planets[p1].position.current.y, self.planets[p1].position.previous.y) -\
                max(self.planets[p2].position.current.y, self.planets[p2].position.previous.y) > radius:
            return False
        elif min(self.planets[p2].position.current.y, self.planets[p2].position.previous.y) -\
                max(self.planets[p1].position.current.y, self.planets[p1].position.previous.y) > radius:
            return False
        else:
            return True

    def _calculate_time_at_closest(self, p1, p2):
        i = self.planets[p1].position.previous.x - self.planets[p1].position.current.x -\
            self.planets[p2].position.previous.x + self.planets[p2].position.current.x
        j = self.planets[p1].position.previous.y - self.planets[p1].position.current.y -\
            self.planets[p2].position.previous.y + self.planets[p2].position.current.y
        time = (i*(self.planets[p1].position.previous.x - self.planets[p2].position.previous.x) + j *
                (self.planets[p1].position.previous.y - self.planets[p2].position.previous.y)) / (i*i + j * j)
        if time < 0:
            time = 0
        elif time > 1:
            time = 1
        return time

    def _determine_if_collision(self, p1, p2, time, combined_radius):
        x_part = self.planets[p1].position.current.x*time + self.planets[p1].position.previous.x*(1 - time) -\
            self.planets[p2].position.previous.x*(1 - time) - self.planets[p2].position.current.x*time
        y_part = self.planets[p1].position.current.y*time + self.planets[p1].position.previous.y*(1 - time) -\
            self.planets[p2].position.previous.y*(1 - time) - self.planets[p2].position.current.y*time
        distance = sqrt(x_part * x_part + y_part * y_part)
        if distance >= combined_radius:
            return False
        else:
            return True

    def _crash_checker_single(self, p1, p2):
        if self._check_if_planets_close(p1, p2, self.planets[p1].radius + self.planets[p2].radius):
            time = self._calculate_time_at_closest(p1, p2)
            if self._determine_if_collision(p1, p2, time, self.planets[p1].radius + self.planets[p2].radius):
                return True
        return False

    def _crash_checker(self, previous_time):
        collision_string = ''
        for p1 in range(len(self.planets)):
            for p2 in range(p1+1, len(self.planets)):
                if (self.planets[p1].radius != 0 or self.planets[p2].radius != 0) and not self.planets[p1].crashed \
                        and not self.planets[p2].crashed and self.planets[p1].started and self.planets[p2].started and \
                        (not self.planets[p1].delayed or self.planets[p1].delayed_details.time != previous_time) and \
                        (not self.planets[p2].delayed or self.planets[p2].delayed_details.time != previous_time):
                    collision = self._crash_checker_single(p1, p2)
                    if collision:
                        velocity = sqrt((self.planets[p1].velocity.current.x - self.planets[p2].velocity.current.x)**2 +
                                        (self.planets[p1].velocity.current.y - self.planets[p2].velocity.current.y)**2)
                        delt_x = self.planets[p1].position.current.x - self.planets[p2].position.current.x
                        delt_y = self.planets[p1].position.current.y - self.planets[p2].position.current.y
                        delt_vx = self.planets[p1].velocity.current.x - self.planets[p2].velocity.current.x
                        delt_vy = self.planets[p1].velocity.current.y - self.planets[p2].velocity.current.y
                        if delt_x == 0:
                            pos_angle = 90
                        else:
                            pos_angle = 180/pi*arctan(delt_y/delt_x)
                        # if delt_y < 0:
                        # UNTESTED CORRECTION
                        if delt_x < 0:
                            if pos_angle > 0:
                                pos_angle -= 180
                            else:
                                pos_angle += 180
                        v_angle = 180/pi*arctan(delt_vy/delt_vx)
                        if delt_vy < 0:
                            if v_angle > 0:
                                v_angle -= 180
                            else:
                                pos_angle += 180
                        impact_angle = pos_angle + v_angle
                        # print(f'Position angle: {pos_angle}\tVelocity angle: {v_angle}\tImpact angle: {impact_angle}')
                        collision_string = f'Crashed: {self.planets[p1].name} {self.planets[p2].name} at ' + \
                                           f'{self.current_time}. Velocity = {velocity}. Impact angle: {impact_angle}'
                        if self.planets[p1].crash_checking and self.planets[p2].crash_checking:
                            return collision, collision_string
                        else:
                            print(collision_string)
                            if not self.planets[p1].crash_checking:
                                self.planets[p1].crashed = True
                            if not self.planets[p2].crash_checking:
                                self.planets[p2].crashed = True
        return False, collision_string

    def _determine_new_precision(self):
        distance_squared = (self.planets[0].position.current.x - self.planets[1].position.current.x)**2 +\
                           (self.planets[0].position.current.y - self.planets[1].position.current.y)**2
        max_ratio = self.g/distance_squared*self.precision_cur*max(self.planets[0].mass, self.planets[1].mass)
        for p1 in range(2, len(self.planets)):
            for p2 in range(p1):
                if self.planets[p1].started and self.planets[p2].started and (self.planets[p1].mass != 0 or
                                                                              self.planets[p2].mass != 0):
                    distance_squared = (self.planets[p1].position.current.x - self.planets[p2].position.current.x)**2 +\
                                       (self.planets[p1].position.current.y - self.planets[p2].position.current.y)**2
                    new_ratio = self.g/distance_squared*self.precision_cur*max(self.planets[p1].mass,
                                                                               self.planets[p2].mass)
                    if new_ratio > max_ratio:
                        max_ratio = new_ratio
        if max_ratio > 5:
            if self.precision_cur != self.precision_min:
                print(f'precision changed to {self.precision_cur} at time {self.current_time}')
                self.precision_cur = max(self.precision_cur/10, self.precision_min)
        elif max_ratio < 0.5 and round(self.current_time/self.precision_cur, 0) % 10 == 0:
            if self.precision_cur != self.precision_max:
                print(f'precision changed to {self.precision_cur} at time {self.current_time}')
                self.precision_cur = min(self.precision_cur*10, self.precision_max)

    def _start_delayed_starters(self):
        for this_planet in range(len(self.planets)):
            if not self.planets[this_planet].started and \
                   self.planets[this_planet].delayed_details.time == self.current_time:
                for other_planet in range(len(self.planets)):
                    if self.planets[other_planet].name == self.planets[this_planet].delayed_details.follow:
                        following_planet = self.planets[other_planet]
                    if self.planets[other_planet].name == self.planets[this_planet].delayed_details.oriented:
                        oriented_planet = self.planets[other_planet]
                    if self.planets[other_planet].name == self.planets[this_planet].delayed_details.velocity_oriented:
                        velocity_planet = self.planets[other_planet]
                self.planets[this_planet].start_planet(following_planet, oriented_planet, velocity_planet)

    def run(self, record_history=True):
        if not self.planets_loaded:
            self.load_planets()
        print(f'The input parameters are: Max time = {self.max_time}\tMax runs = {self.max_runs}\tPrecision from ' +
              f'{self.precision_min} to {self.precision_max}')
        collision = False
        collision_string = ''
        self.time_list = [0]
        current_printing_threshold = 5
        while self.current_time < self.max_time and self.current_run < self.max_runs:
            self._determine_new_precision()
            for planet_num in range(len(self.planets)):
                self.planets[planet_num].increment_time_point(self.precision_cur, record_history)
            self._calculate_new_velocities()
            self._start_delayed_starters()
            previous_time = self.current_time
            self.current_time = round(self.current_time + self.precision_cur, 5)
            self.time_list += [self.current_time]
            self.current_run += 1
            collision, collision_string = self._crash_checker(previous_time)
            if collision:
                print(f'Time: {self.current_time}')
                break
            if self.print_percentages and max(self.current_run/self.max_runs, self.current_time/self.max_time)*100 >\
                    current_printing_threshold:
                print(f'Run {self.current_run}\t({int(self.current_run*100/self.max_runs)}%).\t' +
                      f'Time {self.current_time}\t({int(self.current_time*100/self.max_time)}%)')
                current_printing_threshold += 5
        if collision:
            print(collision_string)
            if self.print_percentages:
                print(f'Ended at run {self.current_run} and time {self.current_time}')    
        elif self.print_percentages:
            print(f'No crash. Ended at run {self.current_run} and time {self.current_time}')
    
    @staticmethod
    def print_info():
        print('Valid commands are:')
        # Animation commands
        print('AL\tAnimate Locations')
        print('ARL\tAnimate Relative Locations')
        print('ARLS\tAnimate Relative Locations with a user-given Scale')
        # Graphing commands
        print('GA\tGraph Angle')
        print('GRA\tGraph Relative Angle')
        print('GD\tGraph Distance from centre')
        print('GP\tGraph Positions')
        print('GPX\tGraph Position X')
        print('GPY\tGraph Position Y')
        print('GRD\tGraph Relative Distance')
        print('GRP\tGraph Relative Position')
        print('GRX\tGraph Relative X position')
        print('GRY\tGraph Relative Y position')
        print('GV\tGraph Velocity')
        print('GRV\tGraph Relative Velocity')
        print('GVX\tGraph Velocity X value')
        print('GVY\tGraph Velocity Y value')
        print('GAD\tGraph Angle relative to a specific object against Distance')
        print('PR2\tPlot Relative to 2 fixed objects as if it was a binary star-system')
        # Set commands
        print('SG\tSet Graphing planets')
        print('SGR\tSet Graphing Relative planets')
        print('SPM\tSet ParaMeters')
        print('SMT\tSet Minimum plotting Time')
        print('SPD\tSet Planet Data')
        # Other commands
        print('E\tExit')
        print('I\tPrint info')
        print('L\tLoad planets')
        print('P\tPrint information for a planet for a specified time')
        print('R\tRun the system')
        print('RAL\tReset All Planets')
        print('W\tWrite current data to file')

    def process_commands(self, process_list, extra_information=None):
        ret = 'Fine'
        i = 0
        for inp in process_list:
            if extra_information is None or i >= len(extra_information):
                extra_info = None
            else:
                extra_info = extra_information[i]
            if inp == 'E':
                ret = 'Exit'
                break
            elif inp == 'I':
                self.print_info()
            elif inp == 'GL':
                self.plot_position()
            elif inp == 'GD':
                self.plot_distance()
            elif inp == 'GLX':
                self.plot_position_x()
            elif inp == 'GLY':
                self.plot_position_y()
            elif inp == 'GV':
                self.plot_velocity()
            elif inp == 'GVX':
                self.plot_velocity_x()
            elif inp == 'GVY':
                self.plot_velocity_y()
            elif inp == 'GA':
                self.plot_angles()
            elif inp == 'GRA':
                self.plot_relative_angles()
            elif inp == 'GRL':
                self.plot_relative_position()
            elif inp == 'GRD':
                self.plot_relative_distance()
            elif inp == 'GRX':
                self.plot_relative_position_x()
            elif inp == 'GRY':
                self.plot_relative_position_y()
            elif inp == 'GRV':
                self.plot_relative_velocity()
            elif inp == 'GAD':
                self.plot_distance_relative_to_angle()
            elif inp == 'PR2':
                self.plot_relative_to_two_fixed_stars()
            elif inp == 'AL':
                self.plot_animate_full()
            elif inp == 'ARL':
                self.plot_animate_relative_position()
            elif inp == 'R':
                self.run()
            elif inp == 'SR':
                self.get_planets_for_running(extra_info)
                i += 1
            elif inp == 'SG':
                self.get_subset_planets('Plotting')
            elif inp == 'SGR':
                self.get_relative_planets()
            elif inp == 'SMT':
                self.set_min_time()
            elif inp == 'SPM':
                self.set_parameters(extra_info)
                i += 1
            elif inp == 'SPD':
                self.set_planet_value(int(extra_info[0]), extra_info[1].upper(), extra_info[2:])
                i += 1
            elif inp == 'L':
                self.load_planets()
            elif inp == 'P':
                self.print_info_for_planet_for_time()
            elif inp == 'W':
                self.write_to_file()
            elif inp == 'RAL':
                self.reset_all_planets()
            elif inp == 'A':
                try:
                    analysis(self)
                except (ValueError, IndexError) as e:
                    print(f'Analysis failed! The error was {e}')
            elif inp == 'A2':
                try:
                    analysis_2(self)
                except (ValueError, IndexError) as e:
                    print(f'Analysis failed! The error was {e}')
            else:
                ret = 'invalid'
        return ret
