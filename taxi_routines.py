#!/usr/bin/python3

import os
import time
import sys


# -------------------------- input
def load_data(filename) -> (int, int, int, int, int, int, list):
    c_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(c_dir, filename), 'r') as f_file:
        header_conf = [int(num) for num in f_file.readline().split()]
        rows_R = header_conf[0]
        columns_C = header_conf[1]
        fleet_F = header_conf[2]
        rides_N = header_conf[3]
        bonus_B = header_conf[4]
        steps_T = header_conf[5]

        # read matrix
        routes = [[0 for _ in range(7)] for x in range(rides_N)]
        for row in range(rides_N):
            str_line = f_file.readline().split()
            column = list(str_line)
            for ride_parameter_index in range(len(column)):
                routes[row][ride_parameter_index] = int(column[ride_parameter_index])
            routes[row][6] = row

        return(rows_R, columns_C, fleet_F, rides_N, bonus_B, steps_T,  routes)
    return 0


# -------------------------- output
def write_out(cars, filename='default'):
    """ Form output string. """
    out = ''
    for car in cars:
        out += '{}\n'.format(car.result)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result-{}.out'.format(filename)), 'w+') as f:
            f.write(out)
    return out


# -------------------------- analytics
def printAnalyticsData(data_set, routes, cars, rides, bonus, steps) -> (int, int, int):
    print("Working on data set: {}. Count - {}".format(data_set, rides))
    # print('parsed routes - {}'.format(len(routes)))

    total_distance = 0
    for route in routes:
        total_distance += route.distance

    max_bonus = bonus * rides

    max_score = total_distance + max_bonus

    deistance_per_step = total_distance/steps
    print('Need to do distance per step - {:0.2f}'.format(deistance_per_step))
    print('cars count - {}'.format(len(cars)))

    rides_coverage = min(len(cars)/deistance_per_step*100, 100)
    print('rides can be covered - {:0.2f}%'.format(rides_coverage))

    print('max bonus - {}'.format(max_bonus))
    print('total dist- {}'.format(total_distance))
    print('max score - {}'.format(max_score))

    our_score = 0
    for car in cars:
        our_score += car.score
    print('our score - {}'.format(our_score))

    print('efficiency - {:0.2f}%'.format(our_score/max_score*100))
    print()

    # print_steps_info(steps, cars)
    # for car in cars:
    #     print('{}'.format(car.result))

    return (total_distance, max_score, our_score)


def print_steps_info(steps, cars):
    print('final time - {}'.format(steps))
    for car in cars:
        print('car {}, score {}, final time - {}'.format(car.index, car.score, car.current_time))
