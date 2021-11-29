import numpy as np


def get_distance(p1, p2, t):
    return np.sqrt((p1.position.history[t].x - p2.position.history[t].x)**2 + (p1.position.history[t].y -
                                                                               p2.position.history[t].y)**2)


def get_velocity_difference(p1, p2, t):
    return np.sqrt((p1.velocity.history[t].x - p2.velocity.history[t].x)**2 + (p1.velocity.history[t].y -
                                                                               p2.velocity.history[t].y)**2)


def analysis_2(planet_set):
    min_d = get_distance(planet_set.planets[0], planet_set.planets[1], 0)
    max_d = min_d
    for i in range(1, len(planet_set.planets[0].position.history)):
        d = get_distance(planet_set.planets[0], planet_set.planets[1], i)
        if d < min_d:
            min_d = d
        if d > max_d:
            max_d = d
    print(f'The minimum distance was {round(min_d, 3)} , the maximum distance was {round(max_d, 3)} and ' +
          f'the % difference was {round(max_d*100/min_d-100, 2)}%')


def analysis(planet_set):
    d0 = get_distance(planet_set.planets[2], planet_set.planets[3], 0)
    d1 = get_distance(planet_set.planets[2], planet_set.planets[3], 1)
    d2 = get_distance(planet_set.planets[2], planet_set.planets[3], 2)
    if d1 < d0 and d1 < d2:
        print(f'Local minimum: {planet_set.time_list[1]} {d1}')
    elif d1 > d0 and d1 > d2:
        print(f'Local maximum: {planet_set.time_list[1]} {d1}')
    for t in range(3, len(planet_set.time_list)):
        d0 = d1
        d1 = d2
        d2 = get_distance(planet_set.planets[2], planet_set.planets[3], t)
        if d1 < d0 and d1 < d2:
            print('Local minimum:', planet_set.time_list[t], d1)
        elif d1 > d0 and d1 > d2:
            print('Local maximum:', planet_set.time_list[t], d1)
    d0 = get_velocity_difference(planet_set.planets[2], planet_set.planets[3], 0)
    d1 = get_velocity_difference(planet_set.planets[2], planet_set.planets[3], 1)
    d2 = get_velocity_difference(planet_set.planets[2], planet_set.planets[3], 2)
    if d1 < d0 and d1 < d2:
        print('Local minimum velocity:', planet_set.time_list[1], d1)
    elif d1 > d0 and d1 > d2:
        print('Local maximum velocity:', planet_set.time_list[1], d1)
    for t in range(3, len(planet_set.time_list)):
        d0 = d1
        d1 = d2
        d2 = get_velocity_difference(planet_set.planets[2], planet_set.planets[3], t)
        if d1 < d0 and d1 < d2:
            print('Local minimum velocity:', planet_set.time_list[t], d1)
        elif d1 > d0 and d1 > d2:
            print('Local maximum velocity:', planet_set.time_list[t], d1)
