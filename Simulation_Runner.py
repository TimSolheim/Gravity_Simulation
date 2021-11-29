from Class_PlanetSet import PlanetSet


def main_process():
    planets = PlanetSet()
    while True:
        inp = input('Please input a set of instruction: ')
        if inp == 'E':
            break
        instruction_set = inp.split(' ')
        inp2 = input('Please input extra information: ')
        if inp2 == '':
            extra_information = None
        else:
            temp = inp2.split('|')
            extra_information = []
            for x in temp:
                a = x.split(' ')
                if a[0] == '':
                    del a[0]
                if a[-1] == '':
                    del a[-1]
                extra_information += [a]
        # instruction_set = ['SPM'] + ['R', 'A2', 'RAL', 'SPD', 'SPD']*10 + ['E']
        # extra_information = [['E', 'E', 'E', 'E', 'F']]
        # for i in range(10):
        #     extra_information += [['0', 'Velocity_XY', '0', str(14400+i)], ['1', 'Velocity_XY', '0', str(-14400-i)]]
        ret = planets.process_commands(instruction_set, extra_information)
        if ret == 'Exit':
            break


# UNITS USED HERE:  Mass:       10**24 kg instead of kg, 
#                   Distance:   1 km instead of 1 m
#                   Time:       10 minutes instead of 1 s
main_process()
print('Done')
